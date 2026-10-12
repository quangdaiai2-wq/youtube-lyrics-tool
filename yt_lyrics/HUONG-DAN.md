# HƯỚNG DẪN SỬ DỤNG — Tool trích xuất lời bài hát

> Dành cho người không biết lập trình. Làm theo đúng thứ tự từng bước.

---

## 1. Tool này làm được gì?

Đại đưa vào **một trong hai nguồn** → tool tự lấy lời bài hát → Đại bấm nút để **dịch sang tiếng Việt** hoặc cho AI phân tích.

| Nguồn | Cách đưa vào |
|---|---|
| 🔗 **Link YouTube** | Dán link vào ô (tab "🔗 Link YouTube") |
| 💻 **Video/audio có sẵn trong máy** | Dán đường dẫn file, hoặc bấm "📁 Hoặc chọn file từ máy" (tab "💻 Video trong máy") |

```
🔗 Link YouTube  ────┐
                     ├──→ Lấy lời ──→ 📝 Lời bài hát ──→ 🌐 Dịch / 🤖 Phân tích
💻 File trong máy ───┘
```

**Đường đi của từng nguồn:**

```
🔗 LINK YOUTUBE
      ↓
┌─────────────────────────────┐
│ 1. Video có phụ đề sẵn?     │──✅ Có──→ Lấy luôn (nhanh, chính xác)
└─────────────────────────────┘
      │
      ❌ Không có
      ↓
┌─────────────────────────────┐
│ 2. Tải phần tiếng của video │
│ 3. AI nghe và chép lại lời  │  ← chậm hơn, có thể sai vài chữ
└─────────────────────────────┘

💻 FILE TRONG MÁY
      ↓
┌─────────────────────────────┐
│ Là file phụ đề (.srt/.vtt)? │──✅ Phải──→ Đọc thẳng (không cần nghe)
└─────────────────────────────┘
      │
      ❌ Không phải
      ↓
┌─────────────────────────────┐
│ Đọc thẳng file gốc rồi      │  ← KHÔNG copy file, KHÔNG tải gì về,
│ 3. AI nghe và chép lại lời  │     không cần cài thêm gì
└─────────────────────────────┘
```

Cả hai nguồn đều dẫn tới cùng các nút:

```
┌──────────────────────────────────────────────────┐
│  🌐 DỊCH SANG TIẾNG VIỆT   ← việc chính ⭐       │
│     ⚡ Dịch ngay bằng API                        │
│     📝 Tạo đề bài dịch (miễn phí)               │
├──────────────────────────────────────────────────┤
│  📝 VIỆC KHÁC                                    │
│     📄 Chuyển thành đoạn văn (bỏ mốc thời gian) │
│     🤖 Cho AI đọc và phân tích                   │
└──────────────────────────────────────────────────┘
```

**Việc chính — dịch sang tiếng Việt:**

| Nút | Kết quả |
|---|---|
| ⚡ **Dịch ngay (theo API)** | Dịch *bất kỳ ngôn ngữ nào* sang tiếng Việt, ngay trong tool, chia đoạn sẵn |
| 📝 **Tạo đề bài dịch** | Cách dự phòng miễn phí — tạo đề bài, copy dán sang WorkBuddy/ChatGPT |

**Việc khác:**

| Nút | Kết quả |
|---|---|
| 📄 **Chuyển sang dạng đoạn văn** | Gộp lời rời rạc thành đoạn văn liền mạch, sạch mốc thời gian |
| 🤖 **Phân tích bằng AI** | 8 mục phân tích: chủ đề, cảm xúc, thông điệp... (không phải dịch) |

---

## 2. Cách chạy tool (1 bước — cách nhanh nhất)

### Nhấp đúp vào file `CHAY-TOOL.vbs` ở **thư mục gốc dự án**

```
D:\Buddy Work AI\2026-10-06-08-41-26\youtube-lyrics-tool\CHAY-TOOL.vbs
```

Tool sẽ tự bật lên và tự mở trình duyệt cho Đại. Xong.

> 🕶️ **Không còn cửa sổ đen nào hiện ra.** Tool chạy ngầm ở dưới, Đại chỉ thấy trình duyệt mở ra.

> ⏻ **Muốn tắt tool?** Bấm nút **"⏻ Tắt tool"** ở **cuối trang web**.
> Vì tool chạy ngầm nên không có cửa sổ nào để đóng — nút đó mới là chỗ tắt.

> 🖱️ File `CHAY-TOOL.bat` (nhấp đúp) cũng chạy được như cũ, nhưng nó sẽ **nháy một cửa sổ đen rất nhanh** rồi tắt.
> Muốn hoàn toàn không thấy gì thì dùng file `.vbs`.

<details>
<summary><b>Cách khác — chạy trực tiếp trong thư mục <code>yt_lyrics</code></b></summary>

Mở thư mục:

```
D:\Buddy Work AI\2026-10-06-08-41-26\youtube-lyrics-tool\yt_lyrics
```

Rồi nhấp đúp vào file `BAT-TOOL.bat`. **Cách này CÓ hiện cửa sổ đen** — dùng khi
Đại muốn nhìn thấy thông báo, ví dụ khi tool báo lỗi mà không rõ vì sao.

</details>

---

<details>
<summary><b>Cách 2 — Chạy bằng dòng lệnh (nếu file .vbs không chạy được)</b></summary>

