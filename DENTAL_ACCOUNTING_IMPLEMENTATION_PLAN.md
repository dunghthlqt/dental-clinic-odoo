# Dental Accounting Module - Kế Hoạch Triển Khai

## 📋 Tổng Quan

Module `dental_accounting` tích hợp hệ thống kế toán với quản lý phòng khám nha khoa, bao gồm:
- Quản lý thanh toán cho dịch vụ ngắn ngày và dài ngày
- Payment Plan cho dịch vụ trả góp (12 tháng)
- Tạo invoice từ payment (proof of payment)
- Theo dõi công nợ và follow-up
- Tính toán lợi nhuận (revenue - costs)
- Báo cáo tài chính

**Odoo Version**: 17.0  
**Dependencies**: 
- `dental_clinic_management`
- `account` (Odoo core)
- `analytic` (Odoo core - cho recurring payments)

**Note**: Thay vì phụ thuộc vào `base_accounting_kit` (custom module từ marketplace), chúng ta sẽ implement trực tiếp các tính năng cần thiết vào `dental_accounting` bằng cách copy & adapt code từ `base_accounting_kit`. Điều này giúp:
- Độc lập, không phụ thuộc module bên ngoài
- Chỉ implement những gì cần thiết
- Dễ customize cho workflow nha khoa
- Full control over code

---

## 🎯 Nguyên Tắc Thiết Kế

1. **Invoice Workflow**: Invoice được tạo từ Payment (không phải từ Treatment)
   - Invoice = Proof of payment (chứng từ thanh toán)
   - Nhân viên xác nhận đã nhận tiền → Tạo Payment → Tự động tạo Invoice

2. **Payment Policy**:
   - **Dịch vụ ngắn ngày**: `full_payment` - Thanh toán toàn bộ, không cho nợ
   - **Dịch vụ dài ngày**: `installment` - Trả góp 12 tháng, cho phép nợ

3. **Payment Plan**:
   - Đóng trước 50% (kỳ 1)
   - 12 tháng còn lại: Linh hoạt (có thể skip hoặc đóng nhiều)
   - Sau 12 tháng từ ngày đóng 50% → Follow-up nếu còn nợ

4. **Supply Cost**: 
   - Giai đoạn 1: Manual input (tạm thời)
   - Giai đoạn 2: Tự động từ Inventory module

5. **Follow-up**: Chỉ áp dụng cho dịch vụ dài ngày (`installment`)

---

## 📦 Cấu Trúc Module

```
dental_accounting/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── dental_treatment.py          # Extend dental.treatment
│   ├── payment_plan.py               # NEW: Payment Plan model
│   ├── account_payment.py            # Extend account.payment
│   ├── account_move.py               # Extend account.move (Invoice)
│   ├── account_followup.py           # NEW: Follow-up (copy & adapt từ base_accounting_kit)
│   ├── recurring_payments.py        # NEW: Recurring payments (copy & adapt)
│   ├── account_lock_date.py         # NEW: Lock dates (copy & adapt)
│   ├── profit_report.py             # NEW: Profit report model
│   └── financial_reports.py         # NEW: Financial reports (customize)
├── views/
│   ├── dental_treatment_views.xml
│   ├── payment_plan_views.xml
│   ├── invoice_views.xml
│   ├── followup_views.xml           # NEW: Follow-up views
│   ├── recurring_payments_views.xml  # NEW: Recurring payments views
│   ├── lock_date_views.xml          # NEW: Lock date wizard
│   ├── profit_report_views.xml
│   └── accounting_menu.xml
├── wizard/
│   ├── __init__.py
│   └── account_lock_date.py         # NEW: Lock date wizard
├── security/
│   ├── dental_accounting_security.xml
│   └── ir.model.access.csv
├── data/
│   ├── payment_plan_data.xml
│   └── followup_levels.xml          # NEW: Follow-up default data
├── reports/
│   ├── profit_report.xml
│   └── financial_reports.xml        # NEW: Financial report templates
└── static/
    └── description/
        └── icon.png
```

---

## 📚 Strategy: Copy & Adapt từ base_accounting_kit

### Tại sao không dùng Dependency?

**Vấn đề với dependency:**
- Module từ marketplace có thể thay đổi/update → rủi ro conflict
- Có nhiều tính năng không cần (PDC, Credit Limit...)
- Khó customize sâu cho workflow nha khoa
- Phụ thuộc vào module bên ngoài → khó maintain

