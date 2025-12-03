# Tổng Quan Các Module - Hệ Thống Quản Lý Phòng Khám Nha Khoa

## 📋 Tổng Quan Hệ Thống

Hệ thống bao gồm 5 module chính được xây dựng trên Odoo 17.0 để quản lý toàn diện phòng khám nha khoa:

1. **dental_clinic_management** - Module cốt lõi quản lý bệnh nhân và điều trị
2. **dental_inquiry** - Module CRM quản lý inquiry và chuyển đổi thành bệnh nhân
3. **dental_accounting** - Module kế toán, thanh toán và báo cáo tài chính
4. **dental_inventory** - Module quản lý vật tư tiêu hao
5. **dental_hr** - Module quản lý nhân viên, lương và thưởng

---

## 1. 🏥 Module: `dental_clinic_management`

### Mục đích
Module cốt lõi quản lý thông tin bệnh nhân, hồ sơ điều trị và các buổi điều trị.

### Chức năng chính

#### 1.1. Quản lý Bệnh nhân (`dental.patient`)
- **Thông tin cơ bản**: Họ tên, ngày sinh, giới tính, số điện thoại, email, địa chỉ
- **Thông tin y tế**: Tình trạng răng miệng, ghi chú y tế
- **Mã bệnh nhân**: Tự động tạo mã bệnh nhân (BN000, BN001, ...)
- **Liên kết**: Theo dõi tất cả các hồ sơ điều trị của bệnh nhân

#### 1.2. Quản lý Hồ sơ Điều trị (`dental.treatment`)
- **Thông tin điều trị**:
  - Mã hồ sơ tự động (DT000, DT001, ...)
  - Loại điều trị: Niềng răng, Trám răng, Nhổ răng, Tẩy trắng, Cấy ghép, Khác
  - Trạng thái: Lấy thông tin → Khám lâm sàng → Tư vấn → Lên kế hoạch → Đang điều trị → Tái khám → Hoàn thành
  - Bác sĩ phụ trách
  - Ngày bắt đầu và kết thúc dự kiến
- **Tài chính**:
  - Tổng chi phí điều trị
  - Trạng thái thanh toán: Chưa thanh toán / Thanh toán một phần / Đã thanh toán
  - Số tiền đã thanh toán
- **Liên kết**: Quản lý nhiều buổi điều trị (treatment sessions)

#### 1.3. Quản lý Buổi Điều trị (`treatment.session`)
- Lưu trữ thông tin từng buổi điều trị
- Liên kết với hồ sơ điều trị
- Theo dõi vật tư sử dụng trong buổi điều trị

#### 1.4. Quản lý Sử dụng Vật tư (`supply.usage`)
- Theo dõi vật tư sử dụng trong từng buổi điều trị
- (Sau này sẽ được mở rộng bởi module `dental_inventory`)

### Dependencies
- `base`
- `mail` (cho tracking và activities)

### Tích hợp
- Module nền tảng cho các module khác
- Được mở rộng bởi:
  - `dental_accounting` (thêm fields kế toán)
  - `dental_inventory` (quản lý vật tư chi tiết)
  - `dental_hr` (quản lý bác sĩ)

---

## 2. 📞 Module: `dental_inquiry`

### Mục đích
Module CRM quản lý inquiry từ khách hàng tiềm năng, từ lần liên hệ đầu tiên đến khi chuyển đổi thành bệnh nhân.

### Chức năng chính

#### 2.1. Quản lý Inquiry (`crm.lead` - extended)
- **Nguồn inquiry**: Điện thoại, Facebook, Website
- **Thông tin nha khoa**:
  - Vấn đề nha khoa (`dental_issue`)
  - Dịch vụ quan tâm (`treatment_interest`)
  - Mức độ khẩn cấp (`urgency_level`)
- **Workflow stages**:
  - Inquiry mới
  - Đã liên hệ
  - Đã hẹn tư vấn
  - Đã tư vấn - Chờ quyết định
  - Đã đồng ý điều trị
  - Đã chuyển đổi thành bệnh nhân
- **Tự động tạo bệnh nhân**: Khi chuyển sang stage "Đã tư vấn - Chờ quyết định"

