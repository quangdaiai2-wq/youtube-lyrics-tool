"""
core.py - Trích xuất lyrics từ video YouTube.

Luồng xử lý:
  1. Lấy thông tin video + danh sách phụ đề có sẵn (yt-dlp).
  2. Nếu có phụ đề  -> dùng luôn (nhanh, chính xác).
  3. Nếu không có  -> tải audio -> nhận dạng giọng nói (faster-whisper).

Không cần người dùng hiểu gì bên trong file này.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# Cấu hình
# ---------------------------------------------------------------------------

# Ưu tiên phụ đề theo thứ tự này (vi trước, rồi en, rồi các thứ tiếng khác)
PREFERRED_SUB_LANGS = ["vi", "en"]

# Model Whisper: tiny | base | small | medium
# "base" là điểm cân bằng tốt giữa tốc độ và độ chính xác cho cả vi + en,
# và nhẹ nên chạy tốt trên máy thường. Muốn chính xác hơn thì đổi sang
# "small" hoặc "medium" (chậm hơn, nặng hơn).
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "base")

_whisper_model_cache = {}


@dataclass
class LyricResult:
    ok: bool
    video_id: str = ""
    title: str = ""
    channel: str = ""
    duration: int = 0
    thumbnail: str = ""
    web_url: str = ""
    lyrics: str = ""
    source: str = ""          # "subtitle" | "whisper" | ""
    language: str = ""
    detected_language: str = ""
    warnings: list[str] = field(default_factory=list)
    error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Tiện ích
# ---------------------------------------------------------------------------

def extract_video_id(url: str) -> str:
    """Lấy ID video từ nhiều dạng link YouTube khác nhau."""
    url = (url or "").strip()
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:shorts/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
        r"(?:live/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    # Nếu người dùng dán thẳng ID 11 ký tự
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url
    return ""


def _clean_vtt(raw: str) -> str:
    """Chuyển nội dung phụ đề .vtt thành text sạch, đã gộp trùng."""
    lines = raw.splitlines()
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("WEBVTT") or s.startswith("Kind:") or s.startswith("Language:"):
            continue
        if "-->" in s:
            continue
        if re.fullmatch(r"\d+", s):
            continue
        # Bỏ thẻ định dạng như <00:00:01.234><c> ... </c>
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"&amp;#39;", "'", s)
        s = re.sub(r"&amp;quot;", '"', s)
        s = s.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
        s = s.strip()
        if s:
            out.append(s)

    # Gộp các dòng trùng lặp liên tiếp (phụ đề auto hay bị lặp)
    merged: list[str] = []
    for s in out:
        if not merged or merged[-1] != s:
            merged.append(s)

    text = "\n".join(merged)
    # Phụ đề auto thường không có dấu câu -> thêm dấu chấm cuối dòng cho dễ đọc
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _fmt_time(seconds: float) -> str:
    seconds = int(seconds or 0)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ---------------------------------------------------------------------------
# Bước 1 + 2: lấy phụ đề có sẵn
# ---------------------------------------------------------------------------

def fetch_subtitle(url: str, video_id: str, workdir: Path,
                   log: Callable[[str], None] = lambda m: None) -> tuple[str, str]:
    """
    Thử lấy phụ đề có sẵn. Trả về (lyrics, language) hoặc ("", "").
    """
    import yt_dlp

    log("Đang kiểm tra phụ đề có sẵn của video...")

    # 1) Thử phụ đề do người đăng tự làm (chính xác nhất)
    for kind, flag in (("manual", True), ("auto", False)):
        opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writesubtitles": flag,
            "writeautomaticsub": not flag,
            "subtitleslangs": ["vi", "en", "vi-VN", "en-US", "en-GB"],
            "subtitlesformat": "vtt",
            "outtmpl": str(workdir / "%(id)s.%(ext)s"),
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as exc:  # noqa: BLE001
            log(f"  (bỏ qua {kind}: {type(exc).__name__})")
            continue

        vtt_files = sorted(workdir.glob("*.vtt"))
        if not vtt_files:
            continue

        # Ưu tiên file .vi / .en nếu có nhiều bản
        def rank(p: Path) -> int:
            n = p.name.lower()
            for i, lang in enumerate(PREFERRED_SUB_LANGS):
                if f".{lang}." in n:
                    return i
            return len(PREFERRED_SUB_LANGS)

        vtt_files.sort(key=rank)
        chosen = vtt_files[0]
        raw = chosen.read_text(encoding="utf-8", errors="ignore")
        text = _clean_vtt(raw)
        if text:
            lang = chosen.name.split(".")[-2] if chosen.name.count(".") >= 2 else ""
            kind_vi = "phụ đề do người đăng" if kind == "manual" else "phụ đề tự động của YouTube"
            log(f"  ✅ Đã lấy được {kind_vi} ({lang}) — {len(text)} ký tự.")
            return text, lang

        for f in vtt_files:
            f.unlink(missing_ok=True)

    log("  ⚠️ Video không có phụ đề sẵn.")
    return "", ""


# ---------------------------------------------------------------------------
# Bước 3: tải audio + nhận dạng giọng nói
# ---------------------------------------------------------------------------

def _download_audio(url: str, workdir: Path,
                    log: Callable[[str], None] = lambda m: None,
                    progress: Callable[[float, str], None] | None = None) -> Path | None:
    """
    Tải audio của video. Ưu tiên định dạng đọc được trực tiếp (m4a/mp3/ogg/webm),
    không cần ffmpeg.

    progress: hàm nhận (phần_trăm, mô_tả) để báo tiến độ tải về.
    """
    import yt_dlp

    def report(pct: float, note: str = "") -> None:
        if progress:
            progress(max(0.0, min(100.0, pct)), note)

    log("Đang tải audio của video (chỉ phần tiếng, không tải hình)...")
    report(0, "Bắt đầu tải")

    def hook(d: dict) -> None:
        """yt-dlp gọi hàm này trong lúc tải để báo tiến độ."""
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes") or 0
            if total:
                pct = done / total * 100
                mb_done = done / 1_048_576
                mb_total = total / 1_048_576
                speed = d.get("speed") or 0
                speed_txt = f" — {speed/1_048_576:.1f} MB/s" if speed else ""
                report(pct, f"{mb_done:.0f}/{mb_total:.0f} MB{speed_txt}")
        elif d.get("status") == "finished":
            report(100, "Tải xong")

    opts = {
        "quiet": True,
        "no_warnings": True,
        # m4a (AAC) và webm (Opus) là định dạng YouTube hay dùng nhất
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
        "outtmpl": str(workdir / "audio.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [hook],
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as exc:  # noqa: BLE001
        log(f"  ❌ Không tải được audio: {exc}")
        return None

    for ext in ("m4a", "webm", "mp3", "ogg", "opus", "flac", "wav", "aac"):
        p = workdir / f"audio.{ext}"
        if p.exists():
            size_mb = p.stat().st_size / 1_048_576
            log(f"  ✅ Đã tải audio ({size_mb:.1f} MB, định dạng {ext}).")
            return p
    return None


def _resolve_model_path(size: str, log: Callable[[str], None] = lambda m: None) -> str:
    """
    Trả về đường dẫn model, hoặc tên model để thư viện tự tải.

    Cơ chế tải tự động của thư viện đôi khi tạo file rỗng khi mạng gián đoạn,
    nên ta ưu tiên bản đã tải qua download_model.py (có kiểm tra + thử lại).
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from download_model import ensure_model, cache_dir, MODELS, MIN_BIN_SIZE

        repo = MODELS.get(size)
        if repo:
            snap = cache_dir(repo) / "snapshots" / "manual"
            bin_path = snap / "model.bin"
            if bin_path.exists() and bin_path.stat().st_size >= MIN_BIN_SIZE.get(size, 1):
                log(f"  Dùng model đã tải sẵn tại máy ({size}).")
                return str(snap)
        log(f"  Chưa có model '{size}', đang tải về (có kiểm tra và thử lại)...")
        p = ensure_model(size)
        if p:
            return str(p)
    except Exception as exc:  # noqa: BLE001
        log(f"  (Không dùng được bộ tải riêng: {type(exc).__name__}, "
            f"chuyển sang cách tải mặc định)")
    return size


