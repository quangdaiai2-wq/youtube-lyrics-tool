# HƯỚNG DẪN SỬ DỤNG — Tool trích xuất lời bài hát YouTube

> Dành cho người không biết lập trình. Làm theo đúng thứ tự từng bước.

---

## 1. Tool này làm được gì?

Đại dán một link YouTube vào → tool tự lấy lời bài hát → Đại bấm nút để **dịch sang tiếng Việt** hoặc cho AI phân tích.

```
🔗 Link YouTube
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
      ↓
   📝 Lời bài hát
      ↓
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

## 2. Cách chạy tool (2 bước — cách nhanh nhất)

### Bước 1 — Mở thư mục tool

Mở **File Explorer** (biểu tượng thư mục vàng trên thanh dưới màn hình), dán đường dẫn này vào thanh địa chỉ rồi nhấn **Enter**:

```
D:\Workbuddy AI\2026-10-05-21-21-00\yt_lyrics
```

### Bước 2 — Nhấp đúp vào file `BAT-TOOL.bat`

Tool sẽ tự bật lên và tự mở trình duyệt cho Đại. Xong.

> 🔄 **Muốn tắt tool?** Đóng cửa sổ đen vừa hiện ra.

---

<details>
<summary><b>Cách 2 — Chạy bằng dòng lệnh (nếu file .bat không chạy được)</b></summary>

1. Nhấn phím **Windows**, gõ `cmd`, nhấn **Enter**.
2. Copy và dán nguyên dòng sau rồi nhấn **Enter**:

```
cd /d "D:\Workbuddy AI\2026-10-05-21-21-00\yt_lyrics" && "C:\Users\nguye\.workbuddy-ai\binaries\python\envs\default\Scripts\python.exe" app.py
```

> Đại **không cần hiểu** đoạn lệnh này. Nó chỉ có nhiệm vụ: đi tới thư mục tool và bật tool lên.

3. Mở **Chrome**, gõ vào thanh địa chỉ: `http://127.0.0.1:5000`

</details>

---

## 3. Cách dùng trên giao diện

### Bước 1 — Dán link
Dán link video YouTube vào ô lớn, ví dụ:
- `https://www.youtube.com/watch?v=xxxxxxxxxxx`
- `https://youtu.be/xxxxxxxxxxx`
- `https://www.youtube.com/shorts/xxxxxxxxxxx`

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

Tool chạy qua **2 bước**, thanh tiến độ chạy liền mạch:

| Bước | Chiếm | Nội dung |
|---|---|---|
| ⬇️ Tải phần tiếng | 0% → 15% | Tải audio của video về máy |
| 🎧 Nghe và chép lời | 15% → 100% | AI nghe và viết ra lời |

> 💡 Bước 2 lâu hơn nhiều. Video 30 phút mất vài phút. Cứ để thanh chạy, **đừng bấm lại nút** — sẽ chạy lại từ đầu.

Khi xong, thanh chuyển xanh và hiện `✅ Hoàn tất`, rồi tự ẩn đi để nhường chỗ cho kết quả.

**Nếu muốn bỏ qua phụ đề, nghe trực tiếp bằng AI:**
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

## 5. File audio tạm — có bị để lại không?

**Không.** File audio tải về chỉ nằm trong thư mục tạm của Windows và **tự xoá ngay khi nghe xong**, dù thành công hay gặp lỗi.

| Thời điểm | File audio ở đâu |
|---|---|
| Đang nghe | `C:\Users\nguye\AppData\Local\Temp\ytlyrics_xxxx\audio.m4a` |
| Nghe xong | 🗑️ Đã xoá cùng cả thư mục `ytlyrics_xxxx` |

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

### Cách gắn — làm 4 bước