**Ưu điểm của Copy & Adapt:**
- ✅ Độc lập, không phụ thuộc
- ✅ Chỉ implement những gì cần thiết
- ✅ Full control, dễ customize
- ✅ Code phù hợp với workflow nha khoa

### Files cần Copy từ base_accounting_kit

#### 1. Follow-up Logic
**Source**: `base_accounting_kit/models/account_followup.py`
- Copy: `account.followup` và `followup.line` models
- Adapt: Filter chỉ cho `installment` treatments
- Adapt: Timing logic (12 tháng từ upfront payment)

#### 2. Recurring Payments
**Source**: `base_accounting_kit/models/recurring_payments.py`
- Copy: `account.recurring.payments` model
- Copy: Cron job logic
- Adapt: Không cần thay đổi nhiều (chi phí chung)

#### 3. Lock Dates
**Source**: `base_accounting_kit/wizard/account_lock_date.py`
- Copy: Wizard model và logic
- Copy: `res.company` extension
- Adapt: Không cần thay đổi (standard feature)

#### 4. Financial Reports
**Source**: `base_accounting_kit/report/`
- Copy: Report templates (Trial Balance, P&L, Cash Flow...)
- Adapt: Customize cho dental-specific reports
- Adapt: Filter theo treatment types

### Cách thực hiện

1. **Copy code** từ `base_accounting_kit` vào `dental_accounting`
2. **Rename models/fields** nếu cần để tránh conflict
3. **Adapt logic** cho workflow nha khoa:
   - Follow-up: Filter theo payment_policy
   - Reports: Thêm dental-specific fields
4. **Remove** những phần không cần (PDC, Credit Limit...)
5. **Test** kỹ để đảm bảo hoạt động đúng

---

## 🚀 GIAI ĐOẠN 1: Triển Khai Không Cần Inventory

### Mục Tiêu
Triển khai các tính năng cốt lõi không phụ thuộc vào Inventory module:
- Payment Plan và quản lý thanh toán
- Invoice workflow (tạo từ payment)
- Follow-up cho dịch vụ dài ngày
- Báo cáo lợi nhuận (supply_cost manual)

---

### 1. Module Setup

#### 1.1. Tạo Module Structure
- [ ] Tạo thư mục `dental_accounting/`
- [ ] Tạo `__init__.py` và `__manifest__.py`
- [ ] Tạo cấu trúc thư mục: `models/`, `views/`, `security/`, `data/`, `reports/`