def _load_audio_array(audio_path: Path, log: Callable[[str], None] = lambda m: None):
    """
    Đọc file audio thành mảng số (numpy) ở 16kHz mono.

    Vì sao tự đọc: hàm đọc audio sẵn có của thư viện dùng một tham số mà bản
    thư viện âm thanh hiện tại không hỗ trợ, gây lỗi. Ta gọi thư viện âm thanh
    trực tiếp ở dạng cơ bản — cách này chạy được và không cần cài ffmpeg.
    """
    import numpy as np
    import av

    log("Đang đọc dữ liệu âm thanh...")
    container = av.open(str(audio_path), mode="r")

    chunks: list = []
    src_rate = 0
    try:
        stream = next(s for s in container.streams if s.type == "audio")
        src_rate = stream.rate or 0
        # Đưa về 16kHz mono ngay trong quá trình giải mã -> Whisper nhận trực tiếp
        resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
        for frame in container.decode(stream):
            for out_frame in resampler.resample(frame):
                arr = out_frame.to_ndarray()
                chunks.append(arr.reshape(-1))
        # Xả nốt phần còn lại trong bộ đổi mẫu
        for out_frame in resampler.resample(None):
            chunks.append(out_frame.to_ndarray().reshape(-1))
    finally:
        container.close()

    if not chunks:
        raise RuntimeError("Không đọc được dữ liệu âm thanh từ video.")

    data = np.concatenate(chunks).astype("float32") / 32768.0
    dur = len(data) / 16000
    log(f"  Âm thanh dài {dur:.1f} giây (gốc {src_rate} Hz → 16000 Hz mono).")
    return data