1. Nhấn phím **Windows**, gõ `cmd`, nhấn **Enter**.
2. Copy và dán nguyên dòng sau rồi nhấn **Enter**:

```
cd /d "D:\Buddy Work AI\2026-10-06-08-41-26\youtube-lyrics-tool\yt_lyrics" && "C:\Users\nguye\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe" app.py
```

> Đại **không cần hiểu** đoạn lệnh này. Nó chỉ có nhiệm vụ: đi tới thư mục tool và bật tool lên.

3. Mở **Chrome**, gõ vào thanh địa chỉ: `http://127.0.0.1:5000`

</details>

---

<details>
<summary><b>Nếu bấm mà không thấy gì xảy ra (tool chạy ngầm nên im lặng)</b></summary>

Vì tool không hiện cửa sổ, nó cũng **không kêu ca** khi có trục trặc. Kiểm tra theo thứ tự:

1. **Đợi khoảng 5 giây** — lần đầu mở hơi chậm, trình duyệt sẽ tự mở.
2. **Không thấy trình duyệt mở?** Tự mở Chrome và gõ `http://127.0.0.1:5000`.
3. **Vẫn không được?** Mở file nhật ký `yt_lyrics\tool.log` bằng Notepad — mọi thông báo của tool được ghi vào đó.
4. **Vẫn bí?** Nhấp đúp `yt_lyrics\BAT-TOOL.bat` — bản này có cửa sổ đen, sẽ hiện thẳng lỗi ra cho Đại thấy.

</details>

---

## 3. Cách dùng trên giao diện

### Bước 1 — Chọn nguồn lấy lời

Ở Bước 1 có **2 tab**, bấm để chuyển qua lại:

| Tab | Dùng khi nào |
|---|---|
| 🔗 **Link YouTube** | Video nằm trên YouTube |
| 💻 **Video trong máy** | Video/audio đã có sẵn trong máy Đại |

#### Tab 🔗 Link YouTube
Dán link video vào ô lớn, ví dụ:
- `https://www.youtube.com/watch?v=xxxxxxxxxxx`
- `https://youtu.be/xxxxxxxxxxx`
- `https://www.youtube.com/shorts/xxxxxxxxxxx`

#### Tab 💻 Video trong máy
Có **2 cách**, dùng cách nào cũng được:

**Cách A — Dán đường dẫn (nhanh hơn, khuyên dùng):**
1. Mở thư mục chứa file bằng Windows Explorer.
2. Giữ phím **Shift** + **bấm chuột phải** vào file → chọn **"Copy as path"**.
3. Dán vào ô đường dẫn trong tool (dán cả dấu ngoặc kép cũng được, tool tự bỏ).

> Cách này tool **đọc thẳng file gốc**: không sao chép, không tốn thêm dung lượng, file 2–3 GB vẫn chạy ngay.

**Cách B — Bấm nút 📁 Hoặc chọn file từ máy:**
1. Bấm nút → chọn file trong hộp thoại.
2. Tool hiện tên file và dung lượng → bấm **"Trích xuất lời"**.

> Cách này tool phải **sao chép file vào thư mục tạm** trước khi nghe (vì trình duyệt không cho biết đường dẫn thật). File tạm **tự xoá sau khi nghe xong**. File trên 500 MB nên dùng Cách A cho nhanh.

**File nhận được:** video (`mp4`, `mkv`, `webm`, `mov`, `avi`, `m4v`, `ts`…), file tiếng (`mp3`, `m4a`, `wav`, `flac`, `ogg`, `opus`, `aac`…), và **file phụ đề** (`srt`, `vtt`, `txt`).

> 📌 Chọn file phụ đề thì tool **đọc luôn**, không cần nghe — nhanh và chính xác nhất.

> 💡 Bấm **✕ Bỏ chọn** ở ô tên file nếu muốn quay lại dùng cách dán đường dẫn.

### Bước 2 — Bấm nút **"Trích xuất lời"**

Ngay sau khi bấm, một **thanh tiến độ** sẽ hiện ra và tự chạy:

```
⬇️ Đang tải phần tiếng của video           37%
████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
12/33 MB — 5.2 MB/s          ⏳ còn khoảng 8 giây
```

| Thành phần | Ý nghĩa |
|---|---|
| 🔴 Thanh đỏ có sọc chạy | Đang làm việc |
| **37%** | Đã xong 37% — **con số này mới là tiến độ** |
| `12/33 MB` | Đang tải được bao nhiêu phần tiếng |
| `⏳ còn khoảng 8 giây` | Ước tính thời gian còn lại |
| 🟢 Thanh xanh | Đã xong bước đó |

Thanh tiến độ chạy liền mạch, chia % theo **đúng nguồn Đại đang dùng**:

| Nguồn | Các bước | Chiếm |
|---|---|---|
| 🔗 Link YouTube | ⬇️ Tải phần tiếng | 0% → 15% |
| | 🎧 Nghe và chép lời | 15% → 100% |
| 💻 Dán đường dẫn | 📂 Đọc file trong máy | 0% → 3% |
| | 🎧 Nghe và chép lời | 3% → 100% |
| 💻 Chọn file từ máy | ⬆️ Gửi file lên tool | 0% → 10% |
| | 📂 Đọc file trong máy | 10% → 13% |
| | 🎧 Nghe và chép lời | 13% → 100% |

