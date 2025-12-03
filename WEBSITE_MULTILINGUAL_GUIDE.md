# Hướng Dẫn Chỉnh Sửa Website Đa Ngôn Ngữ trong Odoo

## 📋 Vấn Đề

Website Odoo có 2 ngôn ngữ (tiếng Anh và tiếng Việt), nhưng Website Builder chỉ cho phép chỉnh sửa trang tiếng Anh. Làm sao để:
1. ✅ Chỉnh sửa trang web tiếng Việt
2. ✅ Hoặc chỉ có mỗi tiếng Việt

---

## 🔍 Hiểu Về Đa Ngôn Ngữ trong Odoo Website

### Cách Odoo Xử Lý Đa Ngôn Ngữ

- **Mỗi ngôn ngữ = 1 bản dịch riêng** của cùng 1 page
- **Website Builder chỉ chỉnh sửa ngôn ngữ hiện tại** (ngôn ngữ đang chọn)
- **Cần chuyển đổi ngôn ngữ** trong Website Builder để chỉnh sửa ngôn ngữ khác
- **Ngôn ngữ mặc định** thường là tiếng Anh (en_US)

### Các Thành Phần Có Thể Dịch

- ✅ **Pages** (Trang): Nội dung, tiêu đề, mô tả
- ✅ **Menus** (Menu): Tên menu, links
- ✅ **Building Blocks**: Text trong các khối
- ✅ **Forms**: Labels, placeholders, messages
- ✅ **SEO**: Meta title, meta description
- ⚠️ **Theme Settings**: Màu sắc, fonts (thường không dịch được)
- ⚠️ **Layout**: Cấu trúc trang (thường không dịch được)

---

## 🎯 Giải Pháp 1: Chỉnh Sửa Trang Web Tiếng Việt

### Bước 1: Kích Hoạt Chế Độ Edit Website

1. Mở website trên browser (chưa đăng nhập hoặc đăng nhập với quyền Website Editor)
2. Nhấn nút **"Edit"** hoặc **"✏️"** ở góc trên cùng
3. Website Builder sẽ mở ra

### Bước 2: Chuyển Đổi Ngôn Ngữ Trong Website Builder

#### Cách A: Qua Language Selector (Nếu có)

1. Trong Website Builder, tìm **language selector** (thường ở góc trên bên phải)
2. Click vào **language selector** (có thể hiển thị "EN" hoặc "English")
3. Chọn **"Tiếng Việt"** hoặc **"Vietnamese"** (vi_VN)
4. Website sẽ reload với ngôn ngữ tiếng Việt
5. Bây giờ bạn có thể chỉnh sửa nội dung tiếng Việt

#### Cách B: Qua URL (Nếu không có language selector)

1. Trong Website Builder, xem URL của trang
2. URL thường có dạng: `http://yourdomain.com/page?edit=1`
3. Thêm `/vi` hoặc `?lang=vi_VN` vào URL:
   - `http://yourdomain.com/page?edit=1&lang=vi_VN`
   - Hoặc: `http://yourdomain.com/vi/page?edit=1`
4. Website sẽ reload với ngôn ngữ tiếng Việt
5. Bây giờ bạn có thể chỉnh sửa nội dung tiếng Việt

#### Cách C: Qua Settings → Languages

1. Vào **Settings** → **Languages** (hoặc **Translations** → **Languages**)
2. Đảm bảo **Tiếng Việt (vi_VN)** đã được kích hoạt
3. Quay lại Website Builder
4. Chuyển đổi ngôn ngữ qua language selector hoặc URL

### Bước 3: Chỉnh Sửa Nội Dung Tiếng Việt

1. Sau khi chuyển sang tiếng Việt, bạn sẽ thấy nội dung tiếng Việt (nếu đã có)
2. Click vào các **text blocks** để chỉnh sửa
3. Thay đổi nội dung thành tiếng Việt
4. Nhấn **"Save"** hoặc **"Publish"** (thay đổi được lưu tự động)

### Bước 4: Kiểm Tra

1. Đóng Website Builder (nhấn **"✕"** hoặc **"Close"**)
2. Mở website ở chế độ xem bình thường
3. Chuyển đổi ngôn ngữ sang tiếng Việt
4. Kiểm tra nội dung đã được cập nhật

---

## 🎯 Giải Pháp 2: Chỉ Có Mỗi Tiếng Việt (Tắt Tiếng Anh)

### Option A: Ẩn Language Selector (Đơn Giản)

**Mục đích:** Ẩn language selector để người dùng không thấy option chuyển đổi ngôn ngữ

**Cách thực hiện:**

1. Vào **Website** → **Configuration** → **Settings**
2. Tìm **"Language Selector"** hoặc **"Show Language Selector"**
3. Tắt option này
4. Lưu settings

**Kết quả:**
- ✅ Language selector bị ẩn
- ✅ Người dùng không thấy option chuyển đổi ngôn ngữ
- ⚠️ Vẫn có thể truy cập tiếng Anh qua URL (nếu biết)

### Option B: Xóa Tiếng Anh Khỏi Website (Nâng Cao)

