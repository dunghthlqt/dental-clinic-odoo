# Hướng Dẫn Lưu Website Odoo

## 📋 Tổng Quan

Website trong Odoo được lưu **tự động** trong database. Mỗi khi bạn chỉnh sửa qua Website Builder, thay đổi được lưu ngay vào database. Tuy nhiên, để **backup** hoặc **chuyển website** sang server khác, bạn cần thực hiện các bước sau.

---

## 🔄 Website Được Lưu Tự Động

### ✅ Điều Gì Được Lưu Tự Động?

Khi bạn chỉnh sửa website qua Website Builder, các thay đổi được lưu **ngay lập tức** vào database:

- ✅ **Pages** (Trang): Nội dung, layout, building blocks
- ✅ **Menus** (Menu): Cấu trúc menu, links
- ✅ **Theme Settings**: Màu sắc, fonts, logo, favicon
- ✅ **Building Blocks**: Các khối đã tạo và tùy chỉnh
- ✅ **Media Files**: Hình ảnh, video đã upload
- ✅ **Forms**: Form liên hệ, form đăng ký
- ✅ **SEO Settings**: Meta tags, URL, sitemap
- ✅ **Translations**: Nội dung đa ngôn ngữ

### ⚠️ Lưu Ý Quan Trọng

- **Không cần nhấn "Save"**: Website được lưu tự động
- **Không có file riêng**: Website không được lưu thành file HTML/CSS riêng
- **Lưu trong database**: Tất cả nằm trong PostgreSQL database
- **Backup database = Backup website**: Backup database là cách tốt nhất

---

## 💾 Các Cách Lưu/Backup Website

### Cách 1: Backup Toàn Bộ Database (Khuyến Nghị) ⭐

**Ưu điểm:**
- ✅ Backup toàn bộ website + tất cả dữ liệu
- ✅ Dễ restore (chỉ cần restore database)
- ✅ Giữ nguyên 100% website
- ✅ Bao gồm cả media files, settings, translations

**Cách thực hiện:**

#### Option A: Qua Odoo Interface (Nếu có quyền Admin)

1. Vào **Settings** → **Database Management** (hoặc **Technical** → **Database Structure**)
2. Tìm option **Backup Database** hoặc **Export Database**
3. Chọn **Full Backup** hoặc **Database Dump**
4. Download file backup (thường là `.dump` hoặc `.sql`)

#### Option B: Qua PostgreSQL Command Line

```bash
# Backup database
pg_dump -U odoo -d database_name > backup_website.dump

# Hoặc backup với format custom (nhỏ hơn)
pg_dump -U odoo -Fc database_name > backup_website.dump
```

#### Option C: Qua phpPgAdmin hoặc pgAdmin (GUI Tool)

1. Mở phpPgAdmin hoặc pgAdmin
2. Chọn database của Odoo
3. Right-click → **Backup** hoặc **Export**
4. Chọn format và download

**Khi nào dùng:**
- ✅ Backup định kỳ (hàng ngày/tuần)
- ✅ Trước khi update Odoo
- ✅ Trước khi thay đổi lớn
- ✅ Chuyển website sang server khác

---

### Cách 2: Export Theme Module (Nếu Có Custom Theme)

**Khi nào dùng:**
- Bạn đã tùy chỉnh theme (custom CSS, custom templates)
- Muốn tái sử dụng theme cho website khác
- Muốn version control theme (Git)

**Cách thực hiện:**

1. Vào **Website** → **Theme** → **Customize**
2. Tùy chỉnh theme (màu sắc, fonts, layout)
3. Vào **Apps** → Tìm theme đang dùng
4. Export theme thành module (nếu có option)
5. Hoặc tạo module mới chứa custom theme

**Lưu ý:**
- ⚠️ Chỉ export được **theme settings**, không export **pages content**
- ⚠️ Cần có kiến thức về Odoo module development
- ⚠️ Theme mặc định không cần export (đã có sẵn)

---

### Cách 3: Export Pages Content (Thủ Công)

**Khi nào dùng:**
- Chỉ muốn backup nội dung pages
- Muốn copy nội dung sang website khác
- Không có quyền backup database

**Cách thực hiện:**

1. Vào **Website** → **Pages**
2. Mở từng page cần backup
3. Copy nội dung (text, HTML)
4. Lưu vào file Word/Google Docs
5. Download hình ảnh về máy

**Lưu ý:**
- ⚠️ Mất thời gian (phải làm thủ công từng page)
- ⚠️ Không backup được theme, menu structure
- ⚠️ Không backup được media files tự động

---

### Cách 4: Screenshot Website (Tạm Thời)

**Khi nào dùng:**
- Chỉ cần tham khảo layout
- Backup nhanh để xem lại sau

**Cách thực hiện:**

1. Mở website trên browser
2. Chụp màn hình từng trang
3. Lưu vào folder

**Lưu ý:**
- ⚠️ Chỉ để tham khảo, không restore được
- ⚠️ Không backup được nội dung, chỉ có hình ảnh

---

## 🔧 Cách Restore Website

### Restore Từ Database Backup

1. **Stop Odoo service**
2. **Restore database:**
   ```bash
   # Restore từ file dump
   pg_restore -U odoo -d database_name backup_website.dump
   
   # Hoặc từ SQL file
   psql -U odoo -d database_name < backup_website.sql
   ```