> 💡 Bước nghe lâu hơn nhiều. Video 30 phút mất vài phút. Cứ để thanh chạy, **đừng bấm lại nút** — sẽ chạy lại từ đầu.

Khi xong, thanh chuyển xanh và hiện `✅ Hoàn tất`, rồi tự ẩn đi để nhường chỗ cho kết quả.

**Nếu muốn bỏ qua phụ đề, nghe trực tiếp bằng AI** (chỉ có ở tab Link YouTube):
✅ Tích vào ô *"Bỏ qua phụ đề, nghe trực tiếp bằng AI"* trước khi bấm nút.

### Bước 3 — Các nút trên khung kết quả (chia làm 2 nhóm)

Sau khi trích xuất xong, các nút được xếp thành **2 nhóm có tiêu đề rõ ràng** để Đại không bấm nhầm:

```
┌─────────────────────────────────────────────────────┐
│  🌐 DỊCH SANG TIẾNG VIỆT          ← nhóm chính      │
│  [ ⚡ Dịch ngay (Nous Portal) ]  ← bấm cái này      │
│  [ 📝 Tạo đề bài dịch ]                             │
│  [ 📋 Copy bản dịch ]                               │
└─────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│  📝 VIỆC KHÁC                    ← nhóm phụ         │
│  [ 📄 Chuyển sang dạng đoạn văn ]                   │
│  [ 📋 Copy lời ]                                    │
│  [ 🤖 Phân tích bằng AI ]                           │
│  [ 📄 Tạo đề bài phân tích ]                        │
│  [ 🗑️ Xoá và làm bài khác ]                         │
└─────────────────────────────────────────────────────┘
```

> **Nhóm 🌐 Dịch sang tiếng Việt** là việc Đại cần làm nhiều nhất, nên được tô nền xanh và đặt **lên trên**.
> **Nhóm 📝 Việc khác** gom các nút phụ ở dưới. Nút **🤖 Phân tích bằng AI** nằm trong nhóm này — *không phải* nút dịch.

**Nút `📄 Chuyển sang dạng đoạn văn`**

Lời do AI tự nghe thường hiện từng dòng kèm mốc thời gian, ví dụ:

```
[10:22] with additional third-party tools.
[10:24] Notebook LM, for example, is one of my favorite MCPs
[10:26] in order to do research and to create a podcast
```

Bấm nút này, toàn bộ gộp thành đoạn văn đọc liền, **sạch mốc thời gian**, không phải xoá tay:

```
with additional third-party tools. Notebook LM, for example, is one of
my favorite MCPs in order to do research and to create a podcast like
you just saw earlier for my daily briefings.
```

Bấm lần nữa để quay lại dạng có mốc thời gian. Nút `📋 Copy lời` luôn copy đúng dạng đang xem.

### Bước 4 — Cho AI phân tích

Nút **🤖 Phân tích bằng AI** nằm trong nhóm **📝 Việc khác**. Có 2 cách, chọn 1:

| Cách | Khi nào dùng | Làm gì |
|---|---|---|
| **📄 Tạo đề bài phân tích** | Đơn giản nhất, không cần cài gì | Bấm nút → bấm *Copy* → dán vào WorkBuddy/ChatGPT → nhận phân tích |
| **🤖 Phân tích bằng AI** | Muốn phân tích ngay trong tool | Chỉ hiện khi Đại đã cấu hình khoá API (xem mục 7) |

---

## 4. Dịch lời bài hát sang tiếng Việt ⭐

Đây là **việc chính** của tool — dịch lời bài hát từ *bất kỳ ngôn ngữ nào* sang tiếng Việt, dùng **API** (không phải copy dán thủ công).

Khi video là tiếng nước ngoài, nhóm **🌐 Dịch sang tiếng Việt** tự hiện ở **đầu khung kết quả**:

```
🌐 DỊCH SANG TIẾNG VIỆT
[ ⚡ Dịch ngay (Nous Portal) ]   ← bấm là có bản dịch ngay
[ 📝 Tạo đề bài dịch ]           ← cách dự phòng, miễn phí
```

### Cách 1 — Bấm `⚡ Dịch ngay` (khuyên dùng, cần khoá API)

1. Bấm nút **⚡ Dịch ngay (Nous Portal)**.
2. Chờ vài giây — khung **🌐 Bản dịch tiếng Việt** tự mở ra ngay bên dưới, đã chia đoạn sẵn.
3. Bấm **📋 Copy bản dịch** là dùng được luôn.

Đã kiểm tra thực tế: Anh → Việt, Trung → Việt, Hàn → Việt đều chạy tốt qua API.

> ✅ Nếu bấm nút mà **không thấy gì hiện ra**: đó là lỗi cũ đã được sửa (khung bản dịch
> bị ẩn). Nay bấm là khung tự mở, có dòng "⏳ Đang dịch..." báo hiệu rõ ràng.

### Cách 2 — Bấm `📝 Tạo đề bài dịch` (miễn phí, không cần khoá)

1. Bấm **📝 Tạo đề bài dịch** → tool tạo sẵn đề bài.
2. Bấm **📋 Copy bản dịch** → dán vào WorkBuddy/ChatGPT → nhận bản dịch tiếng Việt.

Đề bài dịch đã viết sẵn yêu cầu chất lượng: dịch thoát ý đọc cho hay như lời Việt, giữ tên riêng, chia đoạn gọn gàng.