#### 2.2. Lên lịch Tư vấn (`calendar.event` - extended)
- Lên lịch hẹn tư vấn từ inquiry
- Tích hợp với calendar của Odoo
- Gửi thông báo và nhắc nhở

#### 2.3. Chuyển đổi thành Bệnh nhân
- **Action chuyển đổi**: Tự động tạo:
  - `res.partner` (nếu chưa có)
  - `dental.patient` (nếu có module `dental_clinic_management`)
  - `dental.treatment` (nếu có module `dental_clinic_management`)
- Liên kết inquiry với bệnh nhân sau khi chuyển đổi

#### 2.4. Quản lý Team và Stages
- Team riêng: "Đội Inquiry Nha khoa"
- Stages tùy chỉnh cho workflow nha khoa
- Không cho phép chuyển ngược lại stage trước

### Dependencies
- `base`
- `crm`
- `calendar`
- `contacts`
- `mail`

### Tích hợp
- Tích hợp với `dental_clinic_management` để tự động tạo bệnh nhân và hồ sơ điều trị
- Hoạt động độc lập nếu chưa có module clinic

---

## 3. 💰 Module: `dental_accounting`

### Mục đích
Module kế toán tích hợp với quản lý phòng khám, quản lý thanh toán, invoice và báo cáo lợi nhuận.

### Chức năng chính

#### 3.1. Chính sách Thanh toán (`dental.treatment` - extended)
- **Full Payment**: Thanh toán toàn bộ ngay (cho dịch vụ ngắn ngày)
- **Installment**: Trả góp 12 tháng (cho dịch vụ dài ngày)

#### 3.2. Payment Plan (`dental.payment.plan`)
- **Thanh toán trước**: 50% tổng số tiền
- **Trả góp**: 12 tháng linh hoạt (có thể bỏ qua hoặc đóng nhiều kỳ)
- **Theo dõi**: 
  - Ngày đóng trước
  - Các kỳ thanh toán
  - Số tiền còn lại
  - Trạng thái hoàn thành

#### 3.3. Quản lý Payment (`account.payment` - extended)
- **Tạo payment từ điều trị**: Nhân viên xác nhận đã nhận tiền
- **Tự động tạo Invoice**: Invoice = Proof of payment (chứng từ thanh toán)
- **Liên kết với Payment Plan**: Tự động cập nhật số tiền đã thanh toán

#### 3.4. Invoice Workflow (`account.move` - extended)
- Invoice được tạo tự động từ Payment
- Invoice là chứng từ thanh toán, không phải từ Treatment trực tiếp
- Tích hợp với Odoo Accounting chuẩn

#### 3.5. Recurring Payments (`dental.recurring.payment`)
- Quản lý chi phí cố định định kỳ (thuê nhà, điện, nước, ...)
- Tự động tạo bút toán kế toán theo lịch
- Cron job tự động xử lý

#### 3.6. Báo cáo Lợi nhuận (`dental.profit.report`)
- **Công thức**: Lợi nhuận = Doanh thu - Chi phí vật tư - Chi phí khác - Chi phí lương
- **Doanh thu**: Từ các payment đã xác nhận
- **Chi phí vật tư**: Từ module `dental_inventory` hoặc nhập tay
- **Chi phí khác**: Từ recurring payments và chi phí khác
- **Chi phí lương**: Từ module `dental_hr`
- Báo cáo theo tháng, quý, năm

#### 3.7. Account Lock Date
- Khóa kỳ kế toán để bảo vệ dữ liệu
- Wizard để unlock khi cần thiết

### Dependencies
- `base`
- `account`
- `analytic`
- `dental_clinic_management`
- `mail`

### Tích hợp
- Mở rộng `dental.treatment` với các fields kế toán
- Tích hợp với `dental_inventory` để lấy chi phí vật tư
- Tích hợp với `dental_hr` để lấy chi phí lương trong báo cáo lợi nhuận

---

## 4. 📦 Module: `dental_inventory`

### Mục đích
Module quản lý vật tư tiêu hao (consumables) cho phòng khám nha khoa.

### Chức năng chính

#### 4.1. Phân loại Vật tư (`dental.supply.category`)
- Phân loại vật tư: Thuốc, Dụng cụ, Vật liệu, Khác
- Quản lý danh mục vật tư có tổ chức

