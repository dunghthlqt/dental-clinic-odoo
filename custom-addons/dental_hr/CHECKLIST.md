# Checklist Kiểm Tra Module Dental HR

## ✅ Kiểm Tra Cài Đặt Module

### 1. Module đã được cài đặt chưa?
- [ ] Vào **Apps** → Tìm "Dental HR Management"
- [ ] Kiểm tra trạng thái: Phải là **Installed** (Đã cài đặt)
- [ ] Nếu chưa cài: Click **Install**

### 2. Module đã được upgrade chưa?
- [ ] Nếu đã cài nhưng không thấy menu/fields:
  - Vào **Apps** → Tìm "Dental HR Management"
  - Click **Upgrade** (nếu có nút này)

### 3. Restart Odoo Server
- [ ] Sau khi cài/upgrade, restart Odoo server
- [ ] Clear browser cache (Ctrl+F5 hoặc Cmd+Shift+R)

---

## ✅ Kiểm Tra Menu

### Menu "Nha khoa" trong HR app
- [ ] Vào **Nhân sự** (Employees) ở menu trên cùng
- [ ] Tìm menu **Nha khoa** (Dental) - nằm ở cuối danh sách menu trong HR app
- [ ] Click vào **Nha khoa** → Phải thấy sub-menu **Vai trò**

**Nếu không thấy menu:**
- Kiểm tra user có quyền `hr.group_hr_user` hoặc `hr.group_hr_manager`
- Vào **Settings** → **Users & Companies** → **Users** → Mở user của bạn
- Tab **Access Rights** → Kiểm tra có quyền "Human Resources / Officer" hoặc "Human Resources / Manager"

---

## ✅ Kiểm Tra Tab "Thông tin Nha khoa" trong Form Nhân Viên

### Cách kiểm tra:
1. Vào **Nhân sự** → **Nhân viên** (Employees)
2. Mở một nhân viên bất kỳ (ví dụ: Administrator)
3. Cuộn xuống các tabs ở dưới
4. Tìm tab **Thông tin Nha khoa**

**Nếu không thấy tab:**
- Kiểm tra module đã được cài đặt và upgrade chưa
- Restart Odoo server
- Clear browser cache
- Kiểm tra user có quyền `hr.group_hr_user`

**Trong tab "Thông tin Nha khoa" phải có:**
- [ ] Field **Vai trò** (dental_roles) - Many2many tags
- [ ] Field **Chuyên khoa** (dental_specialty) - Selection
- [ ] Field **Số năm kinh nghiệm** (years_of_experience) - Integer
- [ ] Field **Bằng cấp/Chứng chỉ** (certifications) - Text

---

## ✅ Kiểm Tra Smart Button "Lương"

### Cách kiểm tra:
1. Mở form nhân viên
2. Ở góc trên bên phải, tìm smart button **Lương**

**Lưu ý:**
- Button sẽ **ẩn** khi `salary_count = 0` (hiện tại Phase 1, chưa có lương)
- Button sẽ hiển thị sau khi Phase 3 được triển khai và có lương

---

## ✅ Kiểm Tra Menu "Vai trò"

### Cách kiểm tra:
1. Vào **Nhân sự** → **Nha khoa** → **Vai trò**
2. Phải thấy danh sách 5 vai trò mặc định:
   - [ ] Bác sĩ (doctor)
   - [ ] Kỹ thuật viên (technician)
   - [ ] Lễ tân (receptionist)
   - [ ] Kế toán (accountant)
   - [ ] Quản lý kho (inventory_manager)

**Nếu không thấy menu "Vai trò":**
- Kiểm tra menu "Nha khoa" có hiển thị không
- Kiểm tra action `action_dental_role` có được tạo đúng không
- Kiểm tra user có quyền `hr.group_hr_user`

---

## 🔍 Debug Steps

### Nếu không thấy bất kỳ tính năng nào:

1. **Kiểm tra Module Installation:**
   ```bash
   # Trong Odoo shell hoặc log
   # Kiểm tra module có trong danh sách installed modules không
   ```

2. **Kiểm tra View Inheritance:**
   - Vào **Settings** → **Technical** → **User Interface** → **Views**
   - Tìm view: `hr.employee.form.dental`
   - Kiểm tra `inherit_id` = `hr.view_employee_form`
   - Kiểm tra `arch` có đúng không

3. **Kiểm tra Menu:**
   - Vào **Settings** → **Technical** → **User Interface** → **Menu Items**
   - Tìm menu: `menu_dental_hr_root`
   - Kiểm tra `parent` = `hr.menu_hr_root`
   - Kiểm tra `groups` có đúng không

4. **Kiểm tra Model:**
   - Vào **Settings** → **Technical** → **Database Structure** → **Models**
   - Tìm model: `dental.role`
   - Kiểm tra model có tồn tại không

5. **Kiểm tra Access Rights:**
   - Vào **Settings** → **Technical** → **Security** → **Access Rights**
   - Tìm access rights cho `dental.role`
   - Kiểm tra user có quyền đọc không

---

## 🐛 Common Issues

### Issue 1: Menu không hiển thị
**Nguyên nhân:**
- Module chưa được cài đặt
- User không có quyền `hr.group_hr_user`
- Menu bị ẩn do groups

**Giải pháp:**
- Cài đặt/upgrade module
- Cấp quyền HR Officer hoặc HR Manager cho user
- Restart Odoo

### Issue 2: Tab "Thông tin Nha khoa" không hiển thị
**Nguyên nhân:**
- View inheritance không hoạt động
- Module chưa được upgrade
- Browser cache

**Giải pháp:**
- Upgrade module
- Restart Odoo
- Clear browser cache (Ctrl+F5)

### Issue 3: Không thể tạo/sửa vai trò
**Nguyên nhân:**
- User không có quyền `dental_hr.group_dental_hr_manager`

**Giải pháp:**
- Cấp quyền "Quản lý nhân sự nha khoa" cho user
- Hoặc cấp quyền HR Manager (vì `group_dental_hr_manager` có `implied_ids` = `hr.group_hr_manager`)

---

## ✅ Quick Test

Sau khi cài đặt module, thử các bước sau:

1. **Test Menu:**
   - Vào **Nhân sự** → **Nha khoa** → **Vai trò**
   - Phải thấy 5 vai trò mặc định

2. **Test Form Nhân Viên:**
   - Vào **Nhân sự** → **Nhân viên**
   - Mở một nhân viên
   - Tìm tab **Thông tin Nha khoa**
   - Thử gán vai trò "Bác sĩ" cho nhân viên
   - Lưu và kiểm tra vai trò được lưu đúng

3. **Test Vai Trò:**
   - Vào **Nhân sự** → **Nha khoa** → **Vai trò**
   - Mở vai trò "Bác sĩ"
   - Kiểm tra tab **Nhân viên** hiển thị nhân viên vừa gán

---

**Nếu vẫn không thấy, vui lòng cung cấp:**
1. Screenshot màn hình
2. Odoo log errors (nếu có)
3. Trạng thái module (Installed/Upgrade)
4. Quyền của user hiện tại