> ⚠️ **Vì sao cách 1 cần API?**
> Máy nghe sẵn có trong tool **chỉ dịch được sang tiếng Anh**, không dịch sang tiếng Việt. Muốn tool tự dịch sang tiếng Việt phải dùng AI dịch thật qua API. Chưa có khoá thì dùng cách 2 (copy dán) — vẫn miễn phí.

> 💡 **Không thấy nhóm 🌐 Dịch?** Nút **🌐 Dịch bài này sang tiếng Việt** nằm trong nhóm *Việc khác* — bấm nút đó để mở nhóm dịch bằng tay.

### Nếu bấm nhầm nút **🤖 Phân tích bằng AI**

Nút đó **phân tích** bài hát (nội dung, cảm xúc, thông điệp) — **không dịch**. Muốn có bản tiếng Việt, hãy bấm nút trong nhóm **🌐 Dịch sang tiếng Việt** ở trên cùng.

---

## 5. File tạm — có bị để lại không?

**Không.** Tool tự xoá sạch, dù thành công hay gặp lỗi.

**a) Khi lấy từ link YouTube:** file tiếng tải về chỉ nằm trong thư mục tạm và tự xoá ngay khi nghe xong.

| Thời điểm | File ở đâu |
|---|---|
| Đang nghe | `C:\Users\nguye\AppData\Local\Temp\ytlyrics_xxxx\audio.m4a` |
| Nghe xong | 🗑️ Đã xoá cùng cả thư mục `ytlyrics_xxxx` |

**b) Khi bấm "📁 Chọn file từ máy":** file Đại chọn được sao chép tạm vào thư mục `ytlyrics_up_xxxx`, rồi **tự xoá ngay khi nghe xong**.

| Thời điểm | File ở đâu |
|---|---|
| Đang nghe | `C:\Users\nguye\AppData\Local\Temp\ytlyrics_up_xxxx\bai-hat.mp4` |
| Nghe xong | 🗑️ Đã xoá cùng cả thư mục `ytlyrics_up_xxxx` |

> ⚠️ **File gốc của Đại KHÔNG bị đụng tới** — tool chỉ đọc. Chỉ bản sao tạm mới bị xoá.

**c) Khi dán đường dẫn:** không có file tạm nào cả — tool đọc thẳng file gốc, **không xoá gì**.

> 🧹 Nếu lần trước Đại chọn file rồi đóng tab mà chưa bấm "Trích xuất lời", bản sao tạm đó sẽ nằm lại tới lần mở tool sau — tool **tự dọn khi khởi động**.

Đã kiểm tra thực tế: sau nhiều lần chạy, thư mục tạm **không còn tàn dư nào**. Đại không cần dọn tay.

> 🔒 Riêng **lời bài hát** thì ở lại trong trình duyệt cho tới khi Đại bấm *Xoá và làm bài khác* hoặc đóng tab. Không có gì gửi lên mạng.

---

## 6. Phân tích AI sẽ cho Đại những gì?

| Mục | Nội dung |
|---|---|
| Tóm tắt nội dung | Bài hát kể về chuyện gì |
| Chủ đề chính | Tình yêu, quê hương, nỗi buồn... |
| Cảm xúc chủ đạo | Vui, buồn, da diết, hào hùng... |
| Thông điệp / ý nghĩa | Tác giả muốn nói điều gì |
| Cấu trúc bài hát | Verse / Chorus / Bridge... |
| Phân tích ngôn từ & hình ảnh | Cách dùng từ, ẩn dụ, so sánh |
| Câu hát đắt giá nhất | Câu hay nhất và lý do |
| Đánh giá tổng thể | Nhận xét chung |

---

## 7. (Tuỳ chọn) Gắn khoá API — mở khoá 2 nút ⚡

> ❌ **Bỏ qua mục này hoàn toàn cũng dùng được tool.** Khi chưa gắn khoá, Đại vẫn có cách miễn phí: bấm *"Tạo đề bài phân tích"* / *"Tạo đề bài dịch"* rồi dán vào WorkBuddy hoặc ChatGPT — kết quả tương đương.

Gắn khoá API thì tool **tự làm ngay trong trang**, không phải copy đi đâu. Khoá này mở khoá **2 nút**:

| Nút | Việc nó làm |
|---|---|
| ⚡ **Phân tích tự động** | AI đọc lời và trả về 8 mục phân tích ngay trên trang |
| ⚡ **Dịch ngay sang tiếng Việt** | AI dịch lời ngoại ngữ thành tiếng Việt, đã chia đoạn, copy dùng luôn |

### Cách gắn — làm 3 bước

**Bước 1️⃣** — Mở thư mục gốc dự án:

```
D:\Buddy Work AI\2026-10-06-08-41-26\youtube-lyrics-tool
```

**Bước 2️⃣** — Nhấp đúp vào file **`MO-FILE-ENV.bat`** → Notepad tự mở đúng file `.env`.

> ✅ **File `.env` đã được Trợ lý tạo sẵn** và đã đặt `AI_PROVIDER=nous` cho Đại rồi.
> Đại **không cần** tự copy hay đổi tên file như hướng dẫn cũ nữa.
> (Nếu muốn mở bằng tay: file `.env` nằm ngay trong thư mục gốc dự án ở trên — **không** nằm trong `yt_lyrics`.)

**Bước 3️⃣** — Trong Notepad, tìm dòng **`OPENAI_API_KEY`**. Đại sẽ thấy:

```
AI_PROVIDER=nous

OPENAI_API_KEY="dan_khoa_nous_cua_dai_vao_day"
```

Xoá đoạn chữ `dan_khoa_nous_cua_dai_vao_day`, rồi dán **khoá Nous Portal thật** của Đại vào giữa hai dấu ngoặc kép. Xong bấm **Ctrl+S**.

> 🔑 Khoá Nous Portal bắt đầu bằng `sk-nous-`. Lấy ở trang `portal.nousresearch.com`.
> 🛡️ **Đối xử như mật khẩu ngân hàng:** không chụp ảnh gửi ai, không đăng lên mạng, không đẩy lên GitHub. File `.env` đã được chặn sẵn khỏi GitHub.

> 💡 **Muốn đổi sang dịch vụ AI khác?** Sửa dòng `AI_PROVIDER=` thành một trong ba:

| Ghi vào | Dùng dịch vụ | Model tự động |
|---|---|---|
| `AI_PROVIDER=nous` | **Nous Portal** *(đang đặt sẵn cho Đại)* | `google/gemini-3.7-flash` |
| `AI_PROVIDER=gemini` | Google Gemini | `gemini-2.5-flash` |
| `AI_PROVIDER=openai` | OpenAI chính chủ | `gpt-4o-mini` |

> 🔑 **Khoá API là gì?** Dãy ký tự dài giống mật khẩu, do dịch vụ AI cấp cho Đại. Đại lấy ở trang quản lý tài khoản của dịch vụ mình dùng (Nous Portal / Google AI Studio / OpenAI Platform).
> ✅ **Khoá của dịch vụ nào thì phải khớp `AI_PROVIDER` của dịch vụ đó.** Dùng khoá Gemini mà lại để `AI_PROVIDER=openai` thì sẽ báo lỗi 401.

**Bước 4️⃣** — Tắt tool rồi bật lại:
- Nếu đang chạy: bấm vào cửa sổ đen của tool, nhấn **Ctrl + C**, rồi đóng cửa sổ.
- Nhấp đúp vào **`CHAY-TOOL.bat`** (nằm ở thư mục gốc dự án) để mở lại.

Xong. Trang web sẽ hiện **nút ⚡** kèm tên dịch vụ, ví dụ *"⚡ Dịch ngay (Google Gemini)"*. Ngay dưới đó cũng ghi rõ đang dùng model nào.

> ❓ **Không thấy nút ⚡?** Xem lại Bước 3 — khoá có thể bị dính dấu cách thừa, thiếu dấu ngoặc kép, hoặc tên dịch vụ gõ sai chính tả.

---

## 7b. Đổi model ngay trên giao diện (không cần sửa file) ⭐

**Từ nay Đại KHÔNG cần mở file `.env` để đổi model nữa.** Làm hết trên trang web:

**Bước 1** — Trích xuất lời một bài bất kỳ (hoặc bấm làm bài mới).

**Bước 2** — Ở **cuối khung kết quả**, nhìn dòng chữ nhỏ có ghi tên model đang dùng, ví dụ:

```
⚡ Các nút có dấu sét xử lý ngay trong tool bằng Nous Portal
   — model google/gemini-3.7-flash.   [Đổi model / dịch vụ]
```

Bấm vào dòng chữ xanh **`Đổi model / dịch vụ`**.

**Bước 3** — Khung vàng **🔀 Đổi dịch vụ và model** mở ra. Chọn theo 2 ô:

| Ô | Việc cần làm |
|---|---|
| **1. Chọn dịch vụ** | Nous Portal / Google Gemini / OpenAI |
| **2. Chọn model** | Danh sách model gợi ý sẵn — cứ bấm chọn |

**Bước 4** — Bấm **`💾 Lưu và dùng model này`**.

Xong. Tool dùng model mới **ngay lập tức**, và **lần sau mở lại vẫn nhớ** (đã ghi vào file cấu hình giúp Đại).

### Muốn xem ĐẦY ĐỦ các model mình dùng được?

Bấm nút **`🔄 Tải danh sách model thật`** — tool sẽ hỏi thẳng dịch vụ xem khoá của Đại
được dùng những model nào.

> 📊 Đã kiểm tra thực tế: Nous Portal trả về **429 model**. Đại có thể chọn bất kỳ model nào
> trong đó (OpenAI, Google, Anthropic, DeepSeek, Qwen, Moonshot...).

### Muốn gõ tên model không có trong danh sách?

Dùng ô **"Hoặc gõ tên model khác"** — gõ tay tên model rồi bấm Lưu. Ví dụ: `google/gemini-3.8-flash`.

> ⚠️ **Nhớ quy tắc đặt tên của Nous Portal:** phải ghi kèm tên hãng, ví dụ
> `google/gemini-3.7-flash` (ĐÚNG) thay vì `gemini-3.7-flash` (SAI).
> Riêng Gemini và OpenAI thì ghi tên trần, ví dụ `gemini-2.5-flash`, `gpt-4o-mini`.

### Khi nào nên đổi model?

| Tình huống | Nên làm |
|---|---|
| Muốn bản dịch tiếng Việt mượt, sát nghĩa | Đổi sang model có chữ **`pro`** hoặc **`claude`**, **`gpt`** |
| Muốn nhanh và rẻ | Giữ model có chữ **`flash`** hoặc **`mini`** |
| Model hiện tại báo lỗi **404** | Model đã bị nhà cung cấp ngừng phục vụ → bấm **Tải danh sách model thật** rồi chọn cái khác |

