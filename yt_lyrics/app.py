"""
app.py - Web app trích xuất lyrics YouTube và phân tích bằng AI.

Chạy:  python app.py     (rồi mở http://127.0.0.1:5000 trên trình duyệt)

Hai nguồn lấy lời:
  - Link YouTube  -> /api/extract/stream
  - File trong máy -> /api/upload (gửi file lên) rồi /api/extract/local/stream,
                      hoặc dán thẳng đường dẫn file.
"""

from __future__ import annotations

import json
import os
import queue
import re
import shutil
import socket
import sys
import tempfile
import threading
import time
import uuid
import webbrowser
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request

from core import get_lyrics, get_lyrics_from_file
from analyzer import (ANALYSIS_SECTIONS, analyze_with_api, build_prompt,
                      build_translate_prompt, fetch_models, get_api_config,
                      has_api_key, list_models, set_model, strip_timestamps,
                      to_paragraph, translate_with_api)

# ---------------------------------------------------------------------------
# Chạy ẩn (không có cửa sổ đen)
# ---------------------------------------------------------------------------
# Khi Đại mở tool bằng file chạy ẩn, Python không có màn hình để in thông báo.
# Lúc đó sys.stdout / sys.stderr là None, và mọi lệnh print sẽ gây lỗi.
# Nên ta chuyển hết thông báo vào file tool.log để còn xem lại khi cần.
LOG_FILE = Path(__file__).with_name("tool.log")

if sys.stdout is None or sys.stderr is None:
    try:
        _log_handle = open(LOG_FILE, "a", encoding="utf-8", buffering=1)
        sys.stdout = sys.stdout or _log_handle
        sys.stderr = sys.stderr or _log_handle
        print(f"\n===== Mở tool lúc {time.strftime('%d/%m/%Y %H:%M:%S')} =====")
    except Exception:  # noqa: BLE001
        pass


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
# Cho phép gửi file video lớn: không đặt giới hạn kích thước.
app.config["MAX_CONTENT_LENGTH"] = None

# Lưu tiến trình theo từng phiên xử lý: {job_id: queue.Queue}
_jobs: dict[str, queue.Queue] = {}

# File Đại gửi lên từ trình duyệt: {token: {"dir": ..., "path": ..., "name": ...}}
# File nằm trong thư mục tạm và bị xoá ngay sau khi nghe xong.
_uploads: dict[str, dict] = {}


def _cleanup_old_uploads() -> None:
    """
    Dọn các thư mục file tạm còn sót lại từ lần chạy trước.

    Chỉ đụng vào thư mục có tiền tố do chính tool tạo, không ảnh hưởng gì khác.
    """
    root = Path(tempfile.gettempdir())
    for d in root.glob("ytlyrics_up_*"):
        if d.is_dir():
            shutil.rmtree(d, ignore_errors=True)


def _safe_name(name: str) -> str:
    """
    Làm sạch tên file Đại gửi lên: bỏ đường dẫn, bỏ ký tự cấm của Windows,
    nhưng GIỮ tiếng Việt để tiêu đề hiển thị vẫn đọc được.
    """
    base = Path(name or "file").name
    base = re.sub(r'[\\/:*?"<>|]+', "_", base).strip(" .") or "file"
    return base


@app.route("/")
def index():
    cfg = get_api_config()
    return render_template("index.html",
                           sections=[lbl for _, lbl in ANALYSIS_SECTIONS],
                           co_api_key=has_api_key(),
                           nha_cung_cap=cfg["label"],
                           ten_model=cfg["model"])


@app.route("/api/lyrics")
def api_lyrics():
    """Trả về kết quả trích xuất lyrics dạng JSON đơn giản (không streaming)."""
    url = request.args.get("url", "").strip()
    force_whisper = request.args.get("whisper", "0") == "1"
    if not url:
        return jsonify({"ok": False, "error": "Chưa có link YouTube."}), 400

    logs: list[str] = []
    res = get_lyrics(url, force_whisper=force_whisper,
                     log=lambda m: logs.append(m))
    data = res.to_dict()
    data["logs"] = logs
    return jsonify(data)