#### 1.2. Manifest Configuration
```python
{
    'name': 'Dental Accounting',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Accounting',
    'summary': 'Accounting integration for dental clinic',
    'depends': [
        'base',
        'account',
        'analytic',  # Cho recurring payments
        'dental_clinic_management',
    ],
    'data': [
        'security/dental_accounting_security.xml',
        'security/ir.model.access.csv',
        'data/payment_plan_data.xml',
        'views/dental_treatment_views.xml',
        'views/payment_plan_views.xml',
        'views/invoice_views.xml',
        'views/profit_report_views.xml',
        'views/accounting_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

---

### 2. Extend Dental Treatment Model

#### 2.1. File: `models/dental_treatment.py`

**Mục đích**: Mở rộng `dental.treatment` với các fields kế toán

**Công việc**:
- [ ] Inherit `dental.treatment` model
- [ ] Thêm field `payment_policy`:
  ```python
  payment_policy = fields.Selection([
      ('full_payment', 'Thanh toán toàn bộ'),
      ('installment', 'Trả góp'),
  ], string='Chính sách thanh toán', default='full_payment')
  ```
- [ ] Thêm field `payment_plan_id` (Many2one to `dental.payment.plan`)
- [ ] Thêm field `supply_cost` (tạm thời manual):
  ```python
  supply_cost = fields.Float(
      'Chi phí vật tư',
      help='Chi phí vật tư (tạm thời manual, sau sẽ auto từ inventory)'
  )
  ```
- [ ] Thêm computed fields:
  ```python
  revenue = fields.Float('Doanh thu', compute='_compute_revenue', store=True)
  profit = fields.Float('Lợi nhuận', compute='_compute_profit', store=True)
  ```
- [ ] Implement `_compute_revenue()`:
  - Tính tổng payments đã posted cho treatment này
- [ ] Implement `_compute_profit()`:
  - `profit = revenue - supply_cost`
- [ ] Thêm method `action_create_payment_plan()`:
  - Tạo Payment Plan cho treatment có `payment_policy = 'installment'`

**Dependencies**: `dental_clinic_management`

---

### 3. Payment Plan Model (NEW)

#### 3.1. File: `models/payment_plan.py`

**Mục đích**: Quản lý kế hoạch thanh toán trả góp 12 tháng

**Công việc**:
- [ ] Tạo model `dental.payment.plan`:
  ```python
  _name = 'dental.payment.plan'
  _description = 'Payment Plan for Dental Treatment'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  ```
- [ ] Fields:
  ```python
  treatment_id = fields.Many2one('dental.treatment', required=True)
  total_amount = fields.Float('Tổng số tiền', related='treatment_id.total_cost')
  upfront_payment = fields.Float('Đóng trước', compute='_compute_upfront')
  upfront_payment_date = fields.Date('Ngày đóng trước', required=True)
  installment_period = fields.Integer('Số tháng trả góp', default=12)
  end_date = fields.Date('Ngày kết thúc', compute='_compute_end_date')
  total_paid = fields.Float('Đã thanh toán', compute='_compute_total_paid')
  remaining_amount = fields.Float('Còn lại', compute='_compute_remaining')
  is_overdue = fields.Boolean('Quá hạn', compute='_compute_is_overdue')
  payment_ids = fields.One2many('account.payment', 'payment_plan_id')
  ```
- [ ] Computed methods:
  - `_compute_upfront()`: 50% của total_amount
  - `_compute_end_date()`: upfront_payment_date + 12 tháng
  - `_compute_total_paid()`: Tổng payments đã posted
  - `_compute_remaining()`: total_amount - total_paid
  - `_compute_is_overdue()`: Sau 12 tháng và còn nợ → True
- [ ] Constraints:
  - `upfront_payment` phải = 50% của `total_amount`
  - `installment_period` = 12 (cố định)

**Dependencies**: `dental_clinic_management`, `account`

---

### 4. Extend Account Payment Model

#### 4.1. File: `models/account_payment.py`

**Mục đích**: Tạo invoice tự động từ payment

**Công việc**:
- [ ] Inherit `account.payment` model
- [ ] Thêm fields:
  ```python
  dental_treatment_id = fields.Many2one('dental.treatment', 'Điều trị liên quan')
  payment_plan_id = fields.Many2one('dental.payment.plan', 'Payment Plan')
  auto_create_invoice = fields.Boolean('Tự động tạo hóa đơn', default=True)
  ```
- [ ] Override `action_post()`:
  - Sau khi payment được posted
  - Nếu `auto_create_invoice = True` và có `dental_treatment_id`
  - Gọi `_create_invoice_from_payment()`
- [ ] Implement `_create_invoice_from_payment()`:
  - Tạo `account.move` (invoice) từ payment
  - Invoice type: `out_invoice` hoặc `out_receipt`
  - Invoice amount = payment amount
  - Link invoice với treatment
  - Link invoice với payment
- [ ] Validation:
  - Kiểm tra payment amount không vượt quá remaining amount của treatment

**Dependencies**: `account`, `dental_clinic_management`

---

### 5. Extend Account Move (Invoice) Model

#### 5.1. File: `models/account_move.py`

**Mục đích**: Hiển thị thông tin treatment và số tiền còn lại trên invoice

**Công việc**:
- [ ] Inherit `account.move` model
- [ ] Thêm fields:
  ```python
  dental_treatment_id = fields.Many2one('dental.treatment', 'Điều trị liên quan')
  treatment_total_cost = fields.Float('Tổng chi phí điều trị', related='dental_treatment_id.total_cost')
  treatment_paid_amount = fields.Float('Đã thanh toán', compute='_compute_treatment_paid')
  treatment_remaining = fields.Float('Số tiền còn lại', compute='_compute_treatment_remaining')
  ```
- [ ] Computed methods:
  - `_compute_treatment_paid()`: Tổng payments đã posted cho treatment
  - `_compute_treatment_remaining()`: total_cost - paid_amount
- [ ] Domain cho `dental_treatment_id`:
  - Chỉ hiển thị treatments của partner (bệnh nhân)

**Dependencies**: `account`, `dental_clinic_management`

---

### 6. Implement Follow-up Logic (Copy & Adapt)

#### 6.1. File: `models/account_followup.py`

**Mục đích**: Implement follow-up logic (copy từ `base_accounting_kit` và customize)

**Công việc**:
- [ ] Copy models từ `base_accounting_kit/models/account_followup.py`:
  - `account.followup` model
  - `followup.line` model
- [ ] Extend `res.partner` với follow-up fields:
  - `total_due`, `total_overdue`
  - `next_reminder_date`, `followup_status`
  - Computed methods để tính toán
- [ ] Customize filter logic:
  - Chỉ áp dụng cho invoices có `dental_treatment_id.payment_policy = 'installment'`
  - Chỉ hiển thị invoices từ treatments có `payment_plan_id.is_overdue = True`
  - Timing: Sau 12 tháng từ `upfront_payment_date`
- [ ] Create follow-up report:
  - Filter theo payment_policy
  - Hiển thị thông tin treatment trong report

**Dependencies**: `account`, `dental_clinic_management`

**Source**: Copy & adapt từ `base_accounting_kit/models/account_followup.py`

---

### 7. Implement Recurring Payments (Copy & Adapt)

#### 7.1. File: `models/recurring_payments.py`

**Mục đích**: Quản lý chi phí cố định (thuê, lương...) - copy từ `base_accounting_kit`

**Công việc**:
- [ ] Copy models từ `base_accounting_kit/models/recurring_payments.py`:
  - `account.recurring.payments` model
  - `account.recurring.entries.line` model
  - Extend `account.move` với `recurring_ref` field
- [ ] Implement cron job:
  - Tự động tạo journal entries theo lịch
  - `_cron_generate_entries()` method
- [ ] Views:
  - Form view cho recurring payment template
  - Tree view để quản lý
- [ ] Note: Không link với treatment (chi phí chung)

**Dependencies**: `account`, `analytic`

**Source**: Copy & adapt từ `base_accounting_kit/models/recurring_payments.py`

---

### 8. Implement Lock Dates (Copy & Adapt)

#### 8.1. File: `wizard/account_lock_date.py`

**Mục đích**: Khóa ngày kế toán - copy từ `base_accounting_kit`

**Công việc**:
- [ ] Copy wizard từ `base_accounting_kit/wizard/account_lock_date.py`:
  - `account.lock.date` transient model
  - `period_lock_date` và `fiscalyear_lock_date` fields
- [ ] Extend `res.company` model:
  - Validation logic khi set lock dates
  - Check unposted entries trước khi lock
- [ ] Views:
  - Wizard form để set lock dates
  - Menu item trong Accounting

**Dependencies**: `account`

**Source**: Copy & adapt từ `base_accounting_kit/wizard/account_lock_date.py`

---

### 9. Profit Report Model

#### 7.1. File: `models/profit_report.py`

**Mục đích**: Báo cáo lợi nhuận theo tháng

**Công việc**:
- [ ] Tạo model `dental.profit.report` (TransientModel):
  ```python
  _name = 'dental.profit.report'
  _description = 'Dental Profit Report'
  ```
- [ ] Fields:
  ```python
  month = fields.Date('Tháng', required=True)
  revenue = fields.Float('Doanh thu', compute='_compute_profit_data')
  supply_cost = fields.Float('Chi phí vật tư', compute='_compute_profit_data')
  other_costs = fields.Float('Chi phí khác', compute='_compute_profit_data')
  total_cost = fields.Float('Tổng chi phí', compute='_compute_total_cost')
  profit = fields.Float('Lợi nhuận', compute='_compute_profit')
  ```
- [ ] Computed methods:
  - `_compute_profit_data()`: Tính revenue, supply_cost, other_costs từ data
  - `_compute_total_cost()`: supply_cost + other_costs
  - `_compute_profit()`: revenue - total_cost
- [ ] Wizard để chọn tháng báo cáo

**Dependencies**: `account`, `dental_clinic_management`

---

### 8. Views

#### 8.1. File: `views/dental_treatment_views.xml`

**Công việc**:
- [ ] Extend form view của `dental.treatment`:
  - Thêm tab "Kế toán"
  - Hiển thị `payment_policy`
  - Hiển thị `payment_plan_id` (nếu có)
  - Hiển thị `supply_cost` (manual input)
  - Hiển thị `revenue`, `profit` (readonly)
  - Button "Tạo Payment Plan" (nếu `payment_policy = 'installment'` và chưa có plan)
- [ ] Extend tree view:
  - Thêm columns: `payment_policy`, `revenue`, `profit`

#### 8.2. File: `views/payment_plan_views.xml`

**Công việc**:
- [ ] Form view cho `dental.payment.plan`:
  - Hiển thị thông tin treatment
  - Hiển thị `total_amount`, `upfront_payment`, `upfront_payment_date`
  - Hiển thị `total_paid`, `remaining_amount` (readonly)
  - Hiển thị `is_overdue` (badge)
  - One2many field `payment_ids` (tree view)
  - Smart button: "Payments", "Invoices"
- [ ] Tree view:
  - Columns: treatment, total_amount, total_paid, remaining_amount, is_overdue
- [ ] Kanban view (optional):
  - Cards hiển thị payment plans theo trạng thái

#### 8.3. File: `views/invoice_views.xml`

**Công việc**:
- [ ] Extend form view của `account.move`:
  - Thêm field `dental_treatment_id` (nếu invoice type = out_invoice/out_receipt)
  - Hiển thị `treatment_total_cost`, `treatment_paid_amount`, `treatment_remaining`
  - Thêm section "Thông tin điều trị" (nếu có treatment)
- [ ] Extend tree view:
  - Thêm column `dental_treatment_id` (optional)

#### 8.4. File: `views/profit_report_views.xml`

**Công việc**:
- [ ] Wizard form để chọn tháng báo cáo
- [ ] Report view (tree/pivot):
  - Hiển thị revenue, supply_cost, other_costs, profit theo tháng
  - Pivot view để phân tích theo nhiều dimensions

#### 8.5. File: `views/followup_views.xml`

**Công việc**:
- [ ] Form view cho `account.followup`:
  - Hiển thị follow-up lines
  - Configure delay và actions
- [ ] Form view cho `followup.line`:
  - Delay (số ngày)
  - Action name
- [ ] Follow-up report view:
  - List customers với overdue invoices
  - Filter theo dental treatment

#### 8.6. File: `views/recurring_payments_views.xml`

**Công việc**:
- [ ] Form view cho `account.recurring.payments`:
  - Debit/credit accounts
  - Journal, amount, period
  - Recurring schedule
- [ ] Tree view:
  - List recurring payment templates
  - Status (draft/running)

#### 8.7. File: `views/lock_date_views.xml`

**Công việc**:
- [ ] Wizard form:
  - Period lock date
  - Fiscal year lock date
  - Update button

#### 8.8. File: `views/accounting_menu.xml`

**Công việc**:
- [ ] Tạo menu "Dental Accounting" trong Accounting app
- [ ] Sub-menus:
  - Payment Plans
  - Profit Reports
  - Follow-up (NEW)
  - Recurring Payments (NEW)
  - Lock Dates (NEW)

---

### 9. Security

#### 9.1. File: `security/dental_accounting_security.xml`

**Công việc**:
- [ ] Tạo security groups:
  - `group_dental_accountant`: Kế toán nha khoa
  - `group_dental_account_manager`: Quản lý kế toán
- [ ] Record rules:
  - Accountant: Chỉ xem/sửa records của mình
  - Manager: Full access

#### 9.2. File: `security/ir.model.access.csv`

**Công việc**:
- [ ] Access rights cho:
  - `dental.payment.plan`
  - `dental.profit.report`
  - Extend access cho `dental.treatment`, `account.payment`, `account.move`

---

### 10. Data

#### 10.1. File: `data/payment_plan_data.xml`

**Công việc**:
- [ ] Default data (nếu cần):
  - Payment plan templates
  - Sequence numbers

#### 10.2. File: `data/followup_levels.xml`

**Công việc**:
- [ ] Default follow-up levels:
  - Level 1: 5 ngày (Reminder)
  - Level 2: 15 ngày (Warning)
  - Level 3: 30 ngày (Final notice)

---

### 11. Reports

#### 11.1. File: `reports/profit_report.xml`

**Công việc**:
- [ ] QWeb report template cho Profit Report
- [ ] PDF layout cho báo cáo lợi nhuận

#### 11.2. File: `reports/financial_reports.xml`

**Công việc**:
- [ ] Financial report templates (copy & customize từ base_accounting_kit):
  - Trial Balance
  - Profit & Loss
  - Cash Flow
  - General Ledger
- [ ] Customize cho dental-specific:
  - Filter theo treatment types
  - Revenue breakdown

---

### 12. Testing Giai Đoạn 1

**Test Cases**:
- [ ] Tạo treatment với `payment_policy = 'full_payment'`
  - Tạo payment → Invoice được tạo tự động
  - Invoice hiển thị "Số tiền còn lại = 0"
- [ ] Tạo treatment với `payment_policy = 'installment'`
  - Tạo Payment Plan (50% upfront)
  - Đóng kỳ 1 → Invoice hiển thị "Số tiền còn lại"
  - Đóng kỳ 2 (linh hoạt) → Invoice cập nhật "Số tiền còn lại"
  - Sau 12 tháng: Nếu còn nợ → Follow-up hiển thị
- [ ] Supply cost manual:
  - Nhập supply_cost thủ công
  - Profit = revenue - supply_cost
- [ ] Profit Report:
  - Chọn tháng → Hiển thị revenue, costs, profit

---

## 🔄 GIAI ĐOẠN 2: Tích Hợp Với Inventory Module

### Mục Tiêu
Tự động hóa tính toán `supply_cost` từ Inventory module:
- Link `supply.usage` với inventory
- Tự động tính `supply_cost` từ vật tư đã sử dụng
- Cập nhật profit calculation

---

### 1. Extend Supply Usage Model

#### 1.1. File: `models/supply_usage.py` (extend từ inventory module)

**Công việc**:
- [ ] Inherit `supply.usage` model (từ `dental_inventory` hoặc `dental_clinic_management`)
- [ ] Thêm field `unit_cost`:
  ```python
  unit_cost = fields.Float(
      'Đơn giá',
      help='Giá mua vào của vật tư (từ inventory)'
  )
  ```
- [ ] Thêm field `total_cost`:
  ```python
  total_cost = fields.Float(
      'Tổng chi phí',
      compute='_compute_total_cost',
      store=True
  )
  ```
- [ ] Computed method:
  - `_compute_total_cost()`: `quantity * unit_cost`
- [ ] Auto-fill `unit_cost`:
  - Khi chọn vật tư từ inventory
  - Lấy giá từ inventory (product.standard_price hoặc purchase_price)

**Dependencies**: `dental_inventory` (sẽ tạo sau)

---

### 2. Update Dental Treatment Model

#### 2.1. File: `models/dental_treatment.py` (update)

**Công việc**:
- [ ] Update `_compute_supply_cost()`:
  - Thay vì manual input
  - Tính tự động từ `treatment.session_ids.supply_ids.total_cost`
  - Sum tất cả supply costs từ các sessions
- [ ] Remove manual `supply_cost` field (hoặc giữ làm backup)
- [ ] Update `_compute_profit()`:
  - Vẫn dùng công thức: `revenue - supply_cost`
  - Nhưng supply_cost giờ là auto-calculated

**Dependencies**: `dental_inventory`

---

### 3. Integration Points

#### 3.1. Treatment Session → Supply Usage → Inventory

**Workflow**:
```
1. Bác sĩ tạo treatment.session
2. Chọn vật tư từ inventory (supply_ids)
3. Inventory module:
   - Ghi nhận vật tư đã sử dụng
   - Lấy unit_cost từ inventory
