"""
analyzer.py - Đưa lyrics cho AI đọc và phân tích.

Hai chế độ:
  A) Chế độ API key  — cần OPENAI_API_KEY trong file .env. Gọi trực tiếp, trả kết quả ngay.
  B) Chế độ prompt   — không cần API key. Sinh ra một "đề bài" hoàn chỉnh để
                       Đại copy sang WorkBuddy/ChatGPT/Claude và dán kết quả về.
"""

from __future__ import annotations

import json
import os
import re

# ---------------------------------------------------------------------------
# Khung phân tích — dùng chung cho cả 2 chế độ
# ---------------------------------------------------------------------------

ANALYSIS_SECTIONS = [
    ("tom_tat", "Tóm tắt nội dung"),
    ("chu_de", "Chủ đề chính"),
    ("cam_xuc", "Cảm xúc chủ đạo"),
    ("thong_diep", "Thông điệp / ý nghĩa"),
    ("cau_truc", "Cấu trúc bài hát"),
    ("ngon_tu", "Phân tích ngôn từ & hình ảnh"),
    ("diem_nhan", "Câu hát đắt giá nhất"),
    ("danh_gia", "Đánh giá tổng thể"),
]

_SYSTEM_PROMPT = (
    "Bạn là chuyên gia phân tích ca từ âm nhạc, có kiến thức văn học và văn hóa. "
    "Phân tích khách quan, dựa trên chính văn bản lời bài hát được cung cấp, "
    "không bịa thêm thông tin về tác giả hay hoàn cảnh sáng tác nếu không có trong dữ liệu. "
    "Trả lời bằng tiếng Việt, trình bày rõ ràng theo từng mục."
)


def build_prompt(title: str = "", channel: str = "", lyrics: str = "") -> str:
    """
    Sinh ra đoạn "đề bài" hoàn chỉnh để dán vào bất kỳ AI nào.
    Đây là nội dung quan trọng nhất của chế độ B.
    """
    header = "PHÂN TÍCH LỜI BÀI HÁT"
    meta_lines = []
    if title:
        meta_lines.append(f"- Tên bài/video: {title}")
    if channel:
        meta_lines.append(f"- Kênh: {channel}")
    meta = "\n".join(meta_lines)

    sections = "\n".join(f"{i+1}. **{label}**: ..." for i, (_, label) in enumerate(ANALYSIS_SECTIONS))

    return f"""{header}
{meta}

Dưới đây là lời bài hát cần phân tích:

---BẮT ĐẦU LỜI BÀI HÁT---
{lyrics}
---KẾT THÚC LỜI BÀI HÁT---

Hãy phân tích theo đúng các mục sau:

{sections}

Yêu cầu: trả lời bằng tiếng Việt. Mục nào không đủ dữ liệu để kết luận thì ghi rõ "Không đủ dữ liệu", tuyệt đối không suy diễn bịa đặt."""


# ---------------------------------------------------------------------------
# Chế độ A: gọi API trực tiếp
# ---------------------------------------------------------------------------
#
# Hỗ trợ SẴN 3 nhà cung cấp AI (đều dùng chung "chuẩn OpenAI", nên chỉ khác
# địa chỉ và tên model). Đại chỉ cần ghi tên nhà cung cấp vào file .env:
#
#   AI_PROVIDER=openai   -> OpenAI chính chủ (gpt-4o-mini)   [mặc định]
#   AI_PROVIDER=gemini   -> Google Gemini   (gemini-2.5-flash)
#   AI_PROVIDER=nous     -> Nous Portal     (google/gemini-3.7-flash)
#
# ⚠️ Khoá API phải KHỚP với nhà cung cấp đã chọn. Ví dụ khoá Nous Portal
#    (thường bắt đầu bằng "sk-nous-") mà để AI_PROVIDER=openai thì sẽ báo 401.
#
# Không ghi gì thì mặc định là OpenAI.
# ---------------------------------------------------------------------------