**Mục đích:** Xóa hoàn toàn tiếng Anh, chỉ giữ lại tiếng Việt

**Cách thực hiện:**

1. Vào **Settings** → **Languages**
2. Tìm **"English (en_US)"**
3. **Uninstall** hoặc **Archive** ngôn ngữ tiếng Anh
4. Hoặc xóa tiếng Anh khỏi danh sách ngôn ngữ của website

**Lưu ý:**
- ⚠️ Cần cẩn thận: Có thể ảnh hưởng đến backend (admin panel)
- ⚠️ Nên test trên môi trường test trước
- ⚠️ Backup database trước khi thực hiện

### Option C: Set Tiếng Việt Làm Ngôn Ngữ Mặc Định

**Mục đích:** Khi người dùng truy cập website, tự động hiển thị tiếng Việt

**Cách thực hiện:**

1. Vào **Settings** → **Languages**
2. Tìm **"Default Language"** hoặc **"Website Default Language"**
3. Chọn **"Tiếng Việt (vi_VN)"**
4. Lưu settings

**Kết quả:**
- ✅ Website mặc định hiển thị tiếng Việt
- ✅ Người dùng vẫn có thể chuyển sang tiếng Anh (nếu có language selector)
- ✅ URL mặc định sẽ là `/vi/` thay vì `/en/`

---

## 🔧 Cách Cấu Hình Ngôn Ngữ Website

### Bước 1: Kiểm Tra Ngôn Ngữ Đã Cài

1. Vào **Settings** → **Languages** (hoặc **Translations** → **Languages**)
2. Kiểm tra danh sách ngôn ngữ:
   - ✅ **English (en_US)** - Đã cài
   - ✅ **Tiếng Việt (vi_VN)** - Đã cài
3. Nếu chưa có tiếng Việt:
   - Click **"Create"** hoặc **"Install Language"**
   - Chọn **"Vietnamese"** hoặc **"Tiếng Việt"**
   - Install language

### Bước 2: Cấu Hình Ngôn Ngữ Cho Website

1. Vào **Website** → **Configuration** → **Settings**
2. Tìm section **"Languages"** hoặc **"Localization"**
3. Cấu hình:
   - **Default Language**: Chọn tiếng Việt (nếu muốn)
   - **Available Languages**: Chọn tiếng Anh và tiếng Việt
   - **Language Selector**: Bật/tắt tùy ý

### Bước 3: Kiểm Tra Translation Status

1. Vào **Translations** → **Translated Terms**
2. Tìm các terms chưa được dịch
3. Dịch các terms còn thiếu

---

## 📝 Hướng Dẫn Chi Tiết: Chỉnh Sửa Nội Dung Tiếng Việt

### Scenario 1: Chỉnh Sửa Text Trong Page

1. **Mở Website Builder** (nhấn nút Edit)
2. **Chuyển sang tiếng Việt** (qua language selector hoặc URL)
3. **Click vào text block** cần chỉnh sửa
4. **Sửa nội dung** thành tiếng Việt
5. **Click ra ngoài** hoặc nhấn **Enter** → Tự động lưu

### Scenario 2: Thêm Nội Dung Mới Bằng Tiếng Việt

1. **Mở Website Builder** (nhấn nút Edit)
2. **Chuyển sang tiếng Việt** (qua language selector hoặc URL)
3. **Thêm building block mới** (Text, Image, etc.)
4. **Nhập nội dung tiếng Việt**
5. **Lưu** (tự động)

### Scenario 3: Chỉnh Sửa Menu Tiếng Việt

1. Vào **Website** → **Configuration** → **Menus**
2. Tìm menu cần chỉnh sửa
3. Click vào menu
4. Trong form, tìm field **"Name"** hoặc **"Label"**
5. Chỉnh sửa tên menu (có thể có nhiều ngôn ngữ)
6. Hoặc vào **Translations** để dịch menu

### Scenario 4: Chỉnh Sửa Form Labels

1. Vào **Website** → **Pages**
2. Tìm page có form
3. Mở page trong **Edit mode**
4. Click vào form field
5. Chỉnh sửa label (có thể có nhiều ngôn ngữ)
6. Hoặc vào **Translations** để dịch form labels

---

## 🛠️ Troubleshooting

### Vấn Đề 1: Không Thấy Language Selector

**Nguyên nhân:**
- Language selector bị ẩn trong settings
- Chưa cài đặt module website đa ngôn ngữ

**Giải pháp:**
1. Vào **Settings** → **Languages**
2. Kiểm tra có ít nhất 2 ngôn ngữ được cài
3. Vào **Website** → **Configuration** → **Settings**
4. Bật **"Show Language Selector"**

### Vấn Đề 2: Chỉnh Sửa Tiếng Việt Nhưng Vẫn Hiển Thị Tiếng Anh

**Nguyên nhân:**
- Đang chỉnh sửa ngôn ngữ sai
- Cache browser
- Chưa publish changes

**Giải pháp:**
1. Kiểm tra đang ở ngôn ngữ nào trong Website Builder (xem language selector)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Đảm bảo đã publish changes
4. Kiểm tra lại URL (có `/vi/` hoặc `?lang=vi_VN`)