4. Accounting module:
   - Tự động tính supply_cost = sum(quantity * unit_cost)
   - Cập nhật vào treatment.supply_cost
```

**Công việc**:
- [ ] Tạo method `_onchange_supply_ids()`:
  - Khi chọn vật tư trong session
  - Tự động fill `unit_cost` từ inventory
- [ ] Tạo method `_compute_session_supply_cost()`:
  - Tính tổng chi phí vật tư của session
- [ ] Update `treatment._compute_supply_cost()`:
  - Sum supply costs từ tất cả sessions

**Dependencies**: `dental_inventory`, `dental_clinic_management`

---

### 4. Update Views

#### 4.1. File: `views/dental_treatment_views.xml` (update)

**Công việc**:
- [ ] Update form view:
  - `supply_cost` field: readonly (auto-calculated)
  - Thêm note: "Chi phí vật tư được tính tự động từ inventory"
  - Hiển thị breakdown: supply_cost từ từng session

#### 4.2. File: `views/treatment_session_views.xml` (nếu có)

**Công việc**:
- [ ] Extend treatment session form:
  - Supply usage: Hiển thị `unit_cost`, `total_cost`
  - Auto-fill `unit_cost` khi chọn vật tư

**Dependencies**: `dental_inventory`

---

### 5. Testing Giai Đoạn 2

**Test Cases**:
- [ ] Tạo treatment session → Chọn vật tư từ inventory
  - `unit_cost` tự động fill từ inventory
  - `total_cost` = quantity * unit_cost
- [ ] Tạo nhiều sessions với vật tư
  - `treatment.supply_cost` = sum của tất cả sessions
- [ ] Update vật tư trong session
  - `supply_cost` tự động cập nhật
- [ ] Profit calculation:
  - Revenue từ payments
  - Supply cost từ inventory (auto)
  - Profit = revenue - supply_cost

---

## 📊 Tổng Kết Dependencies

### Giai Đoạn 1
- ✅ `dental_clinic_management` (đã có)
- ✅ `account` (Odoo core)
- ✅ `analytic` (Odoo core)
- ❌ `dental_inventory` (chưa có)

**Note**: Không phụ thuộc vào `base_accounting_kit`. Các tính năng cần thiết sẽ được implement trực tiếp trong `dental_accounting` bằng cách copy & adapt code từ `base_accounting_kit`.

### Giai Đoạn 2
- ✅ `dental_clinic_management` (đã có)
- ✅ `account` (Odoo core)
- ✅ `analytic` (Odoo core)
- ✅ `dental_inventory` (sẽ tạo sau)

---

## 🔗 Integration Points

### 1. Dental Treatment ↔ Payment Plan
- Treatment có `payment_plan_id`
- Payment Plan có `treatment_id`
- One-to-one relationship

### 2. Payment Plan ↔ Account Payment
- Payment Plan có `payment_ids` (One2many)
- Payment có `payment_plan_id` (Many2one)

### 3. Account Payment ↔ Account Move (Invoice)
- Payment tự động tạo Invoice
- Invoice link với Payment và Treatment

### 4. Treatment Session ↔ Supply Usage ↔ Inventory
- Session có `supply_ids`
- Supply Usage có `unit_cost` từ inventory
- Treatment `supply_cost` = sum of supply costs

### 5. Recurring Payments ↔ Profit Report
- Recurring payments (chi phí chung) → `other_costs` trong profit report
- Không link với treatment cụ thể

### 6. Follow-up ↔ Payment Plan
- Follow-up chỉ áp dụng cho treatments có `payment_plan_id.is_overdue = True`
- Timing: Sau 12 tháng từ `upfront_payment_date`

---

## 📝 Notes Quan Trọng

1. **Invoice Workflow**:
   - Invoice được tạo từ Payment (không phải từ Treatment)
   - Invoice = Proof of payment
   - Invoice hiển thị "Số tiền còn lại"

2. **Payment Plan**:
   - 12 tháng cố định
   - Đóng trước 50%
   - Số tiền linh hoạt (có thể skip)
   - Follow-up sau 12 tháng nếu còn nợ

3. **Supply Cost**:
   - Giai đoạn 1: Manual input
   - Giai đoạn 2: Auto từ inventory

4. **Follow-up**:
   - Chỉ áp dụng cho `installment` treatments
   - Timing: Sau 12 tháng từ ngày đóng 50%

5. **Profit Calculation**:
   - Revenue = Tổng payments
   - Cost = Supply cost + Other costs (recurring)
   - Profit = Revenue - Cost

---

## ✅ Checklist Hoàn Thành

### Giai Đoạn 1
- [ ] Module setup
- [ ] Extend dental.treatment
- [ ] Payment Plan model
- [ ] Extend account.payment
- [ ] Extend account.move (Invoice)
- [ ] Implement Follow-up (copy & adapt)
- [ ] Implement Recurring Payments (copy & adapt)
- [ ] Implement Lock Dates (copy & adapt)
- [ ] Profit report model
- [ ] Financial reports (copy & customize)
- [ ] Views
- [ ] Security
- [ ] Data
- [ ] Reports
- [ ] Testing

### Giai Đoạn 2
- [ ] Extend supply.usage
- [ ] Update dental.treatment (auto supply_cost)
- [ ] Integration với inventory
- [ ] Update views
- [ ] Testing

---

**Tài liệu này sẽ được cập nhật khi có thay đổi trong quá trình triển khai.**