PROVIDERS: dict[str, dict[str, str]] = {
    "nous": {
        "label": "Nous Portal",
        # Nous Portal là "cổng" gom model của nhiều hãng: OpenAI, Google,
        # Anthropic, DeepSeek, Qwen... (hơn 400 model). Tên model phải ghi
        # kèm tên hãng, ví dụ "google/gemini-3.7-flash".
        # ⚠️ Các model "Hermes-4-70B" cũ đã bị Nous RETIRED (ngừng phục vụ).
        # Nếu tên model dưới đây bị lỗi 404, Đại đổi sang tên khác hoặc hỏi Trợ lý.
        "base": "https://inference-api.nousresearch.com/v1",
        "model": "google/gemini-3.7-flash",
        "ten": "Nous Research",
        # Nhận diện khoá của dịch vụ này để cảnh báo khi chọn nhầm dịch vụ.
        "key_prefixes": ("sk-nous-",),
    },
    "gemini": {
        "label": "Google Gemini",
        "base": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.5-flash",
        "ten": "Google Gemini",
        "key_prefixes": ("AIza",),          # khoá Google AI Studio hay bắt đầu bằng AIza
    },
    "openai": {
        "label": "OpenAI",
        "base": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "ten": "OpenAI",
        "key_prefixes": ("sk-proj-", "sk-"),
    },
}

DEFAULT_PROVIDER = "openai"

# Danh sách model gợi ý sẵn cho từng dịch vụ.
#
# Vì sao cần: tên model AI hết hạn rất nhanh (model Hermes cũ của Nous đã bị
# ngừng phục vụ). Đại không phải nhớ tên — chỉ cần bấm chọn từ danh sách này.
# Vẫn luôn có thể gõ tay tên khác, hoặc nhấn "Tải danh sách model" để lấy
# danh sách THẬT từ dịch vụ (xem `fetch_models`).
MODEL_PRESETS: dict[str, list[str]] = {
    "nous": [
        "google/gemini-3.7-flash",
        "google/gemini-3.8-flash",
        "google/gemini-3.1-pro-preview",
        "openai/gpt-5.6-luna",
        "anthropic/claude-sonnet-5.5",
        "deepseek/deepseek-v4.1-flash",
        "moonshotai/kimi-k3",
        "qwen/qwen3.8-max-prime",
    ],
    "gemini": [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ],
    "openai": [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4.1-mini",
        "gpt-4.1",
    ],
}


def list_models(provider: str | None = None) -> dict:
    """
    Trả về danh sách model gợi ý sẵn + model đang dùng cho một dịch vụ.

    Đây là danh sách "gợi ý", không cần gọi mạng. Muốn danh sách thật đầy đủ
    thì dùng `fetch_models()`.
    """
    name = (provider or get_provider()).strip().lower()
    if name not in PROVIDERS:
        name = get_provider()
    cfg = get_api_config()
    current = cfg["model"] if cfg["provider"] == name else PROVIDERS[name]["model"]
    presets = list(MODEL_PRESETS.get(name, []))
    # Nếu model đang dùng chưa có trong danh sách gợi ý thì chèn lên đầu
    if current and current not in presets:
        presets.insert(0, current)
    return {"provider": name, "label": PROVIDERS[name]["label"],
            "current": current, "models": presets}


def fetch_models(provider: str | None = None, timeout: int = 30) -> dict:
    """
    Lấy danh sách model THẬT từ dịch vụ (gọi GET /models).

    Dùng khi Đại muốn xem đầy đủ các model mà khoá của mình được phép dùng.
    Trả về {"ok", "models": [...], "error": str}.
    """
    name = (provider or get_provider()).strip().lower()
    if name not in PROVIDERS:
        return {"ok": False, "models": [], "error": f"Dịch vụ '{name}' không hợp lệ."}

    cfg = get_api_config()
    if not cfg["key"]:
        return {"ok": False, "models": [],
                "error": "Chưa có khoá API. Xem mục 7 trong HUONG-DAN.md."}

    url = cfg["base"].rstrip("/") + "/models"
    try:
        import requests
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {cfg['key']}"},
            timeout=timeout,
        )
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "models": [],
                "error": f"Không kết nối được tới {cfg['label']}: {e}"}

    if resp.status_code != 200:
        return {"ok": False, "models": [],
                "error": (f"{cfg['label']} trả mã {resp.status_code}. "
                          f"Chưa lấy được danh sách model.")}

    try:
        data = resp.json()
    except Exception:  # noqa: BLE001
        return {"ok": False, "models": [], "error": "Dịch vụ trả về dữ liệu lạ."}

    items = data.get("data") if isinstance(data, dict) else data
    ids: list[str] = []
    if isinstance(items, list):
        for it in items:
            if isinstance(it, dict) and it.get("id"):
                ids.append(str(it["id"]))
            elif isinstance(it, str):
                ids.append(it)
    ids = sorted(set(ids))
    return {"ok": True, "provider": name, "count": len(ids),
            "current": cfg["model"], "models": ids}


