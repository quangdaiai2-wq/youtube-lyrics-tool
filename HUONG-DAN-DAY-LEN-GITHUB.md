# 🚀 HƯỚNG DẪN ĐẨY CODE LÊN GITHUB

> Dành cho Đại — người không biết lập trình. Làm đúng thứ tự từng bước.
> Trợ lý đã làm xong **phần chuẩn bị trên máy**. Đại chỉ cần làm **2 việc trên trang GitHub**.

---

## 📌 TÌNH HÌNH HIỆN TẠI

Trợ lý **đã làm xong**:

| Việc | Trạng thái |
|---|---|
| Khởi tạo Git cho dự án | ✅ Xong |
| Chặn file `.env` (chứa khoá API) khỏi GitHub | ✅ Xong — đã kiểm tra kỹ |
| Tạo file `README.md` giới thiệu dự án | ✅ Xong |
| Tạo bản lưu đầu tiên (12 file) | ✅ Xong |
| Kiểm tra không có khoá thật lọt vào | ✅ An toàn tuyệt đối |

**Thông tin tài khoản GitHub đã nhận diện được:**

```
👤 Tên đăng nhập: quangdaiai2-wq
🔐 Máy đã có sẵn công cụ đăng nhập tự động
```

---

## 🎯 ĐẠI CẦN LÀM: 2 VIỆC

### VIỆC 1 — Tạo "kho chứa" trên GitHub (khoảng 1 phút)

**Bước 1:** Mở trình duyệt, vào địa chỉ: **https://github.com/new**

**Bước 2:** Điền vào trang vừa mở:

| Ô cần điền | Điền gì |
|---|---|
| **Repository name** | `youtube-lyrics-tool` |
| **Description** | (không bắt buộc) `Tool trích xuất lời bài hát YouTube và dịch sang tiếng Việt` |
| **Public / Private** | 🔘 Chọn **Private** (riêng tư) |

**Bước 3:** **QUAN TRỌNG — kéo xuống dưới cùng**, bỏ qua các ô "Add a README file", "Add .gitignore", "Choose a license" — **ĐỪNG tích vào ô nào cả**.

> ⚠️ **Vì sao không tích?** Vì máy Đại đã có sẵn code rồi. Nếu tích, GitHub sẽ tạo thêm file
> gây xung đột, phải làm lại từ đầu.

**Bước 4:** Bấm nút xanh **`Create repository`**.

**Bước 5:** Trang mới hiện ra. **Đừng bấm gì cả** — chỉ cần copy lại **địa chỉ** trên thanh trình duyệt, dạng:

```
https://github.com/quangdaiai2-wq/youtube-lyrics-tool
```

→ **Copy địa chỉ này rồi dán vào ô chat, gửi cho Trợ lý.**

---

### VIỆC 2 — Đăng nhập khi được hỏi (khoảng 30 giây)

Sau khi Đại gửi địa chỉ, Trợ lý sẽ chạy lệnh đẩy code lên. Máy sẽ **tự bật một cửa sổ nhỏ** hỏi Đại đăng nhập:

```
┌──────────────────────────────────────────────┐
│   Sign in to GitHub                          │
│                                              │
│   [ Sign in with your browser ]  ← BẤM CÁI NÀY │
│                                              │
│   [ Sign in with a code ]                    │
└──────────────────────────────────────────────┘
```

**Bước 1:** Bấm **`Sign in with your browser`**

**Bước 2:** Trình duyệt mở trang GitHub → bấm **`Authorize`** (Cho phép)

**Bước 3:** Xong. Cửa sổ tự đóng, code được đẩy lên.

> 💡 **Có thể Đại không cần tạo Token gì cả** — máy đã có công cụ đăng nhập sẵn, chỉ cần
> bấm vài nút là xong. Nếu cửa sổ đó yêu cầu dán Token, Trợ lý sẽ hướng dẫn riêng.

---

## ❓ GIẢI THÍCH: "TOKEN" LÀ GÌ?

Đại hỏi chưa rõ Token là gì. Giải thích ngắn gọn:

```
🏢 NHÀ (máy Đại)                    🏦 NGÂN HÀNG (GitHub)
   │                                    │
   │  1. Gõ cửa: "Cho tôi gửi code"     │
   │ ──────────────────────────────────>│
   │                                    │
   │  2. Ngân hàng hỏi: "Anh là ai?"    │
   │ <──────────────────────────────────│
   │                                    │
   │  3. Đưa CHÌA KHOÁ (Token) 🗝️        │
   │ ──────────────────────────────────>│
   │                                    │
   │  4. "Chìa đúng rồi, mời vào" ✅     │
   │ <──────────────────────────────────│
```

**Token giống như một "chìa khoá điện tử"** — thay cho mật khẩu khi máy tự động gửi code lên GitHub.

| | Mật khẩu | Token (chìa khoá) |
|---|---|---|
| Dùng để | Đăng nhập bằng tay | Máy tự động gửi code |
| Phạm vi | Toàn quyền tài khoản | Chỉ được làm việc Đại cho phép |
| Thu hồi | Phải đổi mật khẩu | Xoá chìa là xong, không ảnh hưởng gì khác |

**Tin tốt:** Máy Đại **đã cài sẵn công cụ quản lý chìa khoá** (Git Credential Manager).
Nghĩa là Đại chỉ cần **đăng nhập một lần qua trình duyệt**, máy tự lưu chìa lại, **không
cần tạo Token thủ công**. Lần sau đẩy code lên sẽ không hỏi nữa.

---

## 🛡️ VỀ CHUYỆN BẢO MẬT

Đại lo khoá API bị lộ lên mạng — Trợ lý đã xử lý:

**Bước 1:** File `.env` (chứa khoá thật) đã được ghi vào danh sách chặn — Git **tuyệt đối không đẩy file này lên**.

**Bước 2:** Trợ lý đã **quét toàn bộ 12 file sẽ đẩy lên**, tìm đúng chuỗi khoá thật của Đại:

```
🔍 Kết quả: ✅ Không file nào chứa khoá thật
```

**Bước 3:** Kiểm tra lại danh sách sau khi đẩy lên, để chắc chắn.

> ⚠️ **Lưu ý riêng:** Khoá Nous của Đại đã từng xuất hiện trong lịch sử trò chuyện với
> Trợ lý. Điều đó **không liên quan tới GitHub**, nhưng nếu Đại muốn yên tâm tuyệt đối,
> có thể vào Nous Portal tạo khoá mới rồi thay vào file `.env`.

---

## 📋 TÓM TẮT — ĐẠI LÀM GÌ

| # | Việc | Ai làm |
|---|---|---|
| 1 | Khởi tạo Git, chặn `.env`, tạo README, lưu bản đầu | ✅ Trợ lý (xong) |
| 2 | Tạo kho trên GitHub tại **github.com/new** | 👉 **Đại** |
| 3 | Copy địa chỉ kho, dán vào ô chat | 👉 **Đại** |
| 4 | Chạy lệnh đẩy code lên | ✅ Trợ lý |
| 5 | Bấm `Sign in with your browser` → `Authorize` | 👉 **Đại** |
| 6 | Kiểm tra code đã lên, xác nhận không lộ khoá | ✅ Trợ lý |

**👉 Việc tiếp theo của Đại: làm VIỆC 1 ở trên, rồi gửi địa chỉ kho cho Trợ lý.**