#### 4.2. Quản lý Vật tư (`product.product` - extended)
- **Đánh dấu vật tư**: Field `is_dental_supply`
- **Phân loại**: Liên kết với `dental.supply.category`
- **Tồn kho tối thiểu**: Cảnh báo khi tồn kho thấp
- **Tích hợp Stock**: Sử dụng Odoo Stock để quản lý tồn kho

#### 4.3. Quản lý Sử dụng Vật tư (`supply.usage` - extended)
- **Tự động trừ tồn kho**: Khi sử dụng trong buổi điều trị
- **Tính chi phí**: Tự động tính `unit_cost` và `total_cost`
- **Liên kết với Treatment**: Cập nhật `supply_cost` của điều trị

#### 4.4. Tích hợp Purchase (`purchase.order` - extended)
- Quản lý đơn mua vật tư
- Tự động lấy giá mua từ Purchase Order
- Cập nhật giá vật tư từ đơn mua

#### 4.5. Tích hợp Stock (`stock.move`, `stock.picking` - extended)
- Quản lý nhập kho, xuất kho
- Tự động cập nhật tồn kho khi validate picking
- Tracking vật tư qua các kho

#### 4.6. Cảnh báo Tồn kho thấp (`dental.low.stock.alert`)
- Tự động phát hiện vật tư có tồn kho < mức tối thiểu
- Cron job chạy định kỳ để kiểm tra
- Danh sách cảnh báo để nhân viên theo dõi

#### 4.7. Báo cáo Sử dụng Vật tư (`dental.supply.usage.report`)
- Báo cáo vật tư sử dụng theo thời gian
- Phân tích chi phí vật tư
- Báo cáo tồn kho

### Dependencies
- `base`
- `stock`
- `purchase`
- `dental_clinic_management`

### Tích hợp
- Mở rộng `supply.usage` từ `dental_clinic_management`
- Tích hợp với `dental_accounting` để tự động cập nhật `supply_cost`

---

## 5. 👥 Module: `dental_hr`

### Mục đích
Module quản lý nhân viên nha khoa, tính lương, thưởng và tích hợp với kế toán.

### Chức năng chính

#### 5.1. Vai trò Nhân viên (`dental.role`)
- **Các vai trò**: Bác sĩ, Kỹ thuật viên, Lễ tân, Kế toán, Quản lý kho
- Phân quyền và quản lý nhân viên theo vai trò

#### 5.2. Mở rộng Employee (`hr.employee` - extended)
- **Thông tin nha khoa**: Vai trò, chuyên môn
- **Liên kết**: Với hợp đồng lao động
- **Quản lý nghỉ phép**: Tích hợp với `hr_holidays`

#### 5.3. Tính Lương (`dental.salary`)
- **Lương cơ bản**: Từ hợp đồng lao động (`hr.contract`)
- **Thưởng**: Liên kết với các khoản thưởng đã phê duyệt
- **Tổng lương**: Lương cơ bản + Thưởng
- **Theo tháng**: Quản lý lương theo từng tháng
- **Bút toán kế toán**: Tự động tạo bút toán kế toán khi tính lương
- **Journal Entry**: Tích hợp với Odoo Accounting

#### 5.4. Quản lý Thưởng (`dental.bonus`)
- **Các loại thưởng**: Thưởng hiệu suất, thưởng doanh số, thưởng đặc biệt
- **Workflow**: Draft → Submitted → Confirmed → Paid
- **Liên kết với Lương**: Chỉ thưởng đã confirmed mới được tính vào lương

#### 5.5. Tích hợp với Accounting
- **Bút toán lương**: Tự động tạo journal entry khi tính lương
- **Chi phí lương trong báo cáo**: Hiển thị trong báo cáo lợi nhuận
- **Journal riêng**: "Chi phí lương" journal để tách biệt

#### 5.6. Quản lý Nghỉ phép
- Tích hợp với `hr_holidays`
- Smart button trên employee form để xem nghỉ phép
- Theo dõi số ngày nghỉ còn lại

### Dependencies
- `base`
- `hr`
- `hr_contract`
- `hr_holidays`
- `account`

### Tích hợp
- Tích hợp với `dental_accounting` để hiển thị chi phí lương trong báo cáo lợi nhuận
- Tích hợp với các module Odoo HR chuẩn

---

## 🔗 Sơ đồ Tích hợp Giữa Các Module