def get_provider() -> str:
    """Đọc tên nhà cung cấp từ .env. Tên lạ thì quay về mặc định."""
    name = (_os_env("AI_PROVIDER") or DEFAULT_PROVIDER).strip().lower()
    return name if name in PROVIDERS else DEFAULT_PROVIDER


def _os_env(name: str, default: str = "") -> str:
    """
    Đọc biến cấu hình theo thứ tự: giá trị trong .env trước, rồi tới biến
    môi trường sẵn có, cuối cùng là giá trị mặc định.

    Vì sao cần hàm này thay vì đọc thẳng os.environ: `_load_env()` nạp .env
    vào một bộ nhớ riêng thay vì ghi đè os.environ, nhờ vậy vẫn có thể đổi
    cấu hình tạm thời từ bên ngoài khi cần.
    """
    _load_env()
    from_file = _ENV_FILE_CACHE.get(name)
    if from_file not in (None, ""):
        return from_file
    return os.environ.get(name, default)


def get_api_config() -> dict:
    """
    Gom toàn bộ cấu hình API vào một chỗ: khoá, địa chỉ, model, tên hiển thị.

    Cho phép ghi đè từng phần bằng .env nếu Đại muốn dùng dịch vụ khác
    hoặc model khác với mặc định của nhà cung cấp.
    """
    name = get_provider()
    preset = PROVIDERS[name]

    base = (_os_env("OPENAI_BASE_URL") or preset["base"]).strip().rstrip("/")
    model = (_os_env("AI_MODEL") or preset["model"]).strip()

    return {
        "provider": name,
        "label": preset["label"],
        "ten": preset["ten"],
        # Nhận cả 3 tên biến cho tiện: dùng tên nào cũng được
        "key": (_os_env("OPENAI_API_KEY")
                or _os_env("AI_API_KEY")
                or _os_env("GEMINI_API_KEY")
                or "").strip(),
        "base": base,
        "model": model,
    }


def has_api_key() -> bool:
    return bool(get_api_config()["key"])


def set_model(model: str, provider: str | None = None) -> dict:
    """
    Ghi model mới (và dịch vụ, nếu có) vào file .env, để lần sau mở tool
    là dùng luôn.

    Đại không cần tự sửa file — bấm chọn trên giao diện là hàm này lo.
    Trả về {"ok": bool, "error": str, "provider", "model"}.
    """
    model = (model or "").strip()
    if not model:
        return {"ok": False, "error": "Chưa chọn model nào."}

    provider = (provider or get_provider()).strip().lower()
    if provider not in PROVIDERS:
        return {"ok": False, "error": f"Dịch vụ '{provider}' không hợp lệ."}

    try:
        path = _env_path()
        lines = _read_env_lines(path)
        lines = _upsert_env_line(lines, "AI_PROVIDER", provider)
        lines = _upsert_env_line(lines, "AI_MODEL", model)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"Không ghi được file .env: {e}"}

    # Nạp lại để lần gọi sau dùng giá trị mới ngay, không cần bật lại tool
    _ENV_FILE_CACHE.clear()
    _load_env()

    return {"ok": True, "error": "", "provider": provider, "model": model}


def _env_path() -> str:
    """Đường dẫn file .env ở thư mục gốc dự án."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, ".env")


def _read_env_lines(path: str) -> list[str]:
    """Đọc .env thành danh sách dòng. Chưa có file thì trả về danh sách rỗng."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def _upsert_env_line(lines: list[str], key: str, value: str) -> list[str]:
    """
    Thay dòng `key=...` nếu đã có, hoặc thêm dòng mới ở cuối nếu chưa có.

    Bỏ qua dòng bị chú thích (bắt đầu bằng #) để không sửa nhầm phần ghi chú.
    """
    new_line = f'{key}="{value}"'
    out: list[str] = []
    found = False
    for ln in lines:
        stripped = ln.strip()
        if not found and stripped and not stripped.startswith("#"):
            head = stripped.split("=", 1)[0].strip()
            if head == key:
                out.append(new_line)
                found = True
                continue
        out.append(ln)
    if not found:
        if out and out[-1].strip():
            out.append("")
        out.append(new_line)
    return out


# Nội dung file .env được đọc vào đây. Dùng dict riêng thay vì nhồi thẳng vào
# os.environ, để không "nuốt" mất giá trị do người chạy đặt từ bên ngoài.
_ENV_FILE_CACHE: dict[str, str] = {}


