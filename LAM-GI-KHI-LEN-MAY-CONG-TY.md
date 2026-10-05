# 🏢 LÀM GÌ KHI LÊN MÁY CÔNG TY

> Trang này để Đại mở ra xem khi ngồi ở máy công ty. Ngắn gọn, 3 bước.

---

## ⚠️ ĐIỀU QUAN TRỌNG NHẤT

**File `.env` KHÔNG có trên GitHub.** Đây là điều **cố ý** — vì file đó chứa khoá API,
không được đẩy lên mạng.

```
GitHub có:  ✅ .env.MAU   (bản mẫu trống, không có khoá)
GitHub KHÔNG có: ❌ .env    (file thật chứa khoá — Đại phải tự tạo)
```

👉 **Nghĩa là: máy công ty sẽ KHÔNG có sẵn khoá. Đại phải tự tay tạo file `.env` và dán khoá vào.**

---

## 📋 3 BƯỚC TẠI MÁY CÔNG TY

### BƯỚC 1 — Tải code về

Mở thư mục Đại muốn để dự án → nhấp chuột phải → **Open Git Bash here** → dán dòng này rồi Enter:

```
git clone https://github.com/quangdaiai2-wq/youtube-lyrics-tool.git
```

> 🔐 Nếu hiện cửa sổ đăng nhập GitHub → bấm **`Sign in with your browser`** → **`Authorize`**.

Xong sẽ có thư mục tên `youtube-lyrics-tool`.

---

### BƯỚC 2 — Tạo file khoá và dán khoá vào

**2.1** Mở thư mục `youtube-lyrics-tool` → tìm file tên **`.env.MAU`**

**2.2** Copy file đó → dán ngay tại chỗ → đổi tên bản copy thành **`.env`**
(bỏ chữ `.MAU` ở cuối)

> 💡 **Mẹo đổi tên:** nhấp chuột phải vào file → **Rename** → xoá `.MAU` → Enter.

**2.3** Mở file `.env` vừa tạo bằng **Notepad**. Tìm 2 dòng này:

```
AI_PROVIDER="nous"
OPENAI_API_KEY="dan_khoa_cua_dai_vao_day"
```

**2.4** Xoá chữ `dan_khoa_cua_dai_vao_day`, dán **khoá API thật** của Đại vào giữa hai dấu ngoặc kép.

> 🔑 **Khoá giống mật khẩu** — dài ~40 ký tự, bắt đầu bằng `sk-nous-`.
> Đại lấy lại ở trang quản lý tài khoản Nous Portal.

**2.5** Bấm **Ctrl + S** để lưu → đóng Notepad.

---

### BƯỚC 3 — Chạy tool

Nhấp đúp vào **`yt_lyrics\BAT-TOOL.bat`** → trình duyệt tự mở → dán link YouTube → thử dịch.

> 📌 **Lần đầu chạy sẽ hơi chậm** vì máy phải tải thư viện và model nhận dạng giọng nói
> (khoảng 140 MB). Từ lần sau sẽ nhanh.

---

## ✅ KIỂM TRA ĐÃ THÀNH CÔNG CHƯA

Sau khi trích xuất lời, nhìn vào **khung xanh** trên cùng. Nếu thấy nút:

```
[ ⚡ Dịch ngay (Nous Portal) ]
```

→ **Thành công!** Bấm nút đó là có bản dịch tiếng Việt.

Nếu **không thấy nút ⚡** → khoá chưa được nhận. Xem lại Bước 2 (có thể thiếu dấu ngoặc kép,
hoặc dán thừa dấu cách).

---

## 🚫 3 LỖI HAY GẶP

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Không thấy nút **⚡ Dịch ngay** | File chưa tên đúng là `.env` | Kiểm tra: phải là `.env`, không phải `.env.MAU` hay `.env.txt` |
| Báo lỗi **401** | Khoá bị sai/dán thiếu ký tự | Copy lại khoá, dán đủ vào giữa hai dấu `"` |
| Báo lỗi **404** | Tên model bị cũ | Mở tool → bấm **"Đổi model / dịch vụ"** → chọn model khác |

---

## 🔄 VỀ CHUYỆN ĐỒNG BỘ 2 MÁY

Vì khoá API không nằm trên GitHub (cố ý), nên:

| | Máy nhà | Máy công ty |
|---|---|---|
| Code | ✅ Có (từ GitHub) | ✅ Có (từ GitHub) |
| File `.env` + khoá | ✅ Có sẵn | ❌ Phải tự tạo (Bước 2) |

👉 **Sau này đổi máy khác, lại làm Bước 2 một lần nữa.** Chỉ mất khoảng 1 phút.

> 💡 **Nếu muốn tiện hơn:** Đại có thể lưu khoá vào phần mềm quản lý mật khẩu (như Bitwarden,
> hoặc ghi chú riêng có khoá). Đừng lưu vào file trong thư mục dự án — sẽ bị Git đẩy lên mạng.

---

## 📥 KHI NÀO CẦN CẬP NHẬT CODE MỚI?

Nếu Trợ lý có sửa code trên máy nhà và đẩy lên GitHub, máy công ty tải về bằng:

```
git pull
```

(chạy trong thư mục `youtube-lyrics-tool`)

> ⚠️ **Không lo mất khoá:** `git pull` **không đụng tới** file `.env` của Đại.

---

**👉 Tóm lại: lên công ty chỉ cần làm Bước 1 (tải code) + Bước 2 (dán khoá) là xong.**
