# Hướng Dẫn Bổ Sung Thông Tin Dental HR Cho Nhân Viên

## 📋 Tổng Quan

Nếu bạn đã tạo nhân viên trong **Settings → Users** trước khi cài đặt module `dental_hr`, bạn có thể bổ sung thông tin dental HR cho những nhân viên đó.

---

## 🚀 Các Bước Thực Hiện

### Bước 1: Truy Cập Danh Sách Nhân Viên

1. Vào app **Nhân sự** (HR) trong Odoo
2. Click vào menu **Nhân viên** (Employees)
3. Bạn sẽ thấy danh sách tất cả nhân viên đã tạo

### Bước 2: Mở Form Nhân Viên

1. Tìm và click vào nhân viên cần bổ sung thông tin
2. Form nhân viên sẽ mở ra

### Bước 3: Bổ Sung Thông Tin Dental HR

1. Trong form nhân viên, tìm tab **"Thông tin Nha khoa"** (ở cuối các tabs)
2. Click vào tab này
3. Điền các thông tin sau:

#### **Vai trò và Chuyên môn:**
- **Vai trò** (`dental_roles`): 
  - Chọn một hoặc nhiều vai trò từ danh sách (Bác sĩ, Kỹ thuật viên, Lễ tân, Kế toán, Quản lý kho)
  - Có thể chọn nhiều vai trò (ví dụ: Kế toán kiêm Quản lý kho)
  
- **Chuyên khoa** (`dental_specialty`): 
  - Chỉ áp dụng cho bác sĩ
  - Chọn từ danh sách: Niềng răng, Cấy ghép, Tẩy trắng, Trám răng, Nhổ răng, Tổng quát, Khác
  
- **Số năm kinh nghiệm** (`years_of_experience`):
  - Nhập số năm kinh nghiệm trong ngành nha khoa

#### **Bằng cấp:**
- **Bằng cấp/Chứng chỉ** (`certifications`):
  - Nhập bằng cấp và chứng chỉ của nhân viên (ví dụ: "Bác sĩ Răng Hàm Mặt - Đại học Y Hà Nội, Chứng chỉ Implant - ICOI")

### Bước 4: Lưu Thông Tin

1. Click nút **Lưu** (Save) ở góc trên bên trái
2. Thông tin đã được lưu

---

## 📝 Ví Dụ Cụ Thể

### Ví dụ 1: Bác sĩ
- **Vai trò**: Bác sĩ
- **Chuyên khoa**: Niềng răng
- **Số năm kinh nghiệm**: 10
- **Bằng cấp/Chứng chỉ**: "Bác sĩ Răng Hàm Mặt - Đại học Y Hà Nội, Chứng chỉ Niềng răng Invisalign"

### Ví dụ 2: Kế toán kiêm Quản lý kho
- **Vai trò**: Kế toán, Quản lý kho
- **Chuyên khoa**: (để trống)
- **Số năm kinh nghiệm**: 5
- **Bằng cấp/Chứng chỉ**: "Cử nhân Kế toán - Đại học Kinh tế, Chứng chỉ Quản lý kho"

### Ví dụ 3: Lễ tân
- **Vai trò**: Lễ tân
- **Chuyên khoa**: (để trống)
- **Số năm kinh nghiệm**: 2
- **Bằng cấp/Chứng chỉ**: "Trung cấp Hành chính văn phòng"

---

## ⚠️ Lưu Ý

1. **Tab "Thông tin Nha khoa" chỉ hiển thị cho user có quyền HR** (`hr.group_hr_user`)
   - Nếu không thấy tab, kiểm tra quyền của user hiện tại

2. **Vai trò có thể chọn nhiều**:
   - Một nhân viên có thể có nhiều vai trò
   - Ví dụ: Kế toán có thể kiêm Quản lý kho

3. **Chuyên khoa chỉ áp dụng cho bác sĩ**:
   - Các vai trò khác (Kỹ thuật viên, Lễ tân, Kế toán, Quản lý kho) không cần điền chuyên khoa

4. **Smart button "Lương"**:
   - Ở góc trên bên phải form nhân viên, có smart button "Lương"
   - Button này sẽ ẩn khi chưa có lương (Phase 1)
   - Sẽ hiển thị sau khi Phase 3 được triển khai

---

## 🔍 Nếu Không Thấy Tab "Thông tin Nha khoa"

### Kiểm tra 1: Quyền User
- User phải có quyền **HR Officer** hoặc **HR Manager**
- Vào **Settings → Users & Companies → Users**
- Chọn user hiện tại
- Kiểm tra tab **Access Rights**
- Đảm bảo có quyền **HR / Officer** hoặc **HR / Manager**

### Kiểm tra 2: Module đã được cài đặt
- Vào **Apps**
- Tìm module **"Dental HR Management"**
- Đảm bảo trạng thái là **"Installed"**

### Kiểm tra 3: Restart Odoo
- Nếu vừa cài đặt module, thử restart Odoo server
- Sau đó refresh browser (Ctrl+F5)

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. File `TESTING_GUIDE.md` - Hướng dẫn testing chi tiết
2. File `TROUBLESHOOTING.md` - Khắc phục sự cố
3. File `CHECKLIST.md` - Checklist kiểm tra module