def _load_env() -> None:
    """
    Đọc file .env ở thư mục gốc dự án và lưu vào _ENV_FILE_CACHE.

    Ưu tiên giá trị trong .env hơn biến môi trường sẵn có (để Đại sửa file là
    có tác dụng ngay), nhưng KHÔNG ghi đè os.environ — nhờ vậy vẫn có thể
    đổi cấu hình tạm thời từ bên ngoài khi cần.
    """
    try:
        from dotenv import dotenv_values  # type: ignore
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, ".env")
        if os.path.exists(path):
            for k, v in dotenv_values(path).items():
                if v is not None:
                    _ENV_FILE_CACHE[k] = v.strip().strip('"').strip("'")
    except Exception:  # noqa: BLE001
        pass


def _detect_key_mismatch(cfg: dict) -> str:
    """
    Phát hiện trường hợp khoá API không thuộc dịch vụ đã chọn.

    Đây là lỗi rất dễ gặp: Đại dán khoá Nous nhưng để AI_PROVIDER=openai,
    rồi nhận thông báo 401 khó hiểu ("Incorrect API key provided") mà không
    biết vì sao. Hàm này nhìn vào TIỀN TỐ của khoá để cảnh báo sớm, rõ ràng.

    Trả về chuỗi cảnh báo, hoặc "" nếu không phát hiện vấn đề.
    """
    key = cfg["key"]
    if not key:
        return ""

    low = key.lower()

    # Khoá Nous Portal: bắt đầu bằng "sk-nous-"
    if low.startswith("sk-nous-"):
        if cfg["provider"] != "nous":
            return (
                f"Khoá API của Đại là khoá **Nous Portal** (bắt đầu bằng "
                f"`sk-nous-...`), nhưng tool đang được đặt để gọi "
                f"**{cfg['label']}**.\n\n"
                f"→ Cách sửa: mở file `.env`, đổi dòng đầu thành:\n"
                f"    AI_PROVIDER=nous\n"
                f"rồi lưu (Ctrl+S) và bật lại tool."
            )
        return ""

    # Khoá Google AI Studio: bắt đầu bằng "AIza"
    if low.startswith("aiza") and cfg["provider"] != "gemini":
        return (
            f"Khoá API của Đại là khoá **Google/Gemini** (bắt đầu bằng "
            f"`AIza...`), nhưng tool đang được đặt để gọi **{cfg['label']}**.\n\n"
            f"→ Cách sửa: mở file `.env`, đổi dòng đầu thành:\n"
            f"    AI_PROVIDER=gemini\n"
            f"rồi lưu (Ctrl+S) và bật lại tool."
        )

    return ""


def _call_chat(cfg: dict, system: str, user: str, temperature: float,
               timeout: int = 180) -> dict:
    """
    Gọi một lần tới API theo chuẩn OpenAI. Dùng chung cho cả phân tích và dịch.

    Trả về {"ok", "text", "error"}. Thông báo lỗi được viết lại cho dễ hiểu,
    kèm tên nhà cung cấp để Đại biết đang gọi dịch vụ nào.
    """
    try:
        import requests
    except ImportError:
        return {"ok": False, "text": "", "error": "Thiếu thư viện requests."}

    # Cảnh báo khi khoá API không thuộc dịch vụ đã chọn (lỗi rất hay gặp:
    # dán khoá Nous nhưng quên đổi AI_PROVIDER, khiến báo 401 khó hiểu).
    mismatch = _detect_key_mismatch(cfg)
    if mismatch:
        return {"ok": False, "text": "", "error": mismatch}

    url = f"{cfg['base']}/chat/completions"
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {cfg['key']}",
                     "Content-Type": "application/json"},
            json={
                "model": cfg["model"],
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": temperature,
            },
            timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "text": "",
                "error": (f"Không kết nối được tới {cfg['ten']}. "
                          f"Kiểm tra mạng, hoặc địa chỉ API trong file .env. "
                          f"(Chi tiết: {exc})")}

    if resp.status_code != 200:
        hint = ""
        if resp.status_code in (401, 403):
            hint = (f" → Khoá API bị từ chối. Kiểm tra lại khoá của {cfg['ten']} "
                    f"trong file .env, hoặc xem khoá còn hạn / còn tiền không.")
        elif resp.status_code == 404:
            hint = (f" → Không tìm thấy model '{cfg['model']}' ở {cfg['ten']}. "
                    f"Tên model trong file .env có thể bị sai, hoặc model đã bị "
                    f"ngừng phục vụ. Đại thử xoá dòng AI_MODEL, hoặc hỏi Trợ lý.")
        elif resp.status_code == 429:
            hint = (f" → {cfg['ten']} báo quá nhiều yêu cầu hoặc hết hạn mức. "
                    f"Đợi một lát rồi thử lại.")
        elif resp.status_code == 400:
            hint = (f" → {cfg['ten']} không chấp nhận yêu cầu. Thường do: khoá API "
                    f"sai/không đúng định dạng, tên model sai, hoặc tài khoản chưa "
                    f"được cấp quyền. Kiểm tra lại khoá và dòng AI_MODEL trong .env.")
        return {"ok": False, "text": "",
                "error": (f"{cfg['ten']} trả lỗi {resp.status_code}.{hint}\n"
                          f"(Nội dung gốc: {resp.text[:300]})")}

    try:
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        if not text or not str(text).strip():
            return {"ok": False, "text": "",
                    "error": f"{cfg['ten']} trả về nội dung rỗng. Thử lại giúp Đại."}
        return {"ok": True, "text": text, "error": ""}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "text": "",
                "error": f"Không đọc được kết quả từ {cfg['ten']}: {exc}"}


