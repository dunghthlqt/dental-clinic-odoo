# Khắc Phục: Chỉ Hiển Thị 1 Nhân Viên Trong Danh Sách

## 🔍 Nguyên Nhân

Khi bạn tạo user trong **Settings → Users**, Odoo thường tự động tạo một `hr.employee` record. Tuy nhiên, có một số trường hợp nhân viên không xuất hiện:

1. **User chưa có employee record**: User được tạo nhưng chưa có employee record tương ứng
2. **Filter đang được áp dụng**: Có filter đang ẩn các nhân viên khác
3. **Employee record bị inactive**: Employee record bị vô hiệu hóa
4. **Quyền truy cập**: User hiện tại không có quyền xem tất cả nhân viên

---

## ✅ Giải Pháp

### Giải Pháp 1: Kiểm Tra và Xóa Filters

1. Vào **Nhân sự** → **Nhân viên**
2. Kiểm tra thanh **Filters** ở trên cùng
3. Xóa tất cả filters đang được áp dụng (click X trên các tags)
4. Kiểm tra lại danh sách

**Lưu ý**: Có thể có filter theo:
- Phòng ban (Department)
- Trạng thái (Active/Inactive)
- Vai trò (nếu đã gán)
- Tìm kiếm (Search)

---

### Giải Pháp 2: Tạo Employee Record Từ User

Nếu user chưa có employee record, bạn cần tạo thủ công:

#### Cách 1: Từ Form User

1. Vào **Settings** → **Users & Companies** → **Users**
2. Mở user cần tạo employee record
3. Trong form user, tìm field **"Employee"** (hoặc **"Nhân viên"**)
4. Nếu field này trống, click vào icon **"Tạo"** hoặc **"Create"** bên cạnh
5. Điền thông tin cơ bản:
   - **Tên** (Name): Tên nhân viên
   - **Phòng ban** (Department): Chọn phòng ban (nếu có)
   - **Công việc** (Job Position): Chọn vị trí công việc (nếu có)
6. Click **Lưu**
7. Employee record sẽ được tạo và link với user

#### Cách 2: Tạo Trực Tiếp Từ HR

1. Vào **Nhân sự** → **Nhân viên**
2. Click nút **Mới** (New)
3. Điền thông tin:
   - **Tên** (Name): Tên nhân viên
   - **User**: Chọn user tương ứng từ danh sách
   - **Phòng ban** (Department): Chọn phòng ban
   - **Công việc** (Job Position): Chọn vị trí công việc
4. Click **Lưu**
5. Employee record sẽ được tạo và link với user

---

### Giải Pháp 3: Kiểm Tra Employee Records Bị Inactive

1. Vào **Nhân sự** → **Nhân viên**
2. Click vào icon **Filters** (biểu tượng lọc)
3. Chọn **"Archived"** hoặc **"Inactive"** để xem các nhân viên bị vô hiệu hóa
4. Nếu thấy nhân viên bị inactive:
   - Mở form nhân viên
   - Bỏ tick **"Active"** (nếu có) hoặc click **"Unarchive"**
   - Click **Lưu**

---

### Giải Pháp 4: Kiểm Tra Quyền Truy Cập

1. Vào **Settings** → **Users & Companies** → **Users**
2. Chọn user hiện tại (user bạn đang đăng nhập)
3. Kiểm tra tab **Access Rights**
4. Đảm bảo user có quyền:
   - **HR / Officer** hoặc **HR / Manager**
   - Hoặc có quyền **"See all employees"**

**Lưu ý**: Nếu user chỉ có quyền **HR / User**, họ chỉ có thể xem nhân viên trong phòng ban của mình.

---

### Giải Pháp 5: Sử Dụng Search View

1. Vào **Nhân sự** → **Nhân viên**
2. Trong ô **Tìm kiếm**, thử tìm kiếm:
   - Tên nhân viên
   - Email của user
   - Mã nhân viên (nếu có)
3. Nếu tìm thấy, nhân viên đã tồn tại nhưng có thể bị filter

---

## 🔧 Kiểm Tra Nhanh

### Checklist:

- [ ] Đã xóa tất cả filters?
- [ ] Đã kiểm tra user có employee record chưa?
- [ ] Đã kiểm tra employee records bị inactive?
- [ ] Đã kiểm tra quyền truy cập của user?
- [ ] Đã thử tìm kiếm tên nhân viên?

---

## 📝 Cách Tạo Employee Record Hàng Loạt (Nếu Cần)

Nếu có nhiều user chưa có employee record, bạn có thể tạo thủ công từng cái một, hoặc:

1. Vào **Settings** → **Technical** → **Database Structure** → **Models**
2. Tìm model **"hr.employee"**
3. Sử dụng **Developer Mode** để tạo records hàng loạt (chỉ dành cho admin)

**Lưu ý**: Cách này yêu cầu kiến thức kỹ thuật. Nên tạo thủ công từng cái một để đảm bảo đúng.

---

## 🚨 Nếu Vẫn Không Thấy

1. **Kiểm tra Odoo Log**:
   - Xem log Odoo server có lỗi gì không
   - Tìm các lỗi liên quan đến `hr.employee`

2. **Kiểm tra Database**:
   - Vào **Settings** → **Technical** → **Database Structure** → **Models**
   - Tìm model **"hr.employee"**
   - Kiểm tra số lượng records

3. **Restart Odoo**:
   - Restart Odoo server
   - Refresh browser (Ctrl+F5)

4. **Kiểm tra Module HR**:
   - Đảm bảo module **HR** (Human Resources) đã được cài đặt
   - Vào **Apps** → Tìm **"Employees"** → Đảm bảo trạng thái là **"Installed"**

---

## 💡 Mẹo

- **Luôn tạo employee record khi tạo user mới**: Khi tạo user trong Settings, nên tạo employee record ngay lập tức
- **Sử dụng filter để quản lý**: Nếu có nhiều nhân viên, sử dụng filters để tìm kiếm dễ dàng hơn
- **Kiểm tra quyền định kỳ**: Đảm bảo user có quyền phù hợp để xem và quản lý nhân viên

---

## 📞 Hỗ Trợ

Nếu vẫn gặp vấn đề, vui lòng cung cấp:
1. Số lượng user đã tạo trong Settings
2. Số lượng employee records hiển thị trong HR
3. Screenshot màn hình danh sách nhân viên (với filters)
4. Quyền của user hiện tại