3. **Start Odoo service**
4. **Kiểm tra website**: Mở browser và kiểm tra

### Restore Từ Theme Module

1. Copy theme module vào `addons_path`
2. Update Apps List trong Odoo
3. Install theme module
4. Apply theme cho website

---

## 📝 Checklist Backup Website

### Trước Khi Backup

- [ ] Xác định database name
- [ ] Kiểm tra quyền truy cập database
- [ ] Chọn phương pháp backup phù hợp
- [ ] Xác định nơi lưu file backup

### Khi Backup

- [ ] Backup database (nếu có quyền)
- [ ] Export theme (nếu có custom theme)
- [ ] Ghi chép cấu trúc menu (tên menu, URL)
- [ ] Download media files quan trọng (logo, hình ảnh)

### Sau Khi Backup

- [ ] Kiểm tra file backup có tồn tại
- [ ] Test restore trên môi trường test (nếu có)
- [ ] Lưu file backup ở nhiều nơi (local, cloud, external drive)
- [ ] Ghi chép thông tin backup (ngày, version, database name)

---

## 🎯 Khuyến Nghị

### Cho Người Mới Bắt Đầu

1. **Sử dụng Database Backup** (Cách 1)
   - Đơn giản nhất
   - Backup toàn bộ
   - Dễ restore

2. **Backup định kỳ**
   - Hàng ngày: Nếu website thay đổi nhiều
   - Hàng tuần: Nếu website ít thay đổi
   - Trước khi update: Luôn backup trước khi update Odoo

3. **Lưu ở nhiều nơi**
   - Local computer
   - Cloud storage (Google Drive, Dropbox)
   - External drive

### Cho Developer

1. **Version Control Theme**
   - Export theme thành module
   - Commit vào Git
   - Tag version cho mỗi thay đổi lớn

2. **Automated Backup**
   - Setup cron job để backup tự động
   - Lưu backup với timestamp
   - Xóa backup cũ (giữ lại 7-30 ngày)

3. **Documentation**
   - Ghi chép cấu trúc website
   - Lưu lại screenshots quan trọng
   - Document customizations

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Website Không Phải File

- Website **KHÔNG** được lưu thành file HTML/CSS riêng
- Website được lưu trong **database**
- Muốn backup website → Backup database

### 2. Media Files

- Hình ảnh, video được lưu trong database (dạng binary) hoặc file system
- Khi backup database, media files cũng được backup
- Nếu media files lưu ở file system riêng, cần backup thêm folder `filestore`

### 3. Custom Code

- Nếu có custom code (Python, JavaScript, CSS)
- Cần backup cả **module code** (trong `addons_path`)
- Database backup **KHÔNG** bao gồm custom code

### 4. Multi-Website

- Nếu có nhiều website trong 1 Odoo instance
- Backup database sẽ backup **tất cả** websites
- Không thể backup riêng từng website (trừ khi export thủ công)

---

## 🔍 Kiểm Tra Website Đã Được Lưu

### Cách 1: Refresh Browser

1. Mở website trên browser
2. Nhấn **F5** hoặc **Ctrl+R** để refresh
3. Nếu thay đổi hiển thị → Đã được lưu

### Cách 2: Mở Trang Khác

1. Mở trang khác trên website
2. Quay lại trang vừa chỉnh sửa
3. Nếu thay đổi còn → Đã được lưu

### Cách 3: Đăng Xuất/Đăng Nhập

1. Đăng xuất khỏi Odoo
2. Đăng nhập lại
3. Mở website → Nếu thay đổi còn → Đã được lưu

### Cách 4: Kiểm Tra Database

1. Vào **Settings** → **Technical** → **Database Structure**
2. Tìm model `website.page` hoặc `ir.ui.view`
3. Kiểm tra records mới được tạo

---

## 📚 Tài Liệu Tham Khảo

- [Odoo Website Documentation](https://www.odoo.com/documentation/17.0/applications/websites.html)
- [Odoo Database Backup](https://www.odoo.com/documentation/17.0/administration/install/backup.html)
- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)

---

## ❓ Câu Hỏi Thường Gặp

### Q: Website có tự động lưu không?

**A:** Có, website được lưu tự động vào database khi bạn chỉnh sửa qua Website Builder.

### Q: Làm sao để backup website?

**A:** Backup database là cách tốt nhất. Có thể backup qua Odoo interface, PostgreSQL command line, hoặc GUI tools.

### Q: Có thể export website thành file HTML không?

**A:** Không, website trong Odoo không phải file HTML tĩnh. Website được render động từ database.

### Q: Làm sao để chuyển website sang server khác?

**A:** 
1. Backup database từ server cũ
2. Restore database vào server mới
3. Cấu hình Odoo trên server mới
4. Update domain/subdomain nếu cần

### Q: Backup database có bao gồm hình ảnh không?

**A:** Có, nếu hình ảnh lưu trong database. Nếu lưu ở file system (`filestore`), cần backup thêm folder đó.

### Q: Có thể backup riêng 1 trang không?

**A:** Không thể backup riêng 1 trang qua database. Có thể copy nội dung thủ công hoặc export page content.

---

*Tài liệu này hướng dẫn cách lưu và backup website trong Odoo. Cập nhật: 2024*