def analyze_with_api(title: str, channel: str, lyrics: str,
                     model: str | None = None) -> dict:
    """
    Gọi API để phân tích. Trả về {"ok": bool, "text": str, "error": str}.
    """
    cfg = get_api_config()
    if not cfg["key"]:
        return {"ok": False, "text": "",
                "error": ("Chưa cấu hình khoá API. Đại xem mục 7 trong HUONG-DAN.md, "
                          "hoặc dùng chế độ 'Tạo đề bài' để copy sang WorkBuddy.")}
    if model:
        cfg["model"] = model

    prompt = build_prompt(title, channel, lyrics)
    return _call_chat(cfg, _SYSTEM_PROMPT, prompt, temperature=0.7)


def translate_with_api(lyrics: str, source_lang: str = "",
                       target: str = "tiếng Việt",
                       model: str | None = None) -> dict:
    """
    Dịch lời bài hát bằng cách gọi API. Trả về {"ok", "text", "error"}.

    Vì sao cần API: máy nghe sẵn có trong tool chỉ dịch được sang TIẾNG ANH.
    Muốn dịch sang tiếng Việt phải dùng AI dịch thật.
    """
    cfg = get_api_config()
    if not cfg["key"]:
        return {"ok": False, "text": "",
                "error": ("Chưa có khoá API. Đại xem mục 7 trong HUONG-DAN.md để gắn khoá, "
                          "hoặc dùng nút 'Tạo đề bài dịch' (miễn phí, không cần khoá).")}
    if model:
        cfg["model"] = model

    prompt = build_translate_prompt(lyrics, source_lang, target)
    system = ("Bạn là dịch giả chuyên nghiệp, dịch ca từ âm nhạc. "
              "Dịch thoát ý, đọc tự nhiên như lời Việt, giữ đúng sắc thái cảm xúc. "
              "Chỉ trả về bản dịch, không thêm lời bình.")
    return _call_chat(cfg, system, prompt, temperature=0.3)


def strip_timestamps(lyrics: str) -> str:
    """Bỏ mốc thời gian [0:12] để lời sạch hơn khi đưa cho AI.

    Lưu ý: phải bỏ TẤT CẢ mốc trên dòng (một dòng có thể chứa nhiều mốc, và
    mốc có thể nằm giữa dòng), không chỉ mốc ở đầu dòng. Mốc cũng có thể có
    phần thập phân dạng [01:02.500].

    Giữ nguyên đặc điểm riêng của hàm này so với `to_paragraph`: mỗi dòng đầu
    vào vẫn là một dòng đầu ra (không gộp lại thành đoạn văn).
    """
    lines = []
    for line in lyrics.splitlines():
        s = re.sub(r"\[\d+:\d{2}(?::\d{2})?(?:\.\d+)?\]", " ", line)
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            lines.append(s)
    return "\n".join(lines)