---

### Đại dùng Nous và Gemini đều được — chọn thế nào?

Cả hai đều dùng được, vì cả hai đều theo **"chuẩn OpenAI"** giống nhau. Điểm khác biệt đáng chú ý:

| | Nous Portal | Google Gemini |
|---|---|---|
| Địa chỉ API (tool tự điền) | `inference-api.nousresearch.com/v1` | `generativelanguage.googleapis.com/v1beta/openai` |
| Model mặc định | `google/gemini-3.7-flash` | `gemini-2.5-flash` |
| Điểm mạnh | **Gom hơn 400 model của nhiều hãng** (OpenAI, Anthropic, DeepSeek, Qwen...) trong 1 khoá duy nhất | Đa ngôn ngữ rất tốt, dịch tiếng Việt mượt |
| **Riêng việc dịch** | Tốt — có thể chọn model khác để tối ưu | **Nên chọn cái này** — dịch tiếng Việt mượt và sát nghĩa |

> 💡 **Gợi ý của Trợ lý:**
> - Chủ yếu **dịch lời bài hát** → dùng **Gemini**.
> - Muốn **một khoá dùng được nhiều hãng model** → dùng **Nous Portal**, rồi đổi `AI_MODEL` sang model mình thích (ví dụ `anthropic/claude-sonnet-5.5`, `deepseek/deepseek-v4.1-flash`).
>
> Đại đổi qua lại bất cứ lúc nào chỉ bằng cách sửa 1 dòng `AI_PROVIDER` rồi bật lại tool.

> ⚠️ **Lưu ý về Nous Portal:** model cũ `Hermes-4-70B` mà Trợ lý từng dùng **đã bị Nous ngừng phục vụ**. Tên model trên Nous Portal phải ghi **kèm tên hãng**, ví dụ `google/gemini-3.7-flash` — không ghi trần `gemini-3.7-flash`. Nếu thấy lỗi 404, nghĩa là tên model đã cũ; Đại hỏi Trợ lý để cập nhật.

### Muốn đổi model hoặc dùng dịch vụ khác hoàn toàn?

Trong file `.env` có sẵn 2 dòng bị khoá bằng dấu `#`. Bỏ dấu `#` ở đầu dòng và điền:

```
AI_MODEL=anthropic/claude-sonnet-5.5
OPENAI_BASE_URL="https://dia-chi-dich-vu-cua-dai/v1"
```

- `AI_MODEL` — đổi model. Ví dụ trên Nous Portal có sẵn: `google/gemini-3.7-flash`, `openai/gpt-5.6-luna`, `anthropic/claude-sonnet-5.5`, `deepseek/deepseek-v4.1-flash`, `moonshotai/kimi-k3`.
- `OPENAI_BASE_URL` — dùng dịch vụ **không có** trong danh sách 3 cái trên (miễn là theo chuẩn OpenAI).

Nếu không rõ dịch vụ mình dùng có theo chuẩn không — cứ hỏi Trợ lý.

---

## 8. Câu hỏi thường gặp

**Cửa sổ đen đâu rồi? Trước đây mở tool là có mà.**
→ Đã **bỏ hẳn cửa sổ đen** theo yêu cầu. Tool giờ chạy ngầm, Đại chỉ thấy trình duyệt mở ra.
→ Đổi lại: muốn tắt tool thì bấm nút **⏻ Tắt tool** ở cuối trang web (xem câu dưới).
→ Nếu vẫn muốn có cửa sổ đen (để nhìn thấy thông báo khi lỗi), nhấp đúp `yt_lyrics\BAT-TOOL.bat`.

**Tắt tool bằng cách nào?**
→ Bấm nút **⏻ Tắt tool** ở **cuối trang web**, rồi xác nhận. Trang sẽ báo "✅ Đã tắt tool" — lúc đó Đại đóng tab được.
→ Nếu đang mở tool bằng bản có cửa sổ đen thì vẫn tắt được bằng cách đóng cửa sổ đó như cũ.

**Bấm `CHAY-TOOL.vbs` mà không thấy gì xảy ra?**
→ Tool chạy ngầm nên **im lặng là bình thường**. Đợi khoảng 5 giây, trình duyệt sẽ tự mở.
→ Không thấy trình duyệt mở? Tự mở Chrome, gõ `http://127.0.0.1:5000`.
→ Vẫn không được? Mở `yt_lyrics\tool.log` bằng Notepad để xem tool báo gì, hoặc chạy `yt_lyrics\BAT-TOOL.bat` để thấy lỗi trực tiếp.

**Bấm `CHAY-TOOL.vbs` hai lần thì có mở 2 tool không?**
→ **Không.** Lần thứ hai tool phát hiện đã chạy sẵn nên chỉ mở thêm tab trình duyệt, không mở trùng.

**Nút "Tắt tool" có làm mất dữ liệu không?**
→ Không. Nút đó chỉ **tắt tool đang chạy ngầm**, giống như đóng cửa sổ đen trước đây. Nhưng lời bài hát đang xem trong tab sẽ mất nếu chưa copy — nên **copy trước khi tắt**.

**Lấy lời từ video trong máy có cần cài thêm gì không?**
→ **Không.** Tool đọc trực tiếp file bằng thư viện đã có sẵn, không cần cài ffmpeg hay phần mềm nào khác.

