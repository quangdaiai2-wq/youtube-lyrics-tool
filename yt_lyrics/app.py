"""
app.py - Web app trích xuất lyrics YouTube và phân tích bằng AI.

Chạy:  python app.py     (rồi mở http://127.0.0.1:5000 trên trình duyệt)
"""

from __future__ import annotations

import json
import queue
import threading
import uuid

from flask import Flask, Response, jsonify, render_template, request

from core import get_lyrics
from analyzer import (ANALYSIS_SECTIONS, analyze_with_api, build_prompt,
                      build_translate_prompt, fetch_models, get_api_config,
                      has_api_key, list_models, set_model, strip_timestamps,
                      to_paragraph, translate_with_api)

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

# Lưu tiến trình theo từng phiên xử lý: {job_id: queue.Queue}
_jobs: dict[str, queue.Queue] = {}


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


@app.route("/api/extract/stream")
def api_extract_stream():
    """
    Trích xuất kèm tiến trình hiển thị dần (Server-Sent Events).
    Đại sẽ thấy từng bước đang chạy thay vì màn hình đứng im.
    """
    url = request.args.get("url", "").strip()
    force_whisper = request.args.get("whisper", "0") == "1"
    job_id = uuid.uuid4().hex
    q: queue.Queue = queue.Queue()
    _jobs[job_id] = q

    def worker() -> None:
        try:
            res = get_lyrics(
                url, force_whisper=force_whisper,
                log=lambda m: q.put({"type": "log", "message": m}),
                progress=lambda stage, pct, note: q.put({
                    "type": "progress", "stage": stage,
                    "percent": round(pct, 1), "note": note
                }),
            )
            q.put({"type": "result", "data": res.to_dict()})
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


if __name__ == "__main__":
    print("=" * 60)
    print("  TOOL TRICH XUAT LYRICS YOUTUBE + PHAN TICH AI")
    print("=" * 60)
    print("  Mo trinh duyet va vao dia chi:  http://127.0.0.1:5000")
    print("  De dung: nhan Ctrl + C tai cua so nay.")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