```
┌─────────────────────────┐
│ dental_inquiry          │  ────> Tạo patient khi convert
│ (CRM - Inquiry)         │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ dental_clinic_management│  ◄─── Module cốt lõi
│ (Patient & Treatment)   │
└──────────┬──────────────┘
           │
     ┌─────┴─────┬──────────────┬─────────────┐
     ▼           ▼              ▼             ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐
│dental_  │ │dental_   │ │dental_   │ │dental_hr│
│accounting│ │inventory │ │inventory │ │         │
│         │ │          │ │          │ │         │
│Payment  │ │Supplies  │ │Supplies  │ │Salary & │
│& Profit │ │Usage     │ │Cost      │ │Bonus    │
└─────────┘ └──────────┘ └──────────┘ └─────────┘
     │           │              │             │
     └───────────┴──────────────┴─────────────┘
                    │
                    ▼
              ┌──────────┐
              │ Profit   │
              │ Report   │
              │ (Revenue │
              │ - Costs) │
              └──────────┘
```

---

## 📊 Workflow Tổng Thể

### 1. Inquiry → Patient
```
Khách hàng liên hệ (Phone/Facebook/Website)
    ↓
[dental_inquiry] Tạo Inquiry
    ↓
Lên lịch tư vấn (Calendar Event)
    ↓
Tư vấn và chuyển đổi
    ↓
[dental_clinic_management] Tạo Patient & Treatment
```

### 2. Treatment → Payment
```
[dental_clinic_management] Tạo Treatment
    ↓
Chọn Payment Policy (Full/Installment)
    ↓
[dental_accounting] Tạo Payment Plan (nếu Installment)
    ↓
Nhận thanh toán → Tạo Payment
    ↓
Tự động tạo Invoice (Proof of payment)
    ↓
Cập nhật payment_status của Treatment
```

### 3. Treatment → Inventory
```
[dental_clinic_management] Tạo Treatment Session
    ↓
Sử dụng vật tư trong session
    ↓
[dental_inventory] Tự động trừ tồn kho
    ↓
Tính chi phí vật tư (unit_cost từ Purchase)
    ↓
Cập nhật supply_cost vào Treatment
```

### 4. Salary & Bonus
```
[dental_hr] Tạo Bonus → Phê duyệt
    ↓
Tính lương tháng (Base Salary + Bonus)
    ↓
Tạo Journal Entry (Kế toán)
    ↓
[dental_accounting] Hiển thị trong Profit Report
```

---

## 🎯 Các Module Độc Lập vs Phụ Thuộc

### Module độc lập (có thể chạy riêng):
- ✅ `dental_inquiry` - Có thể hoạt động độc lập, chỉ cần CRM
- ✅ `dental_clinic_management` - Module cốt lõi, độc lập

### Module phụ thuộc:
- ⚠️ `dental_accounting` - Cần `dental_clinic_management`
- ⚠️ `dental_inventory` - Cần `dental_clinic_management`
- ⚠️ `dental_hr` - Cần các module HR của Odoo (độc lập với các module dental khác)

### Module có tích hợp chéo:
- 🔄 `dental_accounting` ↔ `dental_inventory` (supply_cost)
- 🔄 `dental_accounting` ↔ `dental_hr` (salary_cost trong profit report)

---

## 📝 Ghi chú Quan trọng

1. **Module cốt lõi**: `dental_clinic_management` là nền tảng, các module khác mở rộng từ đây

2. **Tích hợp kế toán**: Invoice được tạo từ Payment (không phải từ Treatment), theo nguyên tắc "Invoice = Proof of payment"

3. **Payment Policy**:
   - Dịch vụ ngắn ngày: Full payment
   - Dịch vụ dài ngày: Installment (50% trước, 12 tháng)

4. **Chi phí vật tư**: Tự động tính từ `dental_inventory`, có thể nhập tay tạm thời

5. **Báo cáo lợi nhuận**: Tổng hợp từ nhiều nguồn:
   - Doanh thu: từ Payments
   - Chi phí vật tư: từ Inventory
   - Chi phí lương: từ HR
   - Chi phí khác: từ Recurring Payments

---

*Tài liệu này được tạo để mô tả toàn bộ hệ thống module. Cập nhật ngày: 2024*

