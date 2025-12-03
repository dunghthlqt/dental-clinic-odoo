# Dental Accounting Module

Module tích hợp kế toán với quản lý phòng khám nha khoa.

## Tính năng

### 1. Payment Policy
- **Full Payment**: Thanh toán toàn bộ (dịch vụ ngắn ngày)
- **Installment**: Trả góp 12 tháng (dịch vụ dài ngày)

### 2. Payment Plan
- Đóng trước 50% (kỳ 1)
- 12 tháng còn lại: Linh hoạt (có thể skip hoặc đóng nhiều)
- Tự động tính "Đã đóng" và "Còn lại"
- Follow-up sau 12 tháng nếu còn nợ

### 3. Invoice Workflow
- Invoice được tạo từ Payment (không phải từ Treatment)
- Invoice = Proof of payment (chứng từ thanh toán)
- Hiển thị "Số tiền còn lại" trên invoice

### 4. Follow-up
- Chỉ áp dụng cho dịch vụ dài ngày (installment)
- Timing: Sau 12 tháng từ ngày đóng 50%
- Tự động nhắc nhở khi quá hạn

### 5. Recurring Payments
- Quản lý chi phí cố định (thuê, lương...)
- Tự động tạo journal entries theo lịch
- Cron job chạy hàng ngày

### 6. Profit Calculation
- Revenue = Tổng payments đã nhận
- Cost = Supply cost (manual) + Other costs (recurring)
- Profit = Revenue - Cost

### 7. Lock Dates
- Khóa ngày kế toán
- Period lock date và Fiscal year lock date

## Cài đặt

1. Đảm bảo module `dental_clinic_management` đã được cài đặt
2. Update Apps List trong Odoo
3. Tìm và cài đặt module "Dental Accounting"

## Dependencies

- `dental_clinic_management` (required)
- `account` (Odoo core)
- `analytic` (Odoo core)
- `mail` (Odoo core)

## Workflow

### Dịch vụ ngắn ngày
1. Tạo treatment → `payment_policy = 'full_payment'`
2. Bệnh nhân thanh toán → Nhân viên nhận tiền
3. Tạo Payment → Tự động tạo Invoice
4. Invoice hiển thị "Số tiền còn lại = 0"

### Dịch vụ dài ngày
1. Tạo treatment → `payment_policy = 'installment'`
2. Tạo Payment Plan (50% upfront)
3. Bệnh nhân đóng kỳ 1 → Payment → Invoice
4. Bệnh nhân đóng các kỳ tiếp theo (linh hoạt)
5. Sau 12 tháng: Nếu còn nợ → Follow-up

## Ghi chú

- Supply cost: Tạm thời manual input (sẽ auto từ inventory ở Giai đoạn 2)
- Follow-up: Chỉ áp dụng cho installment treatments
- Invoice: Được tạo từ payment, không phải từ treatment

## Giai đoạn 2

Sau khi có Inventory module:
- Tự động tính `supply_cost` từ inventory
- Link `supply.usage` với inventory
- Auto-fill `unit_cost` từ inventory