**Dán đường dẫn file mà tool báo "Không tìm thấy file"?**
→ Kiểm tra 3 điều:
> 1. **Đường dẫn có bị cắt không?** Đường dẫn phải có cả phần đuôi file, ví dụ `.mp4`. Nếu copy từ Explorer thì dùng **Shift + chuột phải → Copy as path** cho chắc.
> 2. **File có bị đổi tên/di chuyển không?** Dán lại đường dẫn mới.
> 3. **Có dán nhầm thư mục không?** Tool cần đường dẫn tới **file**, không phải thư mục.

**Tool báo "File này không có phần tiếng"?**
→ File đó chỉ có hình, không có tiếng (hoặc tiếng bị lỗi). Không thể lấy lời từ file không có tiếng.

**Tool báo "Không mở được file này"?**
→ File có thể bị **hỏng, đang tải dở**, hoặc là định dạng lạ. Thử mở file bằng trình xem video — nếu máy cũng không mở được thì file hỏng.

**Nên dùng "dán đường dẫn" hay "chọn file từ máy"?**
→ **Dán đường dẫn nhanh hơn và sạch hơn** (tool đọc thẳng, không sao chép). Chỉ dùng "chọn file" khi Đại ngại lấy đường dẫn.

**Chọn file phụ đề (.srt) thì sao?**
→ Tool **đọc thẳng**, không cần nghe — nhanh nhất và chính xác nhất. Nhưng nếu phụ đề đó là tiếng nước ngoài, Đại vẫn cần bấm dịch như thường.

**Lời bài hát bị sai vài chữ?**
→ Video đó không có phụ đề nên AI phải tự nghe. Tên riêng, từ lạ dễ sai. Nếu tìm được bản có phụ đề chính thức thì kết quả sẽ chuẩn hơn.

**Chạy mãi không xong?**
→ Video dài + không có phụ đề thì AI phải nghe toàn bộ, mất vài phút. Video 4 phút khoảng 1–2 phút xử lý.

**Báo lỗi "Link YouTube không hợp lệ"?**
→ Kiểm tra lại link đã copy đủ chưa. Link phải có phần `v=` hoặc `youtu.be/`.

**Báo không tải được audio?**
→ Video có thể bị giới hạn tuổi, riêng tư, hoặc chặn theo khu vực.

**Tool báo "Không mở được video này"?**
→ Video **không còn tồn tại** (đã bị xoá hoặc chuyển riêng tư), hoặc link copy bị thiếu ký tự. Thử mở link bằng trình duyệt — nếu Chrome xem được thì copy lại link đầy đủ từ thanh địa chỉ.

**Muốn bản dịch tiếng Việt nhưng không có nút dịch?**
→ Kiểm tra 2 điều:
> 1. **Lời có phải tiếng nước ngoài không?** Nút dịch **chỉ hiện khi lời không phải tiếng Việt**. Nếu lời đã là tiếng Việt, tool báo `✅ Lời đã là tiếng Việt, không cần dịch.`
> 2. **Đã gắn khoá API chưa?** Nút **⚡ Dịch ngay sang tiếng Việt** (dịch tự động trong trang) chỉ hiện sau khi gắn khoá — xem **mục 7**. Khi chưa gắn khoá, Đại dùng nút *"Tạo đề bài dịch"* rồi dán vào WorkBuddy/ChatGPT, cũng ra bản dịch.

**Vì sao máy nghe sẵn có không dịch sang tiếng Việt được?**
→ Đây là **giới hạn của công nghệ**, không phải lỗi tool. Máy nghe đó chỉ dịch được sang tiếng Anh. Muốn dịch sang tiếng Việt cần AI dịch thật — có 2 đường: gắn khoá API để tool dịch ngay (mục 7), hoặc dùng nút *"Tạo đề bài dịch"* rồi dán vào WorkBuddy/ChatGPT (miễn phí).

**Đại dùng API của Nous và Gemini được không?**
→ **Được cả hai.** Tool hỗ trợ sẵn, chỉ cần ghi tên dịch vụ vào 1 dòng trong `.env` (xem mục 7). Lưu ý: **khoá phải khớp dịch vụ** — khoá Gemini đi với `AI_PROVIDER=gemini`, khoá Nous đi với `AI_PROVIDER=nous`.

**Báo lỗi 401 / "Khoá API bị từ chối"?**
→ 3 nguyên nhân thường gặp:
> 1. **Khoá không khớp dịch vụ** — ví dụ dán khoá Gemini nhưng để `AI_PROVIDER=openai`. Sửa lại cho khớp.
> 2. **Khoá dán thiếu/thừa ký tự** — copy lại cẩn thận, nhớ giữ hai dấu ngoặc kép.
> 3. **Khoá hết hạn hoặc hết tiền** — vào trang quản lý tài khoản của dịch vụ kiểm tra.

**Báo lỗi 404 / "Không tìm thấy model"?**
→ Model đã bị nhà cung cấp **ngừng phục vụ** (chuyện rất hay xảy ra — tên model AI hết hạn nhanh).
→ Cách sửa **không cần mở file**: vào **mục 7b**, bấm **🔄 Tải danh sách model thật** rồi chọn một model còn dùng được, bấm Lưu.

