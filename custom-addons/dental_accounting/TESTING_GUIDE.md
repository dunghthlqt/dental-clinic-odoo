# Hướng Dẫn Testing Module Dental Accounting

## ⚠️ Lưu Ý Quan Trọng

> **Tính năng "Theo dõi Công nợ" (Follow-up) đã tạm thời bị vô hiệu hóa** và sẽ được triển khai lại trong phiên bản sau. Vui lòng bỏ qua Test Case 4 trong hướng dẫn này.

## 📋 Mục Lục
1. [Cách Truy Cập Module](#cách-truy-cập-module)
2. [Test Case 1: Dịch vụ Ngắn Ngày (Full Payment)](#test-case-1-dịch-vụ-ngắn-ngày-full-payment)
3. [Test Case 2: Dịch vụ Dài Ngày (Installment)](#test-case-2-dịch-vụ-dài-ngày-installment)
4. [Test Case 3: Thanh toán Định kỳ](#test-case-3-thanh-toán-định-kỳ)
5. ~~[Test Case 4: Theo dõi Công nợ (Follow-up)](#test-case-4-theo-dõi-công-nợ-follow-up)~~ *(Tạm vô hiệu hóa)*
6. [Test Case 5: Báo cáo Lợi nhuận](#test-case-5-báo-cáo-lợi-nhuận)
7. [Test Case 6: Khóa Ngày Kế toán](#test-case-6-khóa-ngày-kế-toán)
8. [Test Case 7: Chi phí Vật tư Tự động (Phase 2)](#test-case-7-chi-phí-vật-tư-tự-động-phase-2)

---

## 🚀 Cách Truy Cập Module

### Bước 1: Đăng nhập vào Odoo
1. Mở trình duyệt và truy cập: `http://localhost:8071` (hoặc URL Odoo của bạn)
2. Đăng nhập với tài khoản có quyền **Accountant** hoặc **Account Manager**

### Bước 2: Truy cập Menu Kế toán Nha khoa
1. Vào menu **Hóa đơn** (Invoicing) ở thanh menu trên cùng
2. Tìm menu **Kế toán Nha khoa** (Dental Accounting) - menu này hiển thị trực tiếp trong menu bar của "Hóa đơn"
3. Click vào **Kế toán Nha khoa** để xem các sub-menu:
   - **Kế hoạch Thanh toán** (Payment Plans)
   - **Báo cáo Lợi nhuận** (Profit Report)
   - ~~**Theo dõi Công nợ** (Follow-up)~~ *(Tạm vô hiệu hóa)*
   - **Thanh toán Định kỳ** (Recurring Payments)

### Bước 3: Menu Khóa Ngày
- Vào **Hóa đơn** → **Cấu hình** (Configuration) → **Accounting** → **Khóa Ngày** (Lock Dates)
- **Lưu ý**: Menu "Cấu hình" chỉ hiển thị cho user có quyền `account.group_account_manager`
- Chỉ hiển thị cho user có quyền **Account Manager**

### Bước 4: Menu Hồ sơ điều trị (cho Accountant)
- Vào **Hóa đơn** → **Kế toán Nha khoa** → **Hồ sơ điều trị**
- **Lưu ý**: Menu này chỉ hiển thị cho user có quyền **Accountant** hoặc **Account Manager**
- Accountant có thể xem (READ-only) hồ sơ điều trị để kiểm tra thông tin kế toán trong tab "Kế toán"

**Lưu ý về cấu trúc menu Odoo 17**:
- Menu chính là **Hóa đơn** (Invoicing) - tương ứng với `account.menu_finance`
- **Kế toán Nha khoa** là menu trực tiếp dưới "Hóa đơn", cùng cấp với "Khách hàng", "Nhà cung cấp", "Báo cáo", "Cấu hình"
- Menu "Cấu hình" (Configuration) chỉ hiển thị cho Account Manager

---

## ✅ Test Case 1: Dịch vụ Ngắn Ngày (Full Payment)

### Mục đích
Test workflow cho dịch vụ ngắn ngày (trám răng, lấy cao răng...) - thanh toán toàn bộ ngay.

### Các bước test:

1. **Tạo Hồ sơ Điều trị**
   - Vào **Quản lý Phòng khám** → **Hồ sơ Điều trị**
   - Tạo mới một hồ sơ điều trị
   - Chọn **Chính sách thanh toán**: `Thanh toán toàn bộ`
   - Nhập **Tổng chi phí**: ví dụ `5,000,000 VND`
   - Lưu

2. **Tạo Thanh toán**
   - Vào **Hóa đơn** → **Khách hàng** → **Thanh toán**
   - Tạo mới thanh toán:
     - **Khách hàng**: Chọn bệnh nhân
     - **Điều trị liên quan**: Chọn hồ sơ điều trị vừa tạo
     - **Số tiền**: `5,000,000 VND`
     - **Tự động tạo hóa đơn**: ✓ (checked)
   - Xác nhận thanh toán (Post)

3. **Kiểm tra Hóa đơn tự động tạo**
   - Vào **Hóa đơn** → **Khách hàng** → **Hóa đơn**
   - Tìm hóa đơn vừa được tạo tự động
   - Kiểm tra:
     - Hóa đơn có link với **Điều trị liên quan**
     - Hiển thị **Tổng chi phí điều trị**: `5,000,000`
     - Hiển thị **Đã thanh toán**: `5,000,000`
     - Hiển thị **Số tiền còn lại**: `0` (vì đã thanh toán đủ)

4. **Kiểm tra Hồ sơ Điều trị**
   - Quay lại **Hồ sơ Điều trị**
   - Mở tab **Kế toán**
   - Kiểm tra:
     - **Doanh thu**: `5,000,000`
     - **Chi phí vật tư**: Tự động tính từ inventory (0 nếu chưa có buổi điều trị với vật tư)
     - **Lợi nhuận**: `5,000,000 - Chi phí vật tư`

### Kết quả mong đợi:
- ✅ Thanh toán được tạo thành công
- ✅ Hóa đơn được tạo tự động
- ✅ Hóa đơn hiển thị đúng thông tin điều trị
- ✅ Số tiền còn lại = 0

---

## ✅ Test Case 2: Dịch vụ Dài Ngày (Installment)

### Mục đích
Test workflow cho dịch vụ dài ngày (niềng răng, cấy ghép...) - trả góp 12 tháng.

### Các bước test:

1. **Tạo Hồ sơ Điều trị**
   - Vào **Quản lý Phòng khám** → **Hồ sơ Điều trị**
   - Tạo mới một hồ sơ điều trị
   - Chọn **Chính sách thanh toán**: `Trả góp`
   - Nhập **Tổng chi phí**: ví dụ `20,000,000 VND`
   - Lưu

2. **Tạo Kế hoạch Thanh toán**
   - Trong form **Hồ sơ Điều trị**, tab **Kế toán**
   - Click button **Tạo Kế hoạch Thanh toán**
   - Form wizard hiển thị:
     - **Tổng số tiền**: `20,000,000` (tự động)
     - **Đóng trước**: `10,000,000` (50% tự động)
     - **Ngày đóng trước**: Chọn ngày hôm nay
     - **Số tháng trả góp**: `12` (cố định, readonly)
   - Lưu và Xác nhận

3. **Thanh toán Kỳ 1 (50% đóng trước)**
   - Vào **Hóa đơn** → **Khách hàng** → **Thanh toán**
   - Tạo mới thanh toán:
     - **Khách hàng**: Chọn bệnh nhân
     - **Kế hoạch thanh toán**: Chọn kế hoạch vừa tạo
     - **Điều trị liên quan**: Tự động fill
     - **Số tiền**: `10,000,000 VND`
     - **Tự động tạo hóa đơn**: ✓
   - Xác nhận thanh toán

4. **Kiểm tra Hóa đơn Kỳ 1**
   - Vào **Hóa đơn** → **Khách hàng** → **Hóa đơn**
   - Tìm hóa đơn vừa tạo
   - Kiểm tra:
     - **Tổng chi phí điều trị**: `20,000,000`
     - **Đã thanh toán**: `10,000,000`
     - **Số tiền còn lại**: `10,000,000` (còn 50%)

5. **Thanh toán Kỳ 2 (Linh hoạt)**
   - Tạo thanh toán mới:
     - **Kế hoạch thanh toán**: Cùng kế hoạch
     - **Số tiền**: `3,000,000 VND` (ví dụ, không nhất thiết phải đều)
   - Xác nhận

6. **Kiểm tra Kế hoạch Thanh toán**
   - Vào **Kế toán Nha khoa** → **Kế hoạch Thanh toán**
   - Mở kế hoạch vừa tạo
   - Kiểm tra:
     - **Tổng số tiền**: `20,000,000`
     - **Đã thanh toán**: `13,000,000`
     - **Còn lại**: `7,000,000`
     - **Quá hạn**: `False` (chưa đến 12 tháng)

### Kết quả mong đợi:
- ✅ Kế hoạch thanh toán được tạo với 50% đóng trước
- ✅ Các khoản thanh toán được ghi nhận đúng
- ✅ Hóa đơn tự động tạo và hiển thị số tiền còn lại
- ✅ Kế hoạch thanh toán cập nhật đúng tổng đã thanh toán

---

## ✅ Test Case 3: Thanh toán Định kỳ

### Mục đích
Test quản lý chi phí cố định (thuê mặt bằng, lương nhân viên...).

### Các bước test:

1. **Tạo Thanh toán Định kỳ**
   - Vào **Kế toán Nha khoa** → **Thanh toán Định kỳ**
   - Tạo mới:
     - **Tên**: "Tiền thuê mặt bằng"
     - **Tài khoản Nợ**: Chọn tài khoản chi phí (ví dụ: Chi phí thuê)
     - **Tài khoản Có**: Chọn tài khoản ngân hàng
     - **Sổ nhật ký**: Chọn sổ nhật ký
     - **Số tiền**: `10,000,000 VND`
     - **Ngày bắt đầu**: Chọn ngày hôm nay
     - **Chu kỳ**: `Tháng`
     - **Khoảng cách**: `1` (mỗi tháng)
     - **Thời điểm thanh toán**: `Thanh toán ngay`
     - **Trạng thái bút toán**: `Đã đăng`
     - **Mô tả**: "Tiền thuê mặt bằng hàng tháng"
   - Click **Bắt đầu**

2. **Kiểm tra Cron Job**
   - Đợi 1 ngày (hoặc chạy cron job thủ công)
   - Vào **Hóa đơn** → **Kế toán** (Accounting) → **Journals** → **Bút toán** (Journal Entries)
   - **Lưu ý**: Menu "Kế toán" chỉ hiển thị nếu user có quyền phù hợp
   - Tìm bút toán có **Tham chiếu** (Ref) = "Tiền thuê mặt bằng"
   - Kiểm tra bút toán đã được tạo tự động

3. **Kiểm tra Tab "Các bút toán định kỳ"**
   - Quay lại **Thanh toán Định kỳ**
   - Mở record vừa tạo
   - Tab **Các bút toán định kỳ** hiển thị các bút toán đã được tạo

### Kết quả mong đợi:
- ✅ Thanh toán định kỳ được tạo và bắt đầu
- ✅ Cron job tự động tạo bút toán theo lịch
- ✅ Bút toán được đăng (posted) nếu chọn "Đã đăng"

---

## ⏸️ Test Case 4: Theo dõi Công nợ (Follow-up) - TẠM VÔ HIỆU HÓA

> ⚠️ **Lưu ý**: Tính năng này đã tạm thời bị vô hiệu hóa và sẽ được triển khai lại trong phiên bản sau. Vui lòng bỏ qua test case này.

### Mục đích
~~Test hệ thống nhắc nhở công nợ cho dịch vụ trả góp quá hạn.~~

### Trạng thái: 🚧 Đang phát triển

Tính năng sẽ bao gồm:
- Cấu hình các bước theo dõi (5 ngày, 15 ngày, 30 ngày)
- Tự động nhắc nhở cho dịch vụ trả góp quá hạn (sau 12 tháng)
- Hiển thị trạng thái theo dõi trên khách hàng

---

## ✅ Test Case 5: Báo cáo Lợi nhuận

### Mục đích
Test báo cáo lợi nhuận theo tháng với chi phí vật tư tự động từ inventory.

### Các bước test:

1. **Tạo Dữ liệu Test**
   - Tạo một số thanh toán trong tháng hiện tại
   - Tạo các buổi điều trị với vật tư (để có chi phí vật tư tự động)
   - Tạo một số **Thanh toán Định kỳ** đã chạy trong tháng

2. **Tạo Báo cáo Lợi nhuận**
   - Vào **Kế toán Nha khoa** → **Báo cáo Lợi nhuận**
   - Chọn **Tháng**: Tháng hiện tại
   - Hệ thống tự động tính toán:
     - **Doanh thu**: Tổng các thanh toán đã posted trong tháng
     - **Chi phí vật tư**: Tổng chi phí vật tư tự động từ inventory (từ các treatments có payments trong tháng)
     - **Chi phí khác**: Tổng các bút toán định kỳ trong tháng
     - **Tổng chi phí**: Chi phí vật tư + Chi phí khác
     - **Lợi nhuận**: Doanh thu - Tổng chi phí

3. **Kiểm tra Kết quả**
   - Xác minh các số liệu tính toán đúng
   - **Chi phí vật tư** chỉ tính từ treatments có payments trong tháng và có sử dụng vật tư
   - **Lợi nhuận** hiển thị màu xanh nếu > 0, màu đỏ nếu < 0

### Kết quả mong đợi:
- ✅ Báo cáo tính toán đúng doanh thu từ payments
- ✅ Báo cáo tính toán đúng chi phí vật tư tự động từ inventory
- ✅ Báo cáo tính toán đúng chi phí định kỳ
- ✅ Lợi nhuận = Doanh thu - Tổng chi phí
- ✅ Chỉ tính chi phí vật tư từ treatments có payments trong tháng

---

## ✅ Test Case 6: Khóa Ngày Kế toán

### Mục đích
Test chức năng khóa kỳ kế toán để bảo vệ dữ liệu.

### Các bước test:

1. **Truy cập Khóa Ngày**
   - Vào **Hóa đơn** → **Cấu hình** (Configuration) → **Accounting** → **Khóa Ngày**
   - (Chỉ hiển thị cho Account Manager)

2. **Thiết lập Khóa Ngày**
   - **Ngày khóa kỳ (Không phải Cố vấn)**: Chọn ngày 1 tháng trước
   - **Ngày khóa năm tài chính**: Chọn ngày đầu năm
   - Click **Cập nhật**

3. **Kiểm tra Bảo vệ**
   - Thử tạo bút toán với ngày trước ngày khóa
   - Hệ thống sẽ ngăn chặn (nếu user không phải Account Manager)

### Kết quả mong đợi:
- ✅ Chỉ Account Manager mới có thể truy cập
- ✅ Ngày khóa được lưu đúng
- ✅ Hệ thống ngăn chặn chỉnh sửa dữ liệu trước ngày khóa

---

## ✅ Test Case 7: Chi phí Vật tư Tự động (Phase 2)

### Mục đích
Test tính năng tự động tính chi phí vật tư từ inventory module và hiển thị breakdown chi tiết.

### Yêu cầu tiên quyết:
- Module `dental_inventory` phải được cài đặt và kích hoạt
- Đã có vật tư trong inventory với giá mua vào (unit_cost)

### Các bước test:

1. **Tạo Hồ sơ Điều trị với Buổi điều trị**
   - Vào **Quản lý Phòng khám** → **Hồ sơ Điều trị**
   - Tạo mới một hồ sơ điều trị
   - Trong tab **Buổi điều trị**, tạo một buổi điều trị mới:
     - **Ngày thực hiện**: Chọn ngày
     - **Trạng thái**: `Đã hoàn thành`
     - Trong tab **Vật tư sử dụng**, thêm vật tư:
       - **Vật tư**: Chọn vật tư từ inventory (ví dụ: Composite A2)
       - **Số lượng**: `2`
       - **Đơn giá**: Tự động fill từ inventory
       - **Tổng chi phí**: Tự động tính = Số lượng × Đơn giá
     - Lưu buổi điều trị

2. **Kiểm tra Chi phí Vật tư Tự động**
   - **Đối với Clinic Management**: Quay lại form **Hồ sơ Điều trị** trong menu **Quản lý Phòng khám**
   - **Đối với Accountant**: Vào **Hóa đơn** → **Kế toán Nha khoa** → **Hồ sơ điều trị** để truy cập
   - Mở tab **Kế toán**
   - Kiểm tra:
     - **Chi phí vật tư**: Tự động tính = Tổng chi phí của tất cả vật tư trong các buổi điều trị
     - **Lợi nhuận**: Tự động tính = Doanh thu - Chi phí vật tư

3. **Kiểm tra Chi tiết Vật tư trong Buổi điều trị**
   - Để xem chi tiết vật tư đã sử dụng, vào tab **Buổi điều trị** (không phải tab "Kế toán")
   - Mở một buổi điều trị có sử dụng vật tư
   - Trong tab **Vật tư sử dụng**, kiểm tra:
     - **Vật tư**: Tên vật tư (từ inventory)
     - **Số lượng**: Số lượng đã sử dụng
     - **Đơn giá**: Đơn giá tự động từ inventory
     - **Tổng chi phí**: Tự động tính = Số lượng × Đơn giá
   - Tổng chi phí của tất cả vật tư trong tất cả buổi điều trị sẽ được tự động cộng vào **Chi phí vật tư** trong tab **Kế toán**

4. **Test Tự động Cập nhật**
   - Thêm một buổi điều trị mới với vật tư
   - Hoàn thành buổi điều trị (status = 'completed')
   - Kiểm tra **Chi phí vật tư** trong tab **Kế toán** tự động cập nhật

5. **Test với Nhiều Buổi điều trị**
   - Tạo thêm 2-3 buổi điều trị khác với vật tư khác nhau
   - Hoàn thành các buổi điều trị (status = 'completed')
   - Kiểm tra trong tab **Kế toán**:
     - **Chi phí vật tư** = Tổng của tất cả vật tư trong tất cả buổi điều trị
     - Tổng chi phí vật tư khớp với tổng của tất cả vật tư trong tab **Buổi điều trị**

### Kết quả mong đợi:
- ✅ Chi phí vật tư tự động tính từ inventory (không cần nhập thủ công)
- ✅ Đơn giá tự động fill từ inventory khi chọn vật tư
- ✅ Tổng chi phí tự động tính = Số lượng × Đơn giá
- ✅ Chi phí vật tư trong tab **Kế toán** tự động cập nhật khi thêm/sửa/xóa vật tư trong các buổi điều trị
- ✅ Chi tiết vật tư có thể xem trong tab **Buổi điều trị** → **Vật tư sử dụng**
- ✅ Tính toán chính xác với nhiều buổi điều trị và nhiều vật tư

---

## 📝 Lưu Ý Khi Testing

1. **Quyền Truy Cập**:
   - User cần có quyền **Accountant** hoặc **Account Manager**
   - Một số chức năng chỉ dành cho **Account Manager**

2. **Dữ liệu Test**:
   - Tạo đủ dữ liệu test (bệnh nhân, điều trị, thanh toán)
   - Đảm bảo có cả dịch vụ ngắn ngày và dài ngày

3. **Cron Job**:
   - Thanh toán định kỳ cần cron job chạy tự động
   - Có thể chạy thủ công qua **Settings** → **Technical** → **Automated Actions**

4. **Chi phí Vật tư (Phase 2)**:
   - ✅ Tự động tính từ inventory module
   - ✅ Đơn giá tự động lấy từ inventory (từ PO hoặc standard_price)
   - ✅ Tự động cập nhật khi thêm/sửa/xóa vật tư trong buổi điều trị
   - ✅ Yêu cầu module `dental_inventory` phải được cài đặt

5. **Dependencies**:
   - Module `dental_inventory` phải được cài đặt để tính năng chi phí vật tư tự động hoạt động
   - Nếu chưa có `dental_inventory`, chi phí vật tư sẽ = 0

---

## 🐛 Troubleshooting

### Lỗi: Không thấy menu "Kế toán Nha khoa"
- **Giải pháp**: Kiểm tra module đã được cài đặt và kích hoạt chưa
- Vào **Apps** → Tìm "Dental Accounting" → **Install**

### Lỗi: Không tạo được Payment Plan
- **Giải pháp**: Kiểm tra **Chính sách thanh toán** = "Trả góp"
- Đảm bảo chưa có Payment Plan nào cho điều trị đó

### Lỗi: Hóa đơn không tự động tạo
- **Giải pháp**: Kiểm tra checkbox **Tự động tạo hóa đơn** = ✓
- Kiểm tra thanh toán đã được **Post** chưa

### Lỗi: Follow-up không hoạt động
- **Giải pháp**: Follow-up chỉ áp dụng cho dịch vụ trả góp
- Đảm bảo đã qua 12 tháng từ ngày đóng trước

### Lỗi: Chi phí vật tư = 0 hoặc không tự động cập nhật
- **Giải pháp**: 
  - Kiểm tra module `dental_inventory` đã được cài đặt chưa
  - Kiểm tra vật tư đã được chọn trong buổi điều trị chưa
  - Kiểm tra buổi điều trị đã có status = 'completed' chưa
  - Kiểm tra vật tư có `product_id` và `total_cost > 0` chưa
  - Refresh trang để trigger recompute

### Lỗi: Không thấy chi tiết vật tư
- **Giải pháp**: 
  - Chi tiết vật tư nằm trong tab **Buổi điều trị**, không phải tab "Kế toán"
  - Mở một buổi điều trị → Tab **Vật tư sử dụng** để xem chi tiết
  - Tab **Kế toán** chỉ hiển thị tổng **Chi phí vật tư**, không có breakdown chi tiết

---

## 📊 Tóm Tắt Test Cases

| Test Case | Mục đích | Trạng thái |
|-----------|----------|------------|
| Test Case 1 | Dịch vụ Ngắn Ngày (Full Payment) | ✅ Hoàn thành |
| Test Case 2 | Dịch vụ Dài Ngày (Installment) | ✅ Hoàn thành |
| Test Case 3 | Thanh toán Định kỳ | ✅ Hoàn thành |
| Test Case 4 | Theo dõi Công nợ (Follow-up) | ⏸️ Tạm vô hiệu hóa |
| Test Case 5 | Báo cáo Lợi nhuận | ✅ Hoàn thành (Phase 2) |
| Test Case 6 | Khóa Ngày Kế toán | ✅ Hoàn thành |
| Test Case 7 | Chi phí Vật tư Tự động (Phase 2) | ✅ Hoàn thành |

---

**Chúc bạn testing thành công! 🎉**

