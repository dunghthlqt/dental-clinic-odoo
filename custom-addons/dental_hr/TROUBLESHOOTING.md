# Troubleshooting - Module Không Hiển Thị Trong Apps

## 🔍 Nguyên Nhân Có Thể

### 1. Module Chưa Được Odoo Discover
**Triệu chứng**: Module không xuất hiện trong Apps sau khi tạo

**Giải pháp**:
1. Vào **Apps**
2. Click **"Update Apps List"** (ở thanh menu trên cùng)
3. Đợi Odoo quét lại các module (có thể mất vài giây đến vài phút)
4. Sau đó tìm kiếm: "Dental HR" hoặc "dental_hr"

### 2. Module Bị Filter Ra
**Triệu chứng**: Module không hiển thị khi search "dental"

**Giải pháp**:
1. Xóa tất cả filters (click X trên các tags)
2. Tìm kiếm: "HR Management" hoặc "dental_hr"
3. Hoặc lọc theo category: "Human Resources"

### 3. Dependencies Chưa Được Cài Đặt
**Triệu chứng**: Module không thể cài đặt do thiếu dependencies

**Giải pháp**:
Module `dental_hr` cần các dependencies sau:
- `base` (luôn có sẵn)
- `hr` (module HR gốc của Odoo)
- `hr_contract` (hợp đồng lao động)
- `account` (kế toán)

Nếu thiếu, cài đặt các module này trước.

### 4. Addons Path Không Đúng
**Triệu chứng**: Odoo không tìm thấy module trong thư mục

**Giải pháp**:
1. Kiểm tra file config Odoo (thường là `/home/dung/odoo/odoo.conf`)
2. Đảm bảo `addons_path` bao gồm `/home/dung/dental-clinic-odoo/custom-addons`
3. Restart Odoo server

### 5. Lỗi Syntax Trong Module
**Triệu chứng**: Module không load được, có lỗi trong log

**Giải pháp**:
1. Kiểm tra Odoo log để xem lỗi cụ thể
2. Kiểm tra syntax của các file Python và XML
3. Sửa lỗi và restart Odoo

---

## ✅ Checklist Kiểm Tra

- [ ] Module đã được tạo trong thư mục `/home/dung/dental-clinic-odoo/custom-addons/dental_hr`
- [ ] File `__manifest__.py` tồn tại và có syntax đúng
- [ ] File `__init__.py` tồn tại
- [ ] Đã click **"Update Apps List"** trong Apps
- [ ] Đã xóa filters và tìm kiếm lại
- [ ] Dependencies (`hr`, `hr_contract`, `account`) đã được cài đặt
- [ ] Addons path đúng trong Odoo config
- [ ] Đã restart Odoo server sau khi tạo module

---

## 🚀 Các Bước Khắc Phục

### Bước 1: Update Apps List
1. Vào **Apps**
2. Click **"Update Apps List"**
3. Đợi hoàn thành

### Bước 2: Tìm Kiếm Module
1. Xóa tất cả filters
2. Tìm kiếm: "Dental HR" hoặc "dental_hr"
3. Hoặc tìm kiếm: "HR Management"

### Bước 3: Kiểm Tra Log
Nếu vẫn không thấy, kiểm tra Odoo log:
```bash
# Xem log Odoo để tìm lỗi
tail -f /path/to/odoo.log | grep -i "dental_hr\|error\|warning"
```

### Bước 4: Kiểm Tra Addons Path
```bash
# Kiểm tra file config
cat /home/dung/odoo/odoo.conf | grep addons_path
```

Đảm bảo có: `/home/dung/dental-clinic-odoo/custom-addons`

---

## 📝 Lưu Ý

- Module `dental_hr` có `application: False`, nghĩa là nó không phải là app chính, chỉ là module mở rộng
- Module sẽ hiển thị trong Apps nhưng không có icon riêng (sẽ dùng icon mặc định)
- Sau khi cài đặt, module sẽ tích hợp vào HR app, không tạo app riêng

---

## 🔧 Nếu Vẫn Không Thấy

Vui lòng cung cấp:
1. Screenshot màn hình Apps (sau khi Update Apps List)
2. Odoo log errors (nếu có)
3. Nội dung file `/home/dung/odoo/odoo.conf` (phần addons_path)

