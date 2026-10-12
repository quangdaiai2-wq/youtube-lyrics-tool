# 🎵 Tool trích xuất lời bài hát + dịch sang tiếng Việt

Dán link YouTube **hoặc** chọn video có sẵn trong máy → tool lấy lời bài hát →
**dịch sang tiếng Việt bằng AI** hoặc cho AI phân tích nội dung.

Chạy hoàn toàn trên máy của bạn. Video YouTube không bị tải về; file trong máy chỉ được đọc tại chỗ.

---

## ✨ Tính năng chính

| Tính năng | Mô tả |
|---|---|
| 🔗 **Lấy lời từ link YouTube** | Tự lấy phụ đề có sẵn; nếu không có thì tải phần tiếng và dùng AI nghe để chép lại |
| 💻 **Lấy lời từ file trong máy** | Dán đường dẫn hoặc chọn file video/audio có sẵn — đọc thẳng file gốc, không copy, không tải gì về |
| 📄 **Đọc thẳng file phụ đề** | Chọn file `.srt` / `.vtt` / `.txt` là ra lời ngay, không cần nghe |
| 🌐 **Dịch sang tiếng Việt** | Dịch từ **bất kỳ ngôn ngữ nào** sang tiếng Việt, chia đoạn sẵn, bấm Copy là dùng |
| 🔀 **Đổi model trên web** | Chọn dịch vụ và model AI ngay trên giao diện — không cần sửa file cấu hình |
| 📄 **Chuyển thành đoạn văn** | Gộp lời rời rạc kèm mốc thời gian thành đoạn văn liền mạch |
| 📊 **Thanh tiến độ %** | Hiển thị tiến trình theo thời gian thực, chia đúng bước cho từng nguồn |
| 🤖 **Phân tích bằng AI** | Phân tích chủ đề, cảm xúc, thông điệp của bài hát |

---

## 🚀 Cách chạy (dành cho người không biết lập trình)

**Bước 1:** Nhấp đúp vào file `CHAY-TOOL.vbs` ở thư mục gốc
→ Tool chạy **ngầm, không hiện cửa sổ đen nào**, trình duyệt tự mở trang `http://127.0.0.1:5000`

**Bước 2:** Chọn nguồn ở Bước 1 rồi bấm **Trích xuất lời**
- Tab **🔗 Link YouTube**: dán link vào ô
- Tab **💻 Video trong máy**: dán đường dẫn file, hoặc bấm **📁 Hoặc chọn file từ máy**

**Bước 3:** Bấm **⚡ Dịch ngay**

**Khi xong việc:** bấm nút **⏻ Tắt tool** ở cuối trang web
→ Tool chạy ngầm nên không có cửa sổ nào để đóng; nút này mới là chỗ tắt.

> 📖 Hướng dẫn chi tiết từng bước: xem file [`yt_lyrics/HUONG-DAN.md`](yt_lyrics/HUONG-DAN.md)

---

## 🔑 Cấu hình khoá API (tuỳ chọn)

Tool chạy được **không cần khoá API** (dùng nút "Tạo đề bài" để copy sang AI khác).
Muốn tool **tự dịch ngay trong trang**, cần gắn khoá API:

**Bước 1:** Copy file `.env.MAU` → đổi tên thành `.env`

**Bước 2:** Mở `.env`, chọn dịch vụ và dán khoá vào:

```
AI_PROVIDER=nous      # nous | gemini | openai
OPENAI_API_KEY="dan_khoa_cua_ban_vao_day"
```

**Bước 3:** Tắt và bật lại tool.

Hoặc đơn giản hơn: chạy tool rồi bấm **"Đổi model / dịch vụ"** trên giao diện.

### Dịch vụ AI được hỗ trợ

| Dịch vụ | Địa chỉ API | Khoá bắt đầu bằng |
|---|---|---|
| **Nous Portal** | `inference-api.nousresearch.com/v1` | `sk-nous-` |
| **Google Gemini** | `generativelanguage.googleapis.com/v1beta/openai` | `AIza` |
| **OpenAI** | `api.openai.com/v1` | `sk-proj-` / `sk-` |

> ⚠️ **Khoá của dịch vụ nào phải khớp `AI_PROVIDER` của dịch vụ đó.**
> Dùng khoá Gemini mà để `AI_PROVIDER=openai` sẽ báo lỗi 401.

> 🔒 **File `.env` đã được chặn khỏi Git** — khoá API sẽ không bị đẩy lên GitHub.

---

## 📁 Cấu trúc dự án

```
yt_lyrics/
├── BAT-TOOL.bat            ← Nhấp đúp để chạy
├── app.py                  ← Web server (Flask)
├── core.py                 ← Lấy lời: từ link YouTube hoặc từ file trong máy
├── analyzer.py             ← Gọi AI: dịch, phân tích, đổi model
├── download_model.py       ← Tải model nhận dạng giọng nói
├── requirements.txt        ← Danh sách thư viện cần cài
├── HUONG-DAN.md            ← Hướng dẫn sử dụng chi tiết
└── templates/
    └── index.html          ← Giao diện web
```

---

## 🛠️ Yêu cầu hệ thống

- **Python 3.10+**
- Kết nối Internet (để tải video từ YouTube và gọi API AI)
- Không cần cài ffmpeg

---

## 📌 Ghi chú kỹ thuật

- **Nhận dạng giọng nói:** dùng `faster-whisper` (model `base`, ~140 MB), tự tải về lần đầu.
  Đổi model qua biến môi trường `WHISPER_MODEL` (`tiny` / `base` / `small` / `medium`).
- **File trong máy — không cần cài thêm gì:** tool dùng thư viện âm thanh `av` (đã có sẵn)
  để đọc thẳng file video/audio, nên **không cần ffmpeg**. Dán đường dẫn thì tool đọc trực tiếp
  file gốc (không copy); nút "Chọn file" thì sao chép tạm rồi tự xoá sau khi nghe xong.
- **File phụ đề (.srt / .vtt / .txt):** đọc thẳng ra lời, không chạy nhận dạng giọng nói.
- **File tạm:** lưu trong thư mục tạm của hệ điều hành và **tự xoá** ngay sau khi nghe xong.
- **Giới hạn của Whisper:** chỉ dịch được sang **tiếng Anh**. Muốn dịch sang tiếng Việt phải
  dùng AI dịch thật qua API (đó là lý do tool có tính năng gắn khoá API).

---

## 📄 Giấy phép

Dự án cá nhân, dùng tự do.