**Bấm "⚡ Dịch ngay" mà không thấy bản dịch đâu?**
→ Lỗi này **đã được sửa**. Trước đây khung bản dịch bị ẩn. Nay bấm là khung tự mở kèm dòng "⏳ Đang dịch...".
→ Nếu vẫn không thấy: cuộn xuống dưới cùng khung kết quả — khung **🌐 Bản dịch tiếng Việt** nằm ngay dưới nhóm nút dịch.

**Không muốn sửa file `.env` để đổi model?**
→ Không cần nữa. Dùng **mục 7b** — đổi model ngay trên giao diện, bấm là xong.

**Báo lỗi 429?**
→ Dịch vụ báo quá nhiều yêu cầu hoặc hết hạn mức. Đợi vài phút rồi thử lại, hoặc kiểm tra hạn mức tài khoản.

**Máy chạy chậm vì model?**
→ Model mặc định là `base` (~140 MB), nhẹ và chạy tốt trên máy thường. Muốn chính xác hơn nữa thì nhờ Trợ lý đổi sang `small` hoặc `medium` (đổi 1 dòng cấu hình).

**Kết quả đã kiểm thử thực tế trên máy Đại:**

| Video thử | Cách lấy lời | Kết quả |
|---|---|---|
| Sơn Tùng M-TP — *Hãy trao cho anh* | Phụ đề chính thức | ✅ 2.743 ký tự, chính xác từng chữ |
| *Me at the zoo* (không có phụ đề) | AI tự nghe | ✅ Nhận đúng tiếng Anh (99%), sai 1 chữ ("trunks" → "hunts") |
| File video mp4 trong máy (có hình + tiếng) | AI nghe thẳng từ file | ✅ Nhận đúng câu nói, tiếng Anh (94%), đúng mốc thời gian |
| File phụ đề .srt trong máy | Đọc thẳng file | ✅ Ra đủ 3 dòng, giữ nguyên dấu tiếng Việt |

> 📌 **Rút ra:** video có phụ đề (nhạc Việt có MV chính thức thường có) thì kết quả hoàn hảo. Video không phụ đề thì nên nâng model lên `small` để giảm sai sót.

**Tool có gửi dữ liệu đi đâu không?**
→ Lời bài hát **không** rời khỏi máy Đại, trừ khi Đại bấm *Copy* và tự dán vào một AI online. Việc lấy video thì tất nhiên phải kết nối tới YouTube.

**Lần đầu chạy video không có phụ đề bị chậm?**
→ Lần đầu AI phải tải model về máy (~140 MB). Từ lần sau dùng lại nên nhanh hơn nhiều. Nếu muốn chuẩn bị trước, nhờ Trợ lý chạy lệnh tải model một lần.

**File audio tải về nằm ở đâu?**
→ Trong thư mục tạm của Windows, xem chi tiết mục 5. Tự xoá khi nghe xong.

---

## 9. Danh sách file trong tool

```
📁 D:\Buddy Work AI\2026-10-06-08-41-26\youtube-lyrics-tool\   ← THƯ MỤC GỐC
   ├── 🖱️ CHAY-TOOL.vbs      ← NHẤP ĐÚP VÀO ĐÂY ĐỂ CHẠY TOOL (không hiện cửa sổ đen)
   ├── 🖱️ CHAY-TOOL.bat      ← Bản chạy cũ (có nháy cửa sổ đen rất nhanh rồi tắt)
   ├── 🖱️ MO-FILE-ENV.bat    ← NHẤP ĐÚP ĐỂ MỞ FILE .env ĐIỀN KHOÁ API
   ├── XEM-TRUOC-GIAO-DIEN.html ← Xem trước giao diện, không cần chạy tool
   ├── .env                 ← Khoá API thật của Đại (đã tạo sẵn, xem mục 7)
   ├── .env.MAU             ← Bản mẫu khoá API (giữ làm tham khảo)
   ├── README.md
   └── 📁 yt_lyrics\
        ├── BAT-TOOL.bat     ← Bản chạy CÓ cửa sổ đen — dùng khi cần nhìn thấy lỗi
        ├── tool.log         ← Nhật ký của tool (tự tạo khi chạy ngầm, xem khi trục trặc)
        ├── HUONG-DAN.md     ← File Đại đang đọc
        ├── app.py           ← Bật giao diện web
        ├── core.py          ← Phần lấy lời bài hát
        ├── analyzer.py      ← Phần cho AI phân tích
        ├── download_model.py← Tải model nhận dạng giọng nói
        ├── requirements.txt ← Danh sách thư viện cần cài
        └── 📁 templates\
             └── index.html  ← Giao diện

📁 C:\Users\nguye\.cache\huggingface\   ← Nơi lưu model AI (tự tải về)
```

> Đại **không cần mở** các file này. Chỉ cần nhấp đúp **`CHAY-TOOL.vbs`** ở thư mục gốc.
> Riêng `.env` thì mở **một lần duy nhất** bằng **`MO-FILE-ENV.bat`** nếu muốn dùng 2 nút ⚡ — hướng dẫn ở **mục 7**.

---

## 10. Nếu chuyển sang máy khác

Tool đã cài sẵn trên máy này. Nếu muốn dùng ở **máy công ty**, cần cài lại thư viện (làm 1 lần):

```
cd /d "đường_dẫn_tới_thư_mục_yt_lyrics" && "đường_dẫn_python" -m pip install -r requirements.txt
```

Nhờ **Trợ lý** làm giúp bước này — Đại chỉ cần mở máy và nói "cài tool lời bài hát".