def transcribe_audio(audio_path: Path, workdir: Path,
                     log: Callable[[str], None] = lambda m: None,
                     progress: Callable[[float, str], None] | None = None
                     ) -> tuple[str, str]:
    """
    Nhận dạng giọng nói bằng faster-whisper.

    progress: hàm nhận (phần_trăm 0..100, mô_tả) để báo tiến độ ra ngoài.
              Nhận dạng là bước lâu nhất nên cần báo để người dùng biết còn bao lâu.
    Trả về (lyrics có timestamp, ngôn ngữ phát hiện).
    """
    from faster_whisper import WhisperModel

    def report(pct: float, note: str = "") -> None:
        if progress:
            progress(max(0.0, min(100.0, pct)), note)

    log(f"Đang nạp model nhận dạng giọng nói '{WHISPER_MODEL}'...")
    report(0, "Đang nạp model")

    if WHISPER_MODEL not in _whisper_model_cache:
        model_ref = _resolve_model_path(WHISPER_MODEL, log=log)
        _whisper_model_cache[WHISPER_MODEL] = WhisperModel(
            model_ref, device="cpu", compute_type="int8"
        )
    model = _whisper_model_cache[WHISPER_MODEL]

    # Tự đọc audio để tránh lỗi tương thích thư viện
    report(2, "Đang đọc âm thanh")
    audio = _load_audio_array(audio_path, log=log)
    total_sec = len(audio) / 16000 if len(audio) else 0

    log("Đang nghe và nhận dạng lời bài hát... (video dài sẽ lâu hơn)")
    report(5, "Bắt đầu nghe")

    segments, info = model.transcribe(
        audio,
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 700},
    )

    lang = getattr(info, "language", "") or ""
    log(f"  ✅ Ngôn ngữ nhận dạng: {lang} "
        f"(độ tin cậy {getattr(info, 'language_probability', 0):.0%})")

    # faster-whisper trả về bộ sinh (generator) — tiến độ chỉ tăng khi ta đọc dần.
    # Mỗi đoạn có mốc thời gian kết thúc, nên biết được đã nghe tới đâu.
    lines: list[str] = []
    last_report = 0.0
    for seg in segments:
        txt = (seg.text or "").strip()
        if txt:
            lines.append(f"[{_fmt_time(seg.start)}] {txt}")
        if total_sec > 0:
            # Lấy 90% quãng đường cho phần nghe, chừa 10% cho bước gom kết quả
            pct = 5 + (min(seg.end, total_sec) / total_sec) * 90
            if pct - last_report >= 0.5:      # báo mỗi khi tăng thêm 0.5%
                last_report = pct
                heard = _fmt_time(seg.end)
                total = _fmt_time(total_sec)
                report(pct, f"Đã nghe {heard} / {total}")

    report(100, "Hoàn tất")
    return "\n".join(lines), lang


# ---------------------------------------------------------------------------
# Bước 0: metadata video
# ---------------------------------------------------------------------------