def _sse_stream(run_job) -> Response:
    """
    Bọc một việc xử lý lâu thành luồng báo tiến trình (SSE), để Đại thấy
    từng bước đang chạy thay vì màn hình đứng im.

    run_job: hàm nhận vào một hàm `emit(payload)` để đẩy sự kiện ra ngoài.
    """
    job_id = uuid.uuid4().hex
    q: queue.Queue = queue.Queue()
    _jobs[job_id] = q

    def worker() -> None:
        def emit(payload: dict) -> None:
            q.put(payload)

        try:
            run_job(emit)
        except Exception as exc:  # noqa: BLE001
            q.put({"type": "result",
                   "data": {"ok": False, "error": f"{type(exc).__name__}: {exc}"}})
        finally:
            q.put(None)  # dấu kết thúc

    threading.Thread(target=worker, daemon=True).start()

    def stream():
        yield f"data: {json.dumps({'type': 'job', 'job_id': job_id})}\n\n"
        while True:
            try:
                item = q.get(timeout=300)
            except queue.Empty:
                break
            if item is None:
                break
            yield f"data: {json.dumps(item, ensure_ascii=False)}\n\n"
        _jobs.pop(job_id, None)
        yield "event: end\ndata: {}\n\n"

    return Response(stream(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no"})


@app.route("/api/extract/stream")
def api_extract_stream():
    """Trích xuất lời từ link YouTube, kèm tiến trình hiển thị dần."""
    url = request.args.get("url", "").strip()
    force_whisper = request.args.get("whisper", "0") == "1"

    def job(emit) -> None:
        res = get_lyrics(
            url, force_whisper=force_whisper,
            log=lambda m: emit({"type": "log", "message": m}),
            progress=lambda stage, pct, note: emit({
                "type": "progress", "stage": stage,
                "percent": round(pct, 1), "note": note}),
        )
        emit({"type": "result", "data": res.to_dict()})

    return _sse_stream(job)


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """
    Nhận file Đại chọn từ trình duyệt, lưu vào thư mục tạm và trả về mã phiên.

    Trình duyệt vì lý do bảo mật không cho biết đường dẫn thật của file, nên
    muốn dùng nút "Chọn file" thì phải gửi file lên. File được xoá ngay sau
    khi nghe xong (xem api_extract_local_stream).
    """
    f = request.files.get("file")
    if f is None or not (f.filename or "").strip():
        return jsonify({"ok": False, "error": "Chưa có file nào được chọn."}), 400

    tmp_dir = Path(tempfile.mkdtemp(prefix="ytlyrics_up_"))
    name = _safe_name(f.filename)
    dest = tmp_dir / name
    try:
        f.save(str(dest))
    except Exception as exc:  # noqa: BLE001
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return jsonify({"ok": False,
                        "error": f"Không lưu được file: {type(exc).__name__}: {exc}"}), 500

    size_mb = dest.stat().st_size / 1_048_576
    if size_mb <= 0:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return jsonify({"ok": False, "error": "File rỗng, không có gì để đọc."}), 400

    token = uuid.uuid4().hex
    _uploads[token] = {"dir": str(tmp_dir), "path": str(dest), "name": name}
    return jsonify({"ok": True, "token": token, "name": name,
                    "size_mb": round(size_mb, 1)})


@app.route("/api/extract/local/stream")
def api_extract_local_stream():
    """
    Trích xuất lời từ file có sẵn trong máy, kèm tiến trình hiển thị dần.

    Hai cách chọn file:
      - ?token=...  file Đại gửi lên ở /api/upload (tự xoá sau khi xong)
      - ?path=...   đường dẫn file có sẵn trên máy (đọc thẳng, không copy, không xoá)
    """
    token = request.args.get("token", "").strip()
    raw_path = request.args.get("path", "").strip()

    info = _uploads.pop(token, None) if token else None
    if token and not info:
        return jsonify({"ok": False,
                        "error": "File gửi lên không còn nữa, Đại chọn lại file giúp."}), 400
    if not info and not raw_path:
        return jsonify({"ok": False,
                        "error": "Chưa có file. Đại chọn file hoặc dán đường dẫn vào ô."}), 400

    target = info["path"] if info else raw_path
    display_name = info["name"] if info else ""
    tmp_dir = info["dir"] if info else ""

    def job(emit) -> None:
        try:
            res = get_lyrics_from_file(
                target,
                log=lambda m: emit({"type": "log", "message": m}),
                progress=lambda stage, pct, note: emit({
                    "type": "progress", "stage": stage,
                    "percent": round(pct, 1), "note": note}),
            )
            data = res.to_dict()
            # Hiện tiêu đề đúng tên file Đại đã chọn (bản lưu tạm có thể bị đổi tên)
            if display_name:
                data["title"] = Path(display_name).stem
            emit({"type": "result", "data": data})
        finally:
            if tmp_dir:
                shutil.rmtree(tmp_dir, ignore_errors=True)

    return _sse_stream(job)


@app.route("/api/models")
def api_models():
    """
    Danh sách model gợi ý sẵn cho một dịch vụ (đọc từ bảng có trong code).

    Tham số tuỳ chọn: ?provider=nous|gemini|openai
    Đây là danh sách nhẹ, không gọi mạng.
    """
    provider = request.args.get("provider", "").strip() or None
    return jsonify(list_models(provider))


@app.route("/api/models/live")
def api_models_live():
    """
    Lấy danh sách model THẬT từ dịch vụ (gọi GET /models).

    Chậm hơn `/api/models` vì phải gọi ra mạng, nhưng cho biết đầy đủ những
    model mà khoá của Đại dùng được.
    """
    provider = request.args.get("provider", "").strip() or None
    return jsonify(fetch_models(provider))


@app.route("/api/model", methods=["POST"])
def api_set_model():
    """
    Lưu model mới (và dịch vụ) vào .env để lần sau mở tool dùng luôn.

    Body JSON: {"model": "...", "provider": "nous"} (provider không bắt buộc)
    """
    body = request.get_json(force=True, silent=True) or {}
    model = (body.get("model") or "").strip()
    provider = (body.get("provider") or "").strip() or None
    result = set_model(model, provider)
    return jsonify(result), (200 if result.get("ok") else 400)


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """Phân tích lyrics: hoặc gọi API, hoặc trả về đề bài để copy."""
    body = request.get_json(force=True, silent=True) or {}
    lyrics = (body.get("lyrics") or "").strip()
    title = body.get("title", "")
    channel = body.get("channel", "")
    mode = body.get("mode", "prompt")

    if not lyrics:
        return jsonify({"ok": False, "error": "Chưa có lời bài hát để phân tích."}), 400

    clean = strip_timestamps(lyrics)

    if mode == "api":
        r = analyze_with_api(title, channel, clean)
        return jsonify(r)

    prompt = build_prompt(title, channel, clean)
    return jsonify({"ok": True, "prompt": prompt})


@app.route("/api/translate", methods=["POST"])
def api_translate():
    """
    Dịch lời bài hát.
    - mode="api"    : gọi API dịch luôn (cần khoá API) -> trả bản dịch tiếng Việt.
    - mode="prompt" : sinh đề bài để copy (không cần khoá).
    """
    body = request.get_json(force=True, silent=True) or {}
    lyrics = (body.get("lyrics") or "").strip()
    source_lang = body.get("source_lang", "")
    target = body.get("target") or "tiếng Việt"
    mode = body.get("mode", "prompt")

    if not lyrics:
        return jsonify({"ok": False, "error": "Chưa có lời để dịch."}), 400

    if mode == "api":
        return jsonify(translate_with_api(lyrics, source_lang, target))

    prompt = build_translate_prompt(lyrics, source_lang, target)
    return jsonify({"ok": True, "prompt": prompt})


@app.route("/api/translate/prompt", methods=["POST"])
def api_translate_prompt():
    """Sinh đề bài dịch để Đại copy sang WorkBuddy/ChatGPT (không cần khoá API)."""
    body = request.get_json(force=True, silent=True) or {}
    lyrics = (body.get("lyrics") or "").strip()
    source_lang = body.get("source_lang", "")
    target = body.get("target") or "tiếng Việt"

    if not lyrics:
        return jsonify({"ok": False, "error": "Chưa có lời để dịch."}), 400

    prompt = build_translate_prompt(lyrics, source_lang, target)
    return jsonify({"ok": True, "prompt": prompt})


@app.route("/api/paragraph", methods=["POST"])
def api_paragraph():
    """Chuyển lời có mốc thời gian thành đoạn văn liền mạch."""
    body = request.get_json(force=True, silent=True) or {}
    lyrics = (body.get("lyrics") or "").strip()
    if not lyrics:
        return jsonify({"ok": False, "error": "Chưa có lời."}), 400
    return jsonify({"ok": True, "text": to_paragraph(lyrics)})


@app.route("/api/shutdown", methods=["POST"])
def api_shutdown():
    """
    Tắt tool.

    Cần có vì khi tool chạy ẩn, Đại không còn cửa sổ đen để đóng nữa.

    Yêu cầu phải gửi kèm tiêu đề xác nhận, để một trang web lạ không
    tắt được tool sau lưng Đại.
    """
    if request.headers.get("X-Tool-Action") != "shutdown":
        return jsonify({"ok": False, "error": "Thiếu xác nhận."}), 400

    def tat_sau_khi_tra_loi() -> None:
        time.sleep(0.6)      # chờ câu trả lời tới được trình duyệt
        print(f"===== Tắt tool lúc {time.strftime('%d/%m/%Y %H:%M:%S')} =====")
        os._exit(0)

    threading.Thread(target=tat_sau_khi_tra_loi, daemon=True).start()
    return jsonify({"ok": True})


def _port_dang_dung(port: int = 5000) -> bool:
    """Kiểm tra xem tool đã chạy sẵn ở cổng này chưa."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def _bao_loi_bang_hop_thoai(noi_dung: str) -> None:
    """
    Hiện hộp thoại cảnh báo khi không có cửa sổ đen để in lỗi ra.

    Chỉ dùng được trên Windows; nếu không thì bỏ qua, vì lỗi đã nằm trong tool.log.
    """
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            None, noi_dung, "Tool trích xuất lời bài hát", 0x10
        )
    except Exception:  # noqa: BLE001
        pass


if __name__ == "__main__":
    _cleanup_old_uploads()   # dọn file tạm còn sót từ lần chạy trước

    # Nếu tool đã chạy sẵn (Đại bấm 2 lần), chỉ mở trình duyệt chứ không mở thêm.
    if _port_dang_dung():
        print("Tool đang chạy sẵn — chỉ mở trình duyệt.")
        webbrowser.open("http://127.0.0.1:5000")
        sys.exit(0)

    print("=" * 60)
    print("  TOOL TRICH XUAT LYRICS YOUTUBE + FILE TRONG MAY + PHAN TICH AI")
    print("=" * 60)
    print("  Mo trinh duyet va vao dia chi:  http://127.0.0.1:5000")
    print("  De tat tool: bam nut 'Tat tool' o cuoi trang web.")
    print("=" * 60)

    # Tự mở trình duyệt sau khi máy chủ kịp khởi động
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    try:
        app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
    except OSError as exc:
        # Không có cửa sổ để báo lỗi -> hiện hộp thoại cho Đại biết
        _bao_loi_bang_hop_thoai(
            f"Không bật được tool:\n{exc}\n\n"
            "Có thể một chương trình khác đang dùng cổng 5000.\n"
            "Chi tiết đã ghi vào file yt_lyrics\\tool.log"
        )
        raise
