# Hướng Dẫn Testing Module Dental HR Management - Phase 1, 2, 3 & 4

## 📋 Mục Lục
1. [Cách Truy Cập Module](#cách-truy-cập-module)
2. [Test Case 1: Quản Lý Vai Trò (Roles)](#test-case-1-quản-lý-vai-trò-roles)
3. [Test Case 2: Thông Tin Nhân Viên Nha Khoa](#test-case-2-thông-tin-nhân-viên-nha-khoa)
4. [Test Case 3: Quản Lý Nhiều Vai Trò](#test-case-3-quản-lý-nhiều-vai-trò)
5. [Test Case 4: Smart Button Lương](#test-case-4-smart-button-lương)
6. [Test Case 5: Smart Button Nghỉ Phép (Phase 2)](#test-case-5-smart-button-nghỉ-phép-phase-2)
7. [Test Case 6: Quản Lý Thưởng (Phase 3)](#test-case-6-quản-lý-thưởng-phase-3)
8. [Test Case 7: Tính Lương (Phase 3)](#test-case-7-tính-lương-phase-3)
9. [Test Case 8: Workflow Tính Lương (Phase 3)](#test-case-8-workflow-tính-lương-phase-3)
10. [Test Case 9: Tích Hợp Báo Cáo Lợi Nhuận (Phase 4)](#test-case-9-tích-hợp-báo-cáo-lợi-nhuận-phase-4)
11. [Lưu Ý Khi Testing](#lưu-ý-khi-testing)
12. [Troubleshooting](#troubleshooting)

---

## 🚀 Cách Truy Cập Module

### Bước 1: Đăng nhập vào Odoo
1. Mở trình duyệt và truy cập: `http://localhost:8071` (hoặc URL Odoo của bạn)
2. Đăng nhập với tài khoản có quyền:
   - **HR Officer** (hoặc **HR Manager**) - để quản lý nhân viên
   - **Dental HR Manager** - để quản lý vai trò (roles)

### Bước 2: Truy cập Menu
1. Vào menu **Nhân sự** (Employees) ở thanh menu trên cùng
2. Tìm menu **Nha khoa** (Dental) - menu này hiển thị trong HR app
3. Click vào **Nha khoa** để xem sub-menu:
   - **Vai trò** (Roles)
   - **Thưởng** (Bonus) - Phase 3
   - **Lương** (Salary) - Phase 3

### Bước 3: Truy cập Nhân viên
1. Vào **Nhân sự** → **Nhân viên** (Employees)
2. Mở một nhân viên bất kỳ
3. Kiểm tra tab **Thông tin Nha khoa** và smart button **Lương**

---

## ✅ Test Case 1: Quản Lý Vai Trò (Roles)

### Mục đích
Test quản lý các vai trò nhân viên nha khoa (Bác sĩ, Kỹ thuật viên, Lễ tân, Kế toán, Quản lý kho).

### Các bước test:

1. **Truy cập Menu Vai trò**
   - Vào **Nhân sự** → **Nha khoa** → **Vai trò**
   - Kiểm tra danh sách 5 vai trò mặc định:
     - Bác sĩ (doctor)
     - Kỹ thuật viên (technician)
     - Lễ tân (receptionist)
     - Kế toán (accountant)
     - Quản lý kho (inventory_manager)

2. **Xem Chi Tiết Vai Trò**
   - Click vào một vai trò (ví dụ: "Bác sĩ")
   - Kiểm tra form view hiển thị:
     - **Tên vai trò**: Bác sĩ
     - **Mã vai trò**: doctor
     - **Mô tả**: Mô tả vai trò
     - **Số nhân viên**: 0 (ban đầu)
     - Tab **Nhân viên**: Danh sách nhân viên có vai trò này (ban đầu trống)

3. **Tạo Vai Trò Mới**
   - Click **Tạo** (Create)
   - Nhập thông tin:
     - **Tên vai trò**: Quản lý phòng khám
     - **Mã vai trò**: clinic_manager
     - **Mô tả**: Quản lý toàn bộ hoạt động phòng khám
   - Click **Lưu**
   - Kiểm tra vai trò mới xuất hiện trong danh sách

4. **Test Validation**
   - Thử tạo vai trò mới với **Mã vai trò** trùng với vai trò đã có (ví dụ: "doctor")
   - Hệ thống phải báo lỗi: "Mã vai trò phải là duy nhất!"

5. **Tìm Kiếm Vai Trò**
   - Sử dụng search bar để tìm kiếm:
     - Tìm theo tên: "Bác sĩ"
     - Tìm theo mã: "doctor"
   - Kiểm tra kết quả tìm kiếm chính xác

### Kết quả mong đợi:
- ✅ Danh sách 5 vai trò mặc định hiển thị đúng
- ✅ Form view hiển thị đầy đủ thông tin
- ✅ Tạo vai trò mới thành công
- ✅ Validation mã vai trò hoạt động đúng
- ✅ Tìm kiếm hoạt động chính xác

---

## ✅ Test Case 2: Thông Tin Nhân Viên Nha Khoa

### Mục đích
Test thêm thông tin nha khoa vào form nhân viên.

### Các bước test:

1. **Truy Cập Form Nhân Viên**
   - Vào **Nhân sự** → **Nhân viên**
   - Tạo nhân viên mới hoặc mở nhân viên có sẵn
   - Cuộn xuống tab **Thông tin Nha khoa**

2. **Gán Vai Trò Cho Nhân Viên**
   - Trong tab **Thông tin Nha khoa**, tìm field **Vai trò**
   - Click vào field và chọn một hoặc nhiều vai trò:
     - Ví dụ: Chọn "Bác sĩ"
   - Lưu form
   - Kiểm tra vai trò được hiển thị dưới dạng tags

3. **Nhập Thông Tin Chuyên Môn (Cho Bác Sĩ)**
   - Nếu nhân viên có vai trò "Bác sĩ":
     - Field **Chuyên khoa** hiển thị
     - Chọn chuyên khoa: "Niềng răng", "Cấy ghép", "Tẩy trắng", v.v.
   - Nếu nhân viên không có vai trò "Bác sĩ":
     - Field **Chuyên khoa** vẫn hiển thị (có thể để trống)

4. **Nhập Số Năm Kinh Nghiệm**
   - Nhập số năm kinh nghiệm: ví dụ `5`
   - Lưu và kiểm tra giá trị được lưu đúng

5. **Nhập Bằng Cấp/Chứng Chỉ**
   - Trong field **Bằng cấp/Chứng chỉ**, nhập:
     ```
     - Bằng Bác sĩ Nha khoa, Đại học Y Hà Nội (2015)
     - Chứng chỉ Niềng răng Invisalign (2018)
     - Chứng chỉ Cấy ghép Implant (2020)
     ```
   - Lưu và kiểm tra nội dung được lưu đúng

6. **Kiểm Tra Smart Button "Lương"**
   - Ở góc trên bên phải form nhân viên, tìm smart button **Lương**
   - Ban đầu button không hiển thị (vì `salary_count = 0`)
   - Button sẽ hiển thị sau khi có lương (Phase 3)

### Kết quả mong đợi:
- ✅ Tab "Thông tin Nha khoa" hiển thị đầy đủ fields
- ✅ Gán vai trò thành công và hiển thị dưới dạng tags
- ✅ Thông tin chuyên môn, kinh nghiệm, bằng cấp được lưu đúng
- ✅ Smart button "Lương" ẩn khi chưa có lương

---

## ✅ Test Case 3: Quản Lý Nhiều Vai Trò

### Mục đích
Test khả năng một nhân viên có nhiều vai trò (ví dụ: Kế toán kiêm Quản lý kho).

### Các bước test:

1. **Tạo Nhân Viên Có Nhiều Vai Trò**
   - Vào **Nhân sự** → **Nhân viên** → **Tạo**
   - Nhập thông tin cơ bản:
     - **Tên**: Nguyễn Văn A
     - **Email**: nguyenvana@example.com
   - Trong tab **Thông tin Nha khoa**:
     - **Vai trò**: Chọn cả "Kế toán" và "Quản lý kho"
   - Lưu

2. **Kiểm Tra Vai Trò Trong Form**
   - Mở lại nhân viên vừa tạo
   - Kiểm tra field **Vai trò** hiển thị 2 tags: "Kế toán" và "Quản lý kho"

3. **Kiểm Tra Vai Trò Trong Danh Sách Roles**
   - Vào **Nhân sự** → **Nha khoa** → **Vai trò**
   - Mở vai trò "Kế toán"
   - Kiểm tra tab **Nhân viên** hiển thị "Nguyễn Văn A"
   - Mở vai trò "Quản lý kho"
   - Kiểm tra tab **Nhân viên** cũng hiển thị "Nguyễn Văn A"
   - Kiểm tra **Số nhân viên** = 1 cho cả 2 vai trò

4. **Test Smart Button "Xem nhân viên"**
   - Trong form vai trò "Kế toán", click smart button **Xem nhân viên**
   - Kiểm tra danh sách nhân viên hiển thị chỉ những nhân viên có vai trò "Kế toán"
   - Làm tương tự với vai trò "Quản lý kho"

5. **Thêm/Xóa Vai Trò**
   - Mở nhân viên "Nguyễn Văn A"
   - Thêm vai trò "Lễ tân" vào danh sách vai trò
   - Lưu
   - Kiểm tra nhân viên hiện có 3 vai trò
   - Xóa vai trò "Kế toán"
   - Lưu
   - Kiểm tra nhân viên còn 2 vai trò: "Quản lý kho" và "Lễ tân"

### Kết quả mong đợi:
- ✅ Một nhân viên có thể có nhiều vai trò
- ✅ Vai trò hiển thị đúng trong form nhân viên
- ✅ Nhân viên xuất hiện đúng trong danh sách nhân viên của từng vai trò
- ✅ Smart button "Xem nhân viên" hoạt động đúng
- ✅ Có thể thêm/xóa vai trò linh hoạt

---

## ✅ Test Case 4: Smart Button Lương

### Mục đích
Test smart button "Lương" trong form nhân viên (sẽ hoạt động đầy đủ ở Phase 3).

### Các bước test:

1. **Kiểm Tra Button Ẩn Khi Chưa Có Lương**
   - Mở một nhân viên chưa có lương nào
   - Kiểm tra smart button **Lương** không hiển thị
   - (Button chỉ hiển thị khi `salary_count > 0`)

2. **Test Khi Model dental.salary Chưa Tồn Tại**
   - Button sẽ hiển thị thông báo nếu click (nhưng không nên click được vì button ẩn)
   - Khi Phase 3 được triển khai, button sẽ hoạt động đầy đủ

### Kết quả mong đợi:
- ✅ Smart button "Lương" hiển thị (sẽ hiển thị 0 khi chưa có lương)
- ✅ Không có lỗi khi module chưa có Phase 3

---

## ✅ Test Case 5: Smart Button Nghỉ Phép (Phase 2)

### Mục đích
Test smart button "Nghỉ phép" trong form nhân viên, tích hợp với module `hr_holidays` của Odoo.

### Các bước test:

1. **Kiểm Tra Smart Button "Nghỉ phép"**
   - Mở một nhân viên bất kỳ
   - Ở góc trên bên phải form nhân viên, tìm smart button **Nghỉ phép**
   - Kiểm tra button hiển thị với số đơn nghỉ phép (ban đầu có thể là 0)
   - Button nằm cạnh smart button **Lương**

2. **Click Smart Button "Nghỉ phép"**
   - Click vào smart button **Nghỉ phép**
   - Kiểm tra màn hình chuyển đến danh sách nghỉ phép của nhân viên
   - Danh sách được filter theo nhân viên hiện tại
   - Nếu chưa có đơn nghỉ phép nào, hiển thị màn hình trống với thông báo

3. **Tạo Đơn Nghỉ Phép Từ Smart Button**
   - Trong danh sách nghỉ phép, click **Tạo** (Create)
   - Kiểm tra form tạo đơn nghỉ phép mới
   - Field **Nhân viên** đã được điền sẵn (từ context)
   - Điền thông tin:
     - **Loại nghỉ**: Chọn loại nghỉ (ví dụ: Nghỉ phép năm)
     - **Ngày bắt đầu**: Chọn ngày bắt đầu
     - **Ngày kết thúc**: Chọn ngày kết thúc
     - **Lý do**: Nhập lý do nghỉ (nếu có)
   - Click **Lưu**
   - Kiểm tra đơn nghỉ phép được tạo thành công

4. **Kiểm Tra Số Đếm Cập Nhật**
   - Quay lại form nhân viên
   - Kiểm tra smart button **Nghỉ phép** hiển thị số đếm = 1 (hoặc số đơn đã tạo)
   - Tạo thêm đơn nghỉ phép khác
   - Kiểm tra số đếm tăng lên

5. **Test Khi Module hr_holidays Chưa Cài Đặt**
   - (Nếu có thể test): Gỡ module `hr_holidays`
   - Mở form nhân viên
   - Smart button **Nghỉ phép** vẫn hiển thị nhưng số đếm = 0
   - Click button sẽ hiển thị thông báo: "Module nghỉ phép chưa được cài đặt."

6. **Tích Hợp Với Menu Nghỉ Phép Của Odoo**
   - Vào **Nhân sự** → **Nghỉ phép** (menu của `hr_holidays`)
   - Kiểm tra có thể tạo/sửa/xóa đơn nghỉ phép từ menu này
   - Kiểm tra smart button trong form nhân viên link đến cùng model `hr.leave`

### Kết quả mong đợi:
- ✅ Smart button "Nghỉ phép" hiển thị trong form nhân viên
- ✅ Button hiển thị số đơn nghỉ phép chính xác
- ✅ Click button mở danh sách nghỉ phép được filter theo nhân viên
- ✅ Có thể tạo đơn nghỉ phép mới từ smart button
- ✅ Số đếm cập nhật tự động khi có đơn nghỉ phép mới
- ✅ Tích hợp tốt với module `hr_holidays` của Odoo

---

## ✅ Test Case 6: Quản Lý Thưởng (Phase 3)

### Mục đích
Test quản lý các khoản thưởng cho nhân viên: thưởng cá nhân, thưởng tập thể, thưởng lễ, lương tháng 13.

### Các bước test:

1. **Truy Cập Menu Thưởng**
   - Vào **Nhân sự** → **Nha khoa** → **Thưởng**
   - Kiểm tra danh sách thưởng (ban đầu trống)

2. **Tạo Thưởng Cá Nhân**
   - Click **Tạo** (Create)
   - Nhập thông tin:
     - **Tên thưởng**: Thưởng hiệu suất tháng 12
     - **Loại thưởng**: Thưởng cá nhân
     - **Số tiền**: 500000
     - **Nhân viên**: Chọn một nhân viên (ví dụ: Bác sĩ A)
     - **Ngày áp dụng**: Chọn ngày hiện tại
     - **Mô tả**: Thưởng cho hiệu suất làm việc tốt
   - Click **Lưu**
   - Kiểm tra trạng thái = "Nháp"
   - Click **Xác nhận**
   - Kiểm tra trạng thái = "Đã xác nhận"

3. **Tạo Thưởng Tập Thể**
   - Click **Tạo** (Create)
   - Nhập thông tin:
     - **Tên thưởng**: Thưởng Tết Nguyên Đán
     - **Loại thưởng**: Thưởng tập thể
     - **Số tiền**: 1000000
     - **Nhân viên**: Để trống (thưởng tập thể không cần chọn nhân viên cụ thể)
     - **Ngày áp dụng**: Chọn ngày
   - Click **Lưu** và **Xác nhận**

4. **Tạo Thưởng Lễ**
   - Tạo thưởng với **Loại thưởng**: Thưởng lễ
   - **Số tiền**: 300000
   - Chọn nhân viên hoặc để trống (tùy loại thưởng lễ)

5. **Tìm Kiếm và Lọc**
   - Sử dụng search bar để tìm kiếm theo tên, loại thưởng
   - Sử dụng filters: "Nháp", "Đã xác nhận", "Thưởng cá nhân", "Thưởng tập thể"
   - Nhóm theo: Loại thưởng, Trạng thái, Ngày

6. **Test Quay Lại Nháp**
   - Mở một thưởng đã xác nhận
   - Click **Quay lại nháp**
   - Kiểm tra trạng thái = "Nháp"

### Kết quả mong đợi:
- ✅ Tạo thưởng cá nhân thành công
- ✅ Tạo thưởng tập thể thành công
- ✅ Workflow Nháp → Đã xác nhận hoạt động đúng
- ✅ Tìm kiếm và lọc hoạt động chính xác
- ✅ Có thể quay lại nháp từ trạng thái đã xác nhận

---

## ✅ Test Case 7: Tính Lương (Phase 3)

### Mục đích
Test tính lương cho nhân viên: lương cơ bản từ hợp đồng + các khoản thưởng đã xác nhận.

### Các bước test:

1. **Truy Cập Menu Lương**
   - Vào **Nhân sự** → **Nha khoa** → **Lương**
   - Kiểm tra danh sách lương (ban đầu trống)

2. **Tạo Lương Mới**
   - Click **Tạo** (Create)
   - Nhập thông tin:
     - **Tên**: Lương tháng 12/2024 (hoặc để mặc định)
     - **Nhân viên**: Chọn một nhân viên có hợp đồng
     - **Tháng/Năm**: Chọn tháng (ví dụ: 01/12/2024)
   - Click **Lưu**
   - Kiểm tra:
     - **Lương cơ bản**: Tự động tính từ hợp đồng (nếu nhân viên có hợp đồng active)
     - **Tổng thưởng**: 0 (chưa chọn thưởng)
     - **Tổng lương**: = Lương cơ bản + Tổng thưởng

3. **Thêm Thưởng Vào Lương**
   - Trong form lương, tab **Thưởng**
   - Chọn các khoản thưởng đã xác nhận (chỉ hiển thị thưởng có state='confirmed')
   - Lưu
   - Kiểm tra:
     - **Tổng thưởng**: Tự động tính từ các thưởng đã chọn
     - **Tổng lương**: Tự động cập nhật = Lương cơ bản + Tổng thưởng

4. **Test Tính Thưởng Tự Động**
   - Tạo thưởng cá nhân cho nhân viên A (đã xác nhận)
   - Tạo thưởng tập thể (đã xác nhận)
   - Tạo lương cho nhân viên A
   - Chọn cả 2 thưởng trên
   - Kiểm tra **Tổng thưởng** = thưởng cá nhân + thưởng tập thể

5. **Test Khi Không Có Hợp Đồng**
   - Tạo lương cho nhân viên chưa có hợp đồng hoặc hợp đồng không active
   - Kiểm tra **Lương cơ bản** = 0

6. **Tìm Kiếm và Lọc**
   - Tìm kiếm theo tên, nhân viên, tháng
   - Lọc theo trạng thái: Nháp, Đã gửi, Đã duyệt, Đã đăng
   - Nhóm theo: Nhân viên, Tháng, Trạng thái

### Kết quả mong đợi:
- ✅ Tạo lương mới thành công
- ✅ Lương cơ bản tự động tính từ hợp đồng
- ✅ Tổng thưởng tự động tính từ các thưởng đã chọn
- ✅ Tổng lương = Lương cơ bản + Tổng thưởng
- ✅ Chỉ hiển thị thưởng đã xác nhận trong danh sách
- ✅ Tìm kiếm và lọc hoạt động chính xác

---

## ✅ Test Case 8: Workflow Tính Lương (Phase 3)

### Mục đích
Test workflow tính lương: Nháp → Đã gửi → Đã duyệt → Đã đăng (tạo bút toán kế toán).

### Các bước test:

1. **Tạo Lương Ở Trạng Thái Nháp**
   - Tạo lương mới với đầy đủ thông tin
   - Kiểm tra trạng thái = "Nháp"
   - Kiểm tra các button: "Gửi để duyệt" hiển thị

2. **Gửi Để Duyệt (Accountant)**
   - Click **Gửi để duyệt**
   - Kiểm tra:
     - Trạng thái = "Đã gửi"
     - **Người gửi** = User hiện tại
     - **Ngày gửi** = Thời gian hiện tại
     - Button "Duyệt" hiển thị

3. **Duyệt (Manager)**
   - Đăng nhập với user có quyền Manager (hoặc HR Manager)
   - Mở lương đã gửi
   - Click **Duyệt**
   - Kiểm tra:
     - Trạng thái = "Đã duyệt"
     - **Người duyệt** = User hiện tại
     - **Ngày duyệt** = Thời gian hiện tại
     - Button "Đăng bút toán" hiển thị

4. **Đăng Bút Toán (Accountant)**
   - Đăng nhập lại với user có quyền **Accountant** (hoặc **Account Manager**)
   - Mở lương đã duyệt
   - Click **Đăng bút toán**
   - Kiểm tra:
     - Trạng thái = "Đã đăng"
     - Smart button "Bút toán" hiển thị
     - Click "Bút toán" mở bút toán kế toán
     - **Lưu ý**: Để xem các dòng kế toán, user phải có quyền **account.group_account_readonly** (thường là Accountant hoặc Account Manager)
     - Trong form bút toán, vào tab **"Journal Items"** (Bút toán chi tiết)
     - Bút toán có:
       - Nợ: Tài khoản 6411 (Chi phí nhân viên) = Tổng lương
       - Có: Tài khoản 3341 (Phải trả công nhân viên) = Tổng lương
       - Journal: SAL (Lương)
   - **Lưu ý quan trọng**: Nếu không thấy tab "Journal Items":
     - Kiểm tra user có quyền Accountant/Account Manager
     - Vào **Cài đặt → Người dùng** → Chọn user → Tab **Quyền truy cập** → Đảm bảo có quyền **Kế toán → Đọc hóa đơn** hoặc cao hơn

5. **Test Quay Lại Nháp**
   - Mở lương ở trạng thái "Đã gửi"
   - Click **Quay lại nháp**
   - Kiểm tra trạng thái = "Nháp", các field workflow bị xóa
   - Thử quay lại nháp từ lương "Đã đăng" → Phải báo lỗi

6. **Test Validation**
   - Thử đăng bút toán 2 lần → Phải báo lỗi "Bút toán đã được tạo rồi!"
   - Thử quay lại nháp từ lương đã đăng → Phải báo lỗi

### Kết quả mong đợi:
- ✅ Workflow hoạt động đúng: Nháp → Đã gửi → Đã duyệt → Đã đăng
- ✅ Thông tin người gửi/duyệt và thời gian được lưu đúng
- ✅ Bút toán kế toán được tạo tự động khi đăng
- ✅ Bút toán có đúng tài khoản Nợ/Có và số tiền
- ✅ Validation hoạt động đúng (không thể đăng 2 lần, không thể quay lại nháp khi đã đăng)

---

## ✅ Test Case 9: Tích Hợp Báo Cáo Lợi Nhuận (Phase 4)

### Mục đích
Test tích hợp chi phí lương vào báo cáo lợi nhuận, đảm bảo chi phí lương được tính vào tổng chi phí và ảnh hưởng đến lợi nhuận.

### Các bước test:

1. **Chuẩn Bị Dữ Liệu**
   - Tạo ít nhất 1 lương đã đăng (state='posted') cho tháng 12/2025
   - Đảm bảo có payments và treatments trong tháng 12/2025 để có doanh thu và chi phí vật tư

2. **Truy Cập Báo Cáo Lợi Nhuận**
   - Vào **Hóa đơn** → **Kế toán Nha khoa** → **Báo cáo Lợi nhuận**
   - (Hoặc menu tương ứng trong module Accounting)

3. **Xem Báo Cáo Tháng 12/2025**
   - Chọn **Tháng**: 01/12/2025
   - Hệ thống tự động tính toán:
     - **Doanh thu**: Tổng payments đã posted trong tháng
     - **Chi phí vật tư**: Tổng supply_cost của treatments
     - **Chi phí khác**: Tổng recurring payments (không bao gồm chi phí lương)
     - **Chi phí lương**: Tổng lương đã đăng trong tháng (từ dental_hr, state='posted')
     - **Tổng chi phí**: = Chi phí vật tư + Chi phí khác + Chi phí lương
     - **Lợi nhuận**: = Doanh thu - Tổng chi phí
   - **Lưu ý**: Chi phí lương được tính từ các record `dental.salary` có:
     - `state = 'posted'` (đã đăng bút toán)
     - `month` cùng năm và tháng với tháng được chọn trong báo cáo

4. **Kiểm Tra Chi Phí Lương**
   - Kiểm tra field **Chi phí lương** hiển thị đúng số tiền
   - So sánh với tổng lương đã đăng trong tháng 12/2025
   - Kiểm tra **Tổng chi phí** bao gồm chi phí lương

5. **Kiểm Tra Khi Không Có Lương**
   - Chọn tháng không có lương đã đăng (ví dụ: tháng 11/2025)
   - Kiểm tra **Chi phí lương** = 0
   - Kiểm tra **Tổng chi phí** = Chi phí vật tư + Chi phí khác (không có chi phí lương)

6. **Kiểm Tra Khi Module dental_hr Chưa Cài Đặt**
   - (Nếu có thể test): Gỡ module `dental_hr`
   - Mở báo cáo lợi nhuận
   - Kiểm tra **Chi phí lương** = 0 (không có lỗi)
   - Kiểm tra hệ thống vẫn hoạt động bình thường

7. **In Báo Cáo PDF**
   - Click **In** hoặc **Print** trong form báo cáo
   - Kiểm tra PDF có hiển thị:
     - Doanh thu
     - Chi phí vật tư
     - Chi phí khác
     - **Chi phí lương** (mới thêm)
     - Tổng chi phí
     - Lợi nhuận

8. **Test Tính Toán Chính Xác**
   - Tạo lương cho nhân viên A: 10.000.000 (đã đăng)
   - Tạo lương cho nhân viên B: 8.000.000 (đã đăng)
   - Mở báo cáo lợi nhuận tháng đó
   - Kiểm tra **Chi phí lương** = 18.000.000
   - Kiểm tra **Tổng chi phí** = Chi phí vật tư + Chi phí khác + 18.000.000
   - Kiểm tra **Lợi nhuận** = Doanh thu - Tổng chi phí (đã bao gồm chi phí lương)

### Kết quả mong đợi:
- ✅ Chi phí lương được tính đúng từ các lương đã đăng trong tháng (state='posted')
- ✅ Chi phí lương được hiển thị trong form báo cáo (field riêng, không nằm trong "Chi phí khác")
- ✅ Chi phí lương được bao gồm trong tổng chi phí
- ✅ Lợi nhuận được tính đúng (Doanh thu - Tổng chi phí bao gồm chi phí lương)
- ✅ Chi phí lương được hiển thị trong PDF report
- ✅ Hệ thống hoạt động bình thường khi module dental_hr chưa cài đặt (chi phí lương = 0)

### Troubleshooting: Chi phí lương không hiển thị

Nếu chi phí lương = 0 mặc dù đã có lương đã đăng:
1. **Kiểm tra trạng thái lương**: 
   - Vào **Nhân sự → Nha khoa → Lương**
   - Kiểm tra lương có `state = 'posted'` (Đã đăng) chưa
   - Chỉ lương ở trạng thái "Đã đăng" mới được tính vào chi phí

2. **Kiểm tra tháng của lương**:
   - Kiểm tra field **Tháng/Năm** trong lương có cùng năm và tháng với tháng được chọn trong báo cáo không
   - Ví dụ: Nếu báo cáo chọn tháng 12/2025, lương phải có month = 12/2025 (bất kỳ ngày nào trong tháng 12)

3. **Kiểm tra module dental_hr**:
   - Đảm bảo module `dental_hr` đã được cài đặt và upgrade
   - Upgrade module `dental_accounting` để áp dụng logic tính chi phí lương mới

---

## 📝 Lưu Ý Khi Testing

1. **Quyền Truy Cập**:
   - **Quản lý Nhân viên**: User cần có quyền **HR Officer** (hoặc **HR Manager**) để xem/sửa nhân viên và các fields mới từ `dental_hr` (dental_roles, dental_specialty, etc.)
   - **Quản lý Vai trò (Roles)**: User cần có quyền **Dental HR Manager** để tạo/sửa/xóa roles
   - User thường (base.group_user) chỉ có thể xem roles (read-only)

2. **Dữ liệu Test**:
   - Module tự động tạo 5 roles mặc định khi cài đặt
   - Có thể tạo thêm roles mới nếu cần

3. **Many2many Relationship**:
   - Một nhân viên có thể có nhiều vai trò
   - Một vai trò có thể được gán cho nhiều nhân viên
   - Relationship được quản lý qua bảng trung gian `employee_role_rel`

4. **Computed Fields**:
   - `employee_count` trong `dental.role`: Tự động tính số nhân viên
   - `salary_count` trong `hr.employee`: Tự động tính số lần tính lương (Phase 3)
   - `leave_count` trong `hr.employee`: Tự động tính số đơn nghỉ phép (Phase 2)
   - `base_salary` trong `dental.salary`: Tự động tính từ hợp đồng
   - `bonus_amount` trong `dental.salary`: Tự động tính từ các thưởng đã chọn
   - `total_salary` trong `dental.salary`: Tự động tính = base_salary + bonus_amount
   - `employee_count` trong `dental.bonus`: Tự động tính số nhân viên được thưởng
   - `salary_cost` trong `dental.profit.report`: Tự động tính từ các lương đã đăng trong tháng (Phase 4)

5. **Validation**:
   - Mã vai trò (`code`) phải là duy nhất
   - Tên vai trò (`name`) là bắt buộc

---

## 🐛 Troubleshooting

### Lỗi: Không thấy menu "Nha khoa"
- **Giải pháp**: 
  - Kiểm tra module `dental_hr` đã được cài đặt và kích hoạt chưa
  - Vào **Apps** → Tìm "Dental HR Management" → **Install**
  - Kiểm tra user có quyền HR Manager

### Lỗi: Không thấy tab "Thông tin Nha khoa" trong form nhân viên
- **Giải pháp**: 
  - Kiểm tra module `dental_hr` đã được cài đặt
  - Refresh trang (Ctrl+F5)
  - Kiểm tra view inheritance có đúng không

### Lỗi: Không thể tạo vai trò mới với mã trùng
- **Giải pháp**: 
  - Đây là behavior đúng - mã vai trò phải là duy nhất
  - Chọn mã khác hoặc sửa vai trò đã có

### Lỗi: Smart button "Lương" không hiển thị
- **Giải pháp**: 
  - Button luôn hiển thị (sẽ hiển thị 0 khi chưa có lương)
  - Kiểm tra module `dental_hr` đã được upgrade lên Phase 3 chưa
  - Refresh trang (Ctrl+F5)

### Lỗi: Không thể tạo thưởng mới
- **Giải pháp**: 
  - Kiểm tra user có quyền HR Officer/Manager
  - Kiểm tra module `dental_hr` đã được upgrade lên Phase 3 chưa
  - Refresh trang

### Lỗi: Không thể tạo lương mới
- **Giải pháp**: 
  - Kiểm tra user có quyền HR Officer/Manager
  - Kiểm tra nhân viên đã có hợp đồng chưa (lương cơ bản sẽ = 0 nếu chưa có hợp đồng)
  - Kiểm tra module `dental_hr` đã được upgrade lên Phase 3 chưa

### Lỗi: Không thể đăng bút toán
- **Giải pháp**: 
  - Kiểm tra journal "Lương" (code: SAL) đã được tạo chưa
  - Kiểm tra tài khoản 6411 (Chi phí nhân viên) đã có trong chart of accounts chưa
  - Kiểm tra tài khoản 3341 (Phải trả công nhân viên) đã có trong chart of accounts chưa
  - Kiểm tra lương đã ở trạng thái "Đã duyệt" chưa

### Lỗi: Smart button "Nghỉ phép" không hiển thị
- **Giải pháp**: 
  - Kiểm tra module `hr_holidays` đã được cài đặt chưa
  - Vào **Apps** → Tìm "Time Off" hoặc "Leave Management" → **Install**
  - Kiểm tra user có quyền HR để xem smart button
  - Refresh trang (Ctrl+F5)

### Lỗi: Không thể gán vai trò cho nhân viên
- **Giải pháp**: 
  - Kiểm tra user có quyền sửa nhân viên
  - Kiểm tra roles đã được tạo chưa
  - Refresh trang

### Lỗi: Nhân viên không xuất hiện trong danh sách nhân viên của vai trò
- **Giải pháp**: 
  - Kiểm tra nhân viên đã được gán vai trò chưa
  - Lưu lại form nhân viên sau khi gán vai trò
  - Refresh trang

---

## 📊 Tóm Tắt Test Cases

| Test Case | Mục đích | Trạng thái |
|-----------|----------|------------|
| Test Case 1 | Quản lý Vai trò (Roles) | ✅ Hoàn thành |
| Test Case 2 | Thông tin Nhân viên Nha khoa | ✅ Hoàn thành |
| Test Case 3 | Quản lý Nhiều Vai trò | ✅ Hoàn thành |
| Test Case 4 | Smart Button Lương | ✅ Hoàn thành |
| Test Case 5 | Smart Button Nghỉ phép (Phase 2) | ✅ Hoàn thành |
| Test Case 6 | Quản lý Thưởng (Phase 3) | ✅ Hoàn thành |
| Test Case 7 | Tính Lương (Phase 3) | ✅ Hoàn thành |
| Test Case 8 | Workflow Tính Lương (Phase 3) | ✅ Hoàn thành |
| Test Case 9 | Tích hợp Báo cáo Lợi nhuận (Phase 4) | ✅ Hoàn thành |

---

## 🔄 Workflow Testing

### Workflow: Gán Vai Trò Cho Nhân Viên

1. **Tạo/Sửa Nhân Viên**
   - Vào **Nhân sự** → **Nhân viên**
   - Tạo mới hoặc mở nhân viên có sẵn

2. **Gán Vai Trò**
   - Tab **Thông tin Nha khoa** → Field **Vai trò**
   - Chọn một hoặc nhiều vai trò từ danh sách
   - Lưu

3. **Kiểm Tra Kết Quả**
   - Vai trò hiển thị dưới dạng tags trong form nhân viên
   - Nhân viên xuất hiện trong danh sách nhân viên của từng vai trò
   - Số nhân viên trong form vai trò được cập nhật

---

## 📈 Test Coverage

### Models
- ✅ `dental.role`: CRUD operations, validation, computed fields
- ✅ `hr.employee`: Extend với fields mới, computed fields, methods (Phase 1, 2 & 3)
- ✅ `hr.leave`: Tích hợp với `hr_holidays` (Phase 2)
- ✅ `dental.bonus`: CRUD operations, workflow, computed fields (Phase 3)
- ✅ `dental.salary`: CRUD operations, workflow, computed fields, accounting integration (Phase 3)
- ✅ `dental.profit.report`: Tích hợp chi phí lương vào báo cáo lợi nhuận (Phase 4)

### Views
- ✅ Tree view cho `dental.role`, `dental.bonus`, `dental.salary`
- ✅ Form view cho `dental.role`, `dental.bonus`, `dental.salary`
- ✅ Search view cho `dental.role`, `dental.bonus`, `dental.salary`
- ✅ Extend form view cho `hr.employee`
- ✅ Smart buttons: Lương, Nghỉ phép (Phase 2 & 3)

### Security
- ✅ Access rights cho `dental.role`, `dental.bonus`, `dental.salary`
- ✅ Security groups

### Data
- ✅ Default roles data
- ✅ Journal cho lương (code: SAL)

---

## 🎯 Next Steps

Sau khi test xong Phase 1, 2, 3 & 4, module `dental_hr` đã hoàn thành đầy đủ các chức năng:
1. ✅ **Phase 1**: Quản lý thông tin nhân viên cơ bản
2. ✅ **Phase 2**: Quản lý nghỉ phép
3. ✅ **Phase 3**: Tính lương và thưởng
4. ✅ **Phase 4**: Tích hợp báo cáo lợi nhuận (hiển thị chi phí lương)

---

**Chúc bạn testing thành công! 🎉**