def to_paragraph(lyrics: str, sentences_per_para: int = 5) -> str:
    """
    Chuyển lời bài hát thành các đoạn văn liền mạch, bỏ mốc thời gian.

    Vì sao cần: lời lấy từ nhận dạng giọng nói có mốc thời gian ở đầu mỗi dòng
    như "[10:22] with additional third-party tools." — nhìn rối và phải xoá thủ
    công mới dùng được. Hàm này gộp lại thành đoạn văn đọc liền.

    Không gộp tất cả thành 1 khối duy nhất: lời nhận dạng tự động thường thiếu
    dấu câu, gộp hết sẽ thành một đoạn khổng lồ rất khó đọc. Thay vào đó chia
    thành đoạn khoảng `sentences_per_para` câu.
    """
    # Bỏ mốc thời gian, giữ phần chữ.
    # Lưu ý: phải bỏ TẤT CẢ mốc trên dòng (có thể có nhiều mốc cùng dòng),
    # không chỉ mốc ở đầu dòng.
    parts: list[str] = []
    for line in lyrics.splitlines():
        s = re.sub(r"\[\d+:\d{2}(?::\d{2})?(?:\.\d+)?\]", " ", line)   # bỏ mọi mốc
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            parts.append(s)

    if not parts:
        return ""

    # Nếu lời đã có dấu câu thì cắt theo dấu câu cho tự nhiên
    joined = " ".join(parts)
    joined = re.sub(r"\s+", " ", joined).strip()

    # Tách thành câu dựa trên dấu . ! ? ; còn nếu không có thì dựa theo dòng gốc
    if re.search(r"[.!?]", joined):
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", joined) if s.strip()]
    else:
        sentences = parts

    # Nhóm thành các đoạn
    paragraphs: list[str] = []
    for i in range(0, len(sentences), sentences_per_para):
        chunk = sentences[i:i + sentences_per_para]
        text = " ".join(chunk).strip()
        if text and not text[-1] in ".!?…":
            text += "."          # thêm dấu chấm cuối đoạn nếu thiếu
        paragraphs.append(text)

    return "\n\n".join(paragraphs)


def build_translate_prompt(text: str, source_lang: str = "",
                           target: str = "tiếng Việt") -> str:
    """
    Sinh đề bài dịch để Đại copy sang WorkBuddy/ChatGPT.

    Dùng cho trường hợp máy nghe sẵn có không dịch được (nó chỉ dịch sang tiếng Anh),
    hoặc khi cần bản dịch chất lượng cao hơn.
    """
    src = f" (ngôn ngữ gốc: {source_lang})" if source_lang else ""
    clean = strip_timestamps(text)

    return f"""DỊCH LỜI BÀI HÁT SANG {target.upper()}

Dưới đây là lời bài hát cần dịch{src}:

---BẮT ĐẦU---
{clean}
---KẾT THÚC---

Yêu cầu:
1. Dịch toàn bộ sang {target}, giữ nguyên ý nghĩa và sắc thái cảm xúc.
2. Với ca từ, ưu tiên bản dịch ĐỌC HAY và tự nhiên như lời Việt, không dịch cứng theo từng chữ.
3. Giữ nguyên tên riêng, tên nghệ sĩ, tên bài hát.
4. Trình bày thành các đoạn văn liền mạch, KHÔNG kèm mốc thời gian.
5. Đặt phần dịch trong khối rõ ràng, không thêm lời bình nếu không được yêu cầu."""


def build_translate_back_prompt(translated: str) -> str:
    """Đề bài kiểm tra chéo: dịch ngược bản dịch về ngôn ngữ gốc để đối chiếu."""
    return f"""DỊCH NGƯỢC ĐỂ KIỂM TRA

Dưới đây là một bản dịch lời bài hát. Hãy dịch ngược lại về ngôn ngữ gốc
và cho biết bản dịch có chỗ nào sai lệch ý nghĩa so với bản gốc không.

---BẮT ĐẦU---
{translated}
---KẾT THÚC---

Trả lời gồm 2 phần:
1. Bản dịch ngược về ngôn ngữ gốc.
2. Nhận xét: chỗ nào dịch chưa sát nghĩa, chỗ nào nên sửa lại cho đúng hơn.

Trả lời bằng tiếng Việt."""


if __name__ == "__main__":
    cfg = get_api_config()
    print(json.dumps({
        "co_api_key": has_api_key(),
        "nha_cung_cap": cfg["label"],
        "dia_chi_api": cfg["base"],
        "model_dang_dung": cfg["model"],
        "cac_muc_phan_tich": [lbl for _, lbl in ANALYSIS_SECTIONS],
    }, ensure_ascii=False, indent=2))