def fetch_metadata(url: str) -> dict:
    import yt_dlp

    opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title") or "",
            "channel": info.get("uploader") or info.get("channel") or "",
            "duration": int(info.get("duration") or 0),
            "thumbnail": info.get("thumbnail") or "",
            "id": info.get("id") or "",
        }
    except Exception:  # noqa: BLE001
        return {}


# ---------------------------------------------------------------------------
# Hàm chính
# ---------------------------------------------------------------------------

def get_lyrics(url: str, force_whisper: bool = False,
               log: Callable[[str], None] = lambda m: None,
               progress: Callable[[str, float, str], None] | None = None) -> LyricResult:
    """
    Lấy lyrics đầy đủ từ link YouTube.

    progress: hàm nhận (giai_đoạn, phần_trăm, mô_tả) để báo tiến độ ra ngoài.
              giai_đoạn là "download" hoặc "transcribe".
    """
    def report(stage: str, pct: float, note: str = "") -> None:
        if progress:
            progress(stage, max(0.0, min(100.0, pct)), note)

    video_id = extract_video_id(url)
    if not video_id:
        return LyricResult(ok=False, error="Link YouTube không hợp lệ. "
                                           "Đại hãy dán đúng link dạng youtube.com/watch?v=... hoặc youtu.be/...")

    canonical = f"https://www.youtube.com/watch?v={video_id}"
    result = LyricResult(ok=False, video_id=video_id)

    log("Đang đọc thông tin video...")
    meta = fetch_metadata(canonical)
    if meta:
        result.title = meta.get("title", "")
        result.channel = meta.get("channel", "")
        result.duration = meta.get("duration", 0)
        result.thumbnail = meta.get("thumbnail", "")
    result.web_url = canonical

    if result.title:
        log(f"  📺 {result.title} — {result.channel} ({_fmt_time(result.duration)})")

    workdir = Path(tempfile.mkdtemp(prefix="ytlyrics_"))
    try:
        # --- Nhánh 1: phụ đề có sẵn ---
        if not force_whisper:
            text, lang = fetch_subtitle(canonical, video_id, workdir, log=log)
            if text:
                result.ok = True
                result.lyrics = text
                result.source = "subtitle"
                result.language = lang
                result.detected_language = lang
                return result
        else:
            log("Đại đã chọn bỏ qua phụ đề, đi thẳng vào nhận dạng giọng nói.")

        # --- Nhánh 2: nhận dạng giọng nói ---
        audio = _download_audio(canonical, workdir, log=log, progress=(
            (lambda pct, note: report("download", pct, note)) if progress else None
        ))
        if not audio:
            # Phân biệt rõ 2 tình huống để Đại biết đường xử lý
            if not result.title:
                result.error = ("Không mở được video này. Kiểm tra lại 3 điều: "
                                "(1) video có bị xoá hoặc để ở chế độ riêng tư không, "
                                "(2) link đã copy đủ chưa (phần sau dấu =), "
                                "(3) video có bị chặn theo khu vực không.")
            else:
                result.error = ("Không tải được phần tiếng của video. Video có thể "
                                "bị giới hạn độ tuổi hoặc chặn theo khu vực.")
            return result

        lyrics, lang = transcribe_audio(
            audio, workdir, log=log,
            progress=((lambda pct, note: report("transcribe", pct, note))
                      if progress else None),
        )
        if not lyrics.strip():
            result.error = "Đã nghe nhưng không nhận ra lời nào (video có thể chỉ có nhạc không lời)."
            return result

        result.ok = True
        result.lyrics = lyrics
        result.source = "whisper"
        result.detected_language = lang
        result.warnings.append(
            f"Lời do AI tự nghe và chép lại (ngôn ngữ: {lang or 'không xác định'}). "
            "Có thể sai vài chữ, đặc biệt là tên riêng hoặc từ chuyên ngành."
        )
        return result

    except Exception as exc:  # noqa: BLE001
        result.error = f"Lỗi khi xử lý: {type(exc).__name__}: {exc}"
        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    # Cho phép chạy nhanh từ dòng lệnh: python core.py <link>
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--whisper", action="store_true", help="Bỏ qua phụ đề, dùng nhận dạng giọng nói")
    args = ap.parse_args()
    res = get_lyrics(args.url, force_whisper=args.whisper, log=lambda m: print(m, flush=True))
    print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