**Bước 1️⃣** — Mở thư mục `D:\Workbuddy AI\2026-10-05-21-21-00\` bằng File Explorer.

Trong đó có sẵn file mẫu tên **`.env.MAU`**. Đây là bản mẫu Trợ lý đã chuẩn bị, có ghi chú hướng dẫn ngay bên trong.

**Bước 2️⃣** — Bấm chuột phải vào `.env.MAU` → **Copy**, rồi **Paste** ngay tại chỗ đó (Ctrl+V). Sẽ có file mới tên `.env.MAU - Copy`.

Bấm chuột phải vào file mới → **Rename** → đổi tên thành:

```
.env
```

> ⚠️ Tên chỉ có đúng 4 ký tự: dấu chấm, chữ `e`, chữ `n`, chữ `v`. **Không có `.txt`** ở cuối. Nếu Windows giấu phần đuôi file, tên trong ô Rename cứ gõ đúng `.env` là được.

**Bước 3️⃣** — Mở file `.env` bằng **Notepad** (chuột phải → Open with → Notepad). Đại sẽ thấy **2 dòng quan trọng**:

```
AI_PROVIDER=openai

OPENAI_API_KEY="dan_khoa_cua_dai_vao_day"
```

**3a. Chọn dịch vụ AI** — sửa dòng `AI_PROVIDER=` thành một trong ba:

| Ghi vào | Dùng dịch vụ | Model tự động |
|---|---|---|
| `AI_PROVIDER=openai` | OpenAI chính chủ *(mặc định)* | `gpt-4o-mini` |
| `AI_PROVIDER=gemini` | **Google Gemini** | `gemini-2.5-flash` |
| `AI_PROVIDER=nous` | **Nous Portal** | `google/gemini-3.7-flash` |

**3b. Dán khoá API** — xoá đoạn `dan_khoa_cua_dai_vao_day`, dán **khoá thật** của Đại vào giữa hai dấu ngoặc kép. Xong bấm **Ctrl+S**.

> 🔑 **Khoá API là gì?** Dãy ký tự dài giống mật khẩu, do dịch vụ AI cấp cho Đại. Đại lấy ở trang quản lý tài khoản của dịch vụ mình dùng (Nous Portal / Google AI Studio / OpenAI Platform).
> ✅ **Khoá của dịch vụ nào thì phải khớp `AI_PROVIDER` của dịch vụ đó.** Dùng khoá Gemini mà lại để `AI_PROVIDER=openai` thì sẽ báo lỗi 401.
> 🛡️ **Đối xử như mật khẩu ngân hàng:** không chụp ảnh gửi ai, không đăng lên mạng, không đẩy lên GitHub. File `.env` đã được chặn sẵn khỏi GitHub.

**Bước 4️⃣** — Tắt tool rồi bật lại:
- Nếu đang chạy: bấm vào cửa sổ đen của tool, nhấn **Ctrl + C**, rồi đóng cửa sổ.
- Bấm đúp vào **`BAT-TOOL.bat`** để mở lại.

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
📁 yt_lyrics\
   ├── 🖱️ BAT-TOOL.bat       ← NHẤP ĐÚP VÀO ĐÂY ĐỂ CHẠY
   ├── HUONG-DAN.md          ← File Đại đang đọc
   ├── app.py                ← Bật giao diện web
   ├── core.py               ← Phần lấy lời bài hát
   ├── analyzer.py           ← Phần cho AI phân tích
   ├── download_model.py     ← Tải model nhận dạng giọng nói
   ├── requirements.txt      ← Danh sách thư viện cần cài
   └── 📁 templates\
        └── index.html       ← Giao diện

📁 C:\Users\nguye\.cache\huggingface\   ← Nơi lưu model AI (tự tải về)

📁 D:\Workbuddy AI\2026-10-05-21-21-00\
   ├── .env.MAU             ← Bản mẫu khoá API (xem mục 7)
   └── .env                 ← Khoá API thật của Đại (Đại tự tạo, xem mục 7)
```

> Đại **không cần mở** các file này. Chỉ cần nhấp đúp `BAT-TOOL.bat`.
> Riêng `.env` thì cần mở **một lần duy nhất** nếu muốn dùng 2 nút ⚡ — hướng dẫn ở **mục 7**.

---

## 10. Nếu chuyển sang máy khác

Tool đã cài sẵn trên máy này. Nếu muốn dùng ở **máy công ty**, cần cài lại thư viện (làm 1 lần):

```
cd /d "đường_dẫn_tới_thư_mục_yt_lyrics" && "đường_dẫn_python" -m pip install -r requirements.txt
```

Nhờ **Trợ lý** làm giúp bước này — Đại chỉ cần mở máy và nói "cài tool lời bài hát".
