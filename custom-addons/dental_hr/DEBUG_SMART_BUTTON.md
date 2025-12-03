# Debug: Smart Button "Lương" Không Hiển Thị

## 🔍 Các Nguyên Nhân Có Thể

### 1. Button Bị Ẩn Do `invisible` (Đã Sửa)
- **Trước đây**: Button có `invisible="salary_count == 0"` nên bị ẩn khi chưa có lương
- **Đã sửa**: Đã xóa `invisible` attribute, button sẽ luôn hiển thị (hiển thị 0 khi chưa có lương)

### 2. XPath Selector Không Tìm Thấy `button_box`
- **Vấn đề**: XPath selector có thể không tìm thấy `button_box` trong view gốc của Odoo 17
- **Đã sửa**: Đã thử cả hai selector:
  - `//div[@name='button_box']`
  - `//div[hasclass('oe_button_box')]`

### 3. User Không Có Quyền HR
- **Vấn đề**: Button có `groups="hr.group_hr_user"` nên chỉ hiển thị cho user có quyền HR
- **Giải pháp**: Đảm bảo user có quyền **HR Officer** hoặc **HR Manager**

### 4. View Inheritance Không Hoạt Động
- **Vấn đề**: View inheritance có thể không được load đúng
- **Giải pháp**: Kiểm tra view trong Technical menu

---

## ✅ Các Bước Kiểm Tra

### Bước 1: Kiểm Tra Quyền User
1. Vào **Settings** → **Users & Companies** → **Users**
2. Chọn user hiện tại
3. Kiểm tra tab **Access Rights**
4. Đảm bảo có quyền **HR / Officer** hoặc **HR / Manager**

### Bước 2: Kiểm Tra View Inheritance
1. Vào **Settings** → **Technical** → **User Interface** → **Views**
2. Tìm view: `hr.employee.form.dental`
3. Kiểm tra:
   - `inherit_id` = `hr.view_employee_form`
   - `arch` có chứa smart button không
   - View có bị inactive không

### Bước 3: Kiểm Tra View Gốc
1. Vào **Settings** → **Technical** → **User Interface** → **Views**
2. Tìm view: `hr.view_employee_form`
3. Kiểm tra xem view gốc có `button_box` không:
   - Mở view trong edit mode
   - Tìm `button_box` hoặc `oe_button_box` trong XML

### Bước 4: Restart Odoo và Clear Cache
1. Restart Odoo server
2. Clear browser cache (Ctrl+Shift+Delete)
3. Refresh browser (Ctrl+F5)
4. Kiểm tra lại

### Bước 5: Upgrade Module
1. Vào **Apps**
2. Tìm module **"Dental HR Management"**
3. Click **Upgrade** (nếu có)
4. Đợi upgrade hoàn thành
5. Refresh browser

---

## 🔧 Giải Pháp Thay Thế

Nếu XPath selector không hoạt động, có thể thử cách khác:

### Cách 1: Thêm Button Vào Header
Thay vì thêm vào `button_box`, có thể thêm vào `header`:

```xml
<xpath expr="//header" position="inside">
    <button name="action_view_salaries" 
            type="object" 
            string="Lương"
            class="oe_stat_button"
            icon="fa-money"
            groups="hr.group_hr_user">
        <field name="salary_count" widget="statinfo" string="Lần tính lương"/>
    </button>
</xpath>
```

### Cách 2: Tạo Button Box Mới
Nếu `button_box` không tồn tại, có thể tạo mới:

```xml
<xpath expr="//sheet" position="before">
    <div class="oe_button_box" name="button_box">
        <button name="action_view_salaries" 
                type="object" 
                string="Lương"
                class="oe_stat_button"
                icon="fa-money"
                groups="hr.group_hr_user">
            <field name="salary_count" widget="statinfo" string="Lần tính lương"/>
        </button>
    </div>
</xpath>
```

---

## 📝 Kiểm Tra Nhanh

### Checklist:
- [ ] User có quyền HR Officer/Manager?
- [ ] View `hr.employee.form.dental` tồn tại?
- [ ] View có `inherit_id` đúng?
- [ ] View gốc `hr.view_employee_form` có `button_box`?
- [ ] Module đã được upgrade?
- [ ] Đã restart Odoo và clear cache?

---

## 🚨 Nếu Vẫn Không Thấy

1. **Kiểm tra Odoo Log**:
   - Xem log Odoo server có lỗi gì không
   - Tìm các lỗi liên quan đến view inheritance

2. **Kiểm tra Developer Mode**:
   - Bật Developer Mode (Settings → Activate Developer Mode)
   - Vào form nhân viên
   - Click **Edit View** để xem cấu trúc view
   - Kiểm tra xem có `button_box` không

3. **Thử Tạo Button Mới**:
   - Sử dụng Developer Mode
   - Tạo button mới trực tiếp trong view
   - Kiểm tra xem có hoạt động không

---

## 💡 Lưu Ý

- **Button sẽ hiển thị 0** khi chưa có lương (Phase 1)
- **Button sẽ hiển thị số lượng** sau khi Phase 3 được triển khai
- **Button chỉ hiển thị cho user có quyền HR**

---

## 📞 Hỗ Trợ

Nếu vẫn gặp vấn đề, vui lòng cung cấp:
1. Screenshot form nhân viên (không thấy button)
2. Screenshot view `hr.employee.form.dental` trong Technical menu
3. Odoo log errors (nếu có)
4. Quyền của user hiện tại