### Vấn Đề 3: Không Thể Chuyển Đổi Ngôn Ngữ Trong Website Builder

**Nguyên nhân:**
- Chưa cài đặt ngôn ngữ tiếng Việt
- Không có quyền chỉnh sửa translations

**Giải pháp:**
1. Vào **Settings** → **Languages**
2. Đảm bảo **Tiếng Việt (vi_VN)** đã được cài
3. Kiểm tra quyền user (cần quyền Website Editor hoặc Admin)
4. Thử truy cập qua URL: `?lang=vi_VN`

### Vấn Đề 4: Một Số Nội Dung Không Dịch Được

**Nguyên nhân:**
- Nội dung hard-coded (không phải translatable)
- Nội dung từ module khác chưa được mark là translatable

**Giải pháp:**
1. Kiểm tra nội dung có trong **Translations** → **Translated Terms** không
2. Nếu không có, cần mark field là translatable trong code
3. Hoặc chỉnh sửa trực tiếp trong database (không khuyến nghị)

---

## ✅ Checklist

### Trước Khi Chỉnh Sửa

- [ ] Đã cài đặt ngôn ngữ tiếng Việt (vi_VN)
- [ ] Đã kích hoạt đa ngôn ngữ cho website
- [ ] Đã có quyền Website Editor hoặc Admin
- [ ] Đã backup database (nếu cần)

### Khi Chỉnh Sửa

- [ ] Đã chuyển sang ngôn ngữ tiếng Việt trong Website Builder
- [ ] Đã chỉnh sửa nội dung tiếng Việt
- [ ] Đã kiểm tra nội dung hiển thị đúng
- [ ] Đã publish changes

### Sau Khi Chỉnh Sửa

- [ ] Đã kiểm tra website ở chế độ xem bình thường
- [ ] Đã test chuyển đổi ngôn ngữ
- [ ] Đã kiểm tra trên mobile (nếu cần)
- [ ] Đã kiểm tra SEO (meta tags, URLs)

---

## 🎯 Khuyến Nghị

### Cho Website Chỉ Có Tiếng Việt

1. **Set tiếng Việt làm ngôn ngữ mặc định**
   - Vào Settings → Languages → Default Language → Chọn tiếng Việt

2. **Ẩn language selector** (nếu không cần tiếng Anh)
   - Vào Website → Configuration → Settings → Tắt "Show Language Selector"

3. **Xóa hoặc archive tiếng Anh** (nếu chắc chắn không cần)
   - Vào Settings → Languages → Uninstall English (cẩn thận!)

### Cho Website Đa Ngôn Ngữ

1. **Giữ cả 2 ngôn ngữ**
   - Tiếng Việt làm mặc định
   - Tiếng Anh làm ngôn ngữ phụ

2. **Hiển thị language selector**
   - Để người dùng dễ chuyển đổi

3. **Dịch đầy đủ nội dung**
   - Đảm bảo tất cả pages, menus, forms đều có bản dịch

---

## 📚 Tài Liệu Tham Khảo

- [Odoo Website Multilingual](https://www.odoo.com/documentation/17.0/applications/websites/website/translate.html)
- [Odoo Translation Guide](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#translatable-fields)
- [Odoo Language Configuration](https://www.odoo.com/documentation/17.0/applications/general/localization/languages.html)

---

## ❓ Câu Hỏi Thường Gặp

### Q: Làm sao để chỉnh sửa trang web tiếng Việt?

**A:** 
1. Mở Website Builder (nhấn nút Edit)
2. Chuyển đổi ngôn ngữ sang tiếng Việt (qua language selector hoặc URL)
3. Chỉnh sửa nội dung tiếng Việt
4. Lưu (tự động)

### Q: Tại sao Website Builder chỉ cho phép chỉnh sửa tiếng Anh?

**A:** Website Builder chỉ chỉnh sửa ngôn ngữ hiện tại. Bạn cần chuyển đổi ngôn ngữ sang tiếng Việt trước khi chỉnh sửa.

### Q: Làm sao để website chỉ có tiếng Việt?

**A:** 
1. Set tiếng Việt làm ngôn ngữ mặc định
2. Ẩn language selector
3. (Tùy chọn) Xóa tiếng Anh khỏi website

### Q: Có thể tắt tiếng Anh hoàn toàn không?

**A:** Có, nhưng cần cẩn thận vì có thể ảnh hưởng đến backend. Nên test trên môi trường test trước.

### Q: Làm sao để set tiếng Việt làm ngôn ngữ mặc định?

**A:** Vào Settings → Languages → Default Language → Chọn Tiếng Việt (vi_VN)

### Q: Một số nội dung không dịch được, tại sao?

**A:** Có thể nội dung đó hard-coded hoặc chưa được mark là translatable. Cần kiểm tra trong Translations hoặc chỉnh sửa code.

---

*Tài liệu này hướng dẫn cách chỉnh sửa website đa ngôn ngữ trong Odoo. Cập nhật: 2024*

