# Kế Hoạch Triển Khai Module Dental HR Management

## 📋 Tổng Quan

Module `dental_hr` quản lý nhân viên nha khoa, tích hợp với module HR gốc của Odoo và các module dental hiện có.

**Tên module**: `dental_hr`  
**Version**: 17.0.1.0.0  
**Category**: Human Resources/Dental

---

## 🎯 Mục Tiêu

1. Quản lý thông tin nhân viên nha khoa (bác sĩ, kỹ thuật viên, lễ tân, kế toán, quản lý kho)
2. Quản lý nghỉ phép (tích hợp `hr_holidays`)
3. Tính lương và thưởng linh hoạt
4. Tích hợp với `dental_accounting` để tạo bút toán kế toán
5. Hiển thị chi phí lương trong báo cáo lợi nhuận

---

## 📦 Dependencies

```python
'depends': [
    'base',
    'hr',                    # Module HR gốc của Odoo
    'hr_contract',            # Hợp đồng lao động
    'hr_holidays',           # Quản lý nghỉ phép
    'account',               # Kế toán (cho bút toán lương)
    'dental_accounting',     # Tích hợp báo cáo lợi nhuận
],
```

---

## 🏗️ Cấu Trúc Module

```
dental_hr/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── hr_employee.py              # Inherit hr.employee
│   ├── hr_contract.py               # Inherit hr.contract
│   ├── dental_salary.py            # Tính lương
│   ├── dental_bonus.py             # Thưởng
│   └── dental_salary_approval.py   # Workflow phê duyệt
├── views/
│   ├── hr_employee_views.xml       # Extend view nhân viên
│   ├── hr_contract_views.xml        # Extend view hợp đồng
│   ├── dental_salary_views.xml     # Views tính lương
│   ├── dental_bonus_views.xml      # Views thưởng
│   └── hr_menu.xml                 # Menu
├── security/
│   ├── dental_hr_security.xml      # Security groups
│   └── ir.model.access.csv         # Access rights
├── data/
│   ├── dental_role_data.xml         # Dữ liệu roles
│   ├── salary_journal_data.xml     # Journal cho lương
│   └── account_data.xml            # Tài khoản kế toán
└── static/
    └── description/
        └── icon.png
```

---

## 📝 Chi Tiết Công Việc

### Phase 1: Quản Lý Thông Tin Nhân Viên Cơ Bản

#### 1.1. Model: `dental.role`

**File**: `models/dental_role.py` (hoặc trong `hr_employee.py`)

**Mục đích**: Quản lý các vai trò trong nha khoa

**Fields**:
- `name`: Tên vai trò (Char, required)
  - Bác sĩ
  - Kỹ thuật viên
  - Lễ tân
  - Kế toán
  - Quản lý kho
- `code`: Mã vai trò (Char, required, unique)
  - `doctor`
  - `technician`
  - `receptionist`
  - `accountant`
  - `inventory_manager`
- `description`: Mô tả (Text)

**Views**:
- Tree view: Hiển thị danh sách roles
- Form view: Form tạo/sửa role

---

#### 1.2. Inherit Model: `hr.employee`

**File**: `models/hr_employee.py`

**Mục đích**: Mở rộng thông tin nhân viên với thông tin đặc thù nha khoa

**Fields thêm vào**:
```python
# Quản lý nhiều roles
dental_roles = fields.Many2many(
    'dental.role',
    'employee_role_rel',
    'employee_id',
    'role_id',
    string='Vai trò',
    help='Nhân viên có thể có nhiều vai trò (ví dụ: Kế toán kiêm Quản lý kho)'
)

# Thông tin chuyên môn (cho bác sĩ)
dental_specialty = fields.Selection([
    ('orthodontics', 'Niềng răng'),
    ('implant', 'Cấy ghép'),
    ('whitening', 'Tẩy trắng'),
    ('filling', 'Trám răng'),
    ('extraction', 'Nhổ răng'),
    ('general', 'Tổng quát'),
    ('other', 'Khác'),
], string='Chuyên khoa', help='Chuyên khoa của bác sĩ')

years_of_experience = fields.Integer(
    'Số năm kinh nghiệm',
    help='Số năm kinh nghiệm trong ngành nha khoa'
)

certifications = fields.Text(
    'Bằng cấp/Chứng chỉ',
    help='Bằng cấp và chứng chỉ của nhân viên'
)

# Computed fields
salary_count = fields.Integer(
    'Số lần tính lương',
    compute='_compute_salary_count'
)

def _compute_salary_count(self):
    """Tính số lần đã tính lương cho nhân viên"""
    for employee in self:
        employee.salary_count = self.env['dental.salary'].search_count([
            ('employee_id', '=', employee.id)
        ])
```

**Views**:
- Extend form view `hr.employee`:
  - Thêm tab "Thông tin Nha khoa" với các fields trên
  - Smart button "Lương" (nếu có `salary_count > 0`)

---

#### 1.3. Inherit Model: `hr.contract`

**File**: `models/hr_contract.py`

**Mục đích**: Mở rộng hợp đồng lao động (nếu cần thêm thông tin)

**Fields thêm vào** (nếu cần):
```python
# Có thể thêm các fields đặc thù nếu cần
# Hiện tại chỉ cần thông tin cơ bản từ hr.contract
```

**Views**:
- Extend form view `hr.contract` (nếu cần)

---

#### 1.4. Security Groups

**File**: `security/dental_hr_security.xml`

**Groups**:
```xml
<!-- Group: Quản lý nhân sự nha khoa -->
<record id="group_dental_hr_manager" model="res.groups">
    <field name="name">Quản lý nhân sự nha khoa</field>
    <field name="category_id" ref="module_category_dental_hr"/>
    <field name="implied_ids" eval="[(4, ref('hr.group_hr_manager'))]"/>
</record>
```

**Access Rights**:
- `dental.role`: Manager có full access
- `hr.employee`: Sử dụng quyền từ module HR gốc
- `hr.contract`: Sử dụng quyền từ module HR gốc

---

#### 1.5. Data: Roles

**File**: `data/dental_role_data.xml`

**Dữ liệu mặc định**:
- Bác sĩ (doctor)
- Kỹ thuật viên (technician)
- Lễ tân (receptionist)
- Kế toán (accountant)
- Quản lý kho (inventory_manager)

---

### Phase 2: Quản Lý Nghỉ Phép

#### 2.1. Tích Hợp `hr_holidays`

**Mục đích**: Sử dụng module `hr_holidays` gốc của Odoo

**Công việc**:
- Depend vào `hr_holidays` trong `__manifest__.py`
- Không cần tạo model mới
- Có thể extend views nếu cần thêm thông tin

**Views** (nếu cần):
- Extend form view `hr.leave` để thêm thông tin đặc thù (nếu có)

---

### Phase 3: Tính Lương Và Thưởng

#### 3.1. Model: `dental.bonus`

**File**: `models/dental_bonus.py`

**Mục đích**: Quản lý thưởng linh hoạt

**Fields**:
```python
name = fields.Char('Tên thưởng', required=True)

bonus_type = fields.Selection([
    ('individual', 'Thưởng cá nhân'),
    ('team', 'Thưởng tập thể'),
    ('holiday', 'Thưởng lễ'),
    ('month_13', 'Lương tháng 13'),
    ('other', 'Khác'),
], string='Loại thưởng', required=True, default='individual')

amount = fields.Float('Số tiền', required=True)

employee_ids = fields.Many2many(
    'hr.employee',
    'bonus_employee_rel',
    'bonus_id',
    'employee_id',
    string='Nhân viên',
    help='Chọn nhân viên được thưởng (để trống nếu là thưởng tập thể)'
)

date = fields.Date('Ngày áp dụng', required=True, default=fields.Date.today)

description = fields.Text('Mô tả')

state = fields.Selection([
    ('draft', 'Nháp'),
    ('confirmed', 'Đã xác nhận'),
], string='Trạng thái', default='draft', readonly=True)

# Computed fields
employee_count = fields.Integer(
    'Số nhân viên',
    compute='_compute_employee_count'
)

def _compute_employee_count(self):
    for bonus in self:
        bonus.employee_count = len(bonus.employee_ids)
```

**Methods**:
```python
def action_confirm(self):
    """Xác nhận thưởng"""
    self.write({'state': 'confirmed'})

def action_draft(self):
    """Quay lại nháp"""
    self.write({'state': 'draft'})
```

**Views**:
- Tree view: Danh sách thưởng
- Form view: Form tạo/sửa thưởng
- Search view: Tìm kiếm theo loại, nhân viên, ngày

---

#### 3.2. Model: `dental.salary`

**File**: `models/dental_salary.py`

**Mục đích**: Tính lương cho nhân viên

**Fields**:
```python
name = fields.Char('Tên', required=True, default=lambda self: _('Lương tháng %s/%s') % (fields.Date.today().month, fields.Date.today().year))

employee_id = fields.Many2one(
    'hr.employee',
    string='Nhân viên',
    required=True,
    ondelete='cascade'
)

month = fields.Date('Tháng/Năm', required=True, default=lambda self: fields.Date.today().replace(day=1))

# Lương cơ bản
base_salary = fields.Float(
    'Lương cơ bản',
    compute='_compute_base_salary',
    store=True,
    help='Lương cơ bản từ hợp đồng'
)

# Thưởng
bonus_ids = fields.Many2many(
    'dental.bonus',
    'salary_bonus_rel',
    'salary_id',
    'bonus_id',
    string='Thưởng',
    domain=[('state', '=', 'confirmed')],
    help='Các khoản thưởng trong tháng'
)

bonus_amount = fields.Float(
    'Tổng thưởng',
    compute='_compute_bonus_amount',
    store=True
)

# Tổng lương
total_salary = fields.Float(
    'Tổng lương',
    compute='_compute_total_salary',
    store=True,
    help='Tổng lương = Lương cơ bản + Tổng thưởng'
)

# Trạng thái
state = fields.Selection([
    ('draft', 'Nháp'),
    ('submitted', 'Đã gửi'),
    ('approved', 'Đã duyệt'),
    ('posted', 'Đã đăng'),
], string='Trạng thái', default='draft', readonly=True)

# Kế toán
account_move_id = fields.Many2one(
    'account.move',
    string='Bút toán kế toán',
    readonly=True,
    help='Bút toán kế toán được tạo tự động'
)

# Workflow
submitted_by = fields.Many2one('res.users', string='Người gửi', readonly=True)
submitted_date = fields.Datetime('Ngày gửi', readonly=True)
approved_by = fields.Many2one('res.users', string='Người duyệt', readonly=True)
approved_date = fields.Datetime('Ngày duyệt', readonly=True)
```

**Computed Methods**:
```python
@api.depends('employee_id', 'month')
def _compute_base_salary(self):
    """Tính lương cơ bản từ hợp đồng"""
    for salary in self:
        if salary.employee_id and salary.month:
            # Tìm hợp đồng có hiệu lực trong tháng
            contract = self.env['hr.contract'].search([
                ('employee_id', '=', salary.employee_id.id),
                ('state', '=', 'open'),
                ('date_start', '<=', salary.month),
                '|',
                ('date_end', '=', False),
                ('date_end', '>=', salary.month),
            ], limit=1)
            salary.base_salary = contract.wage if contract else 0.0
        else:
            salary.base_salary = 0.0

@api.depends('bonus_ids', 'bonus_ids.amount', 'bonus_ids.employee_ids')
def _compute_bonus_amount(self):
    """Tính tổng thưởng"""
    for salary in self:
        total = 0.0
        # Thưởng cá nhân
        individual_bonuses = salary.bonus_ids.filtered(
            lambda b: b.bonus_type == 'individual' and salary.employee_id in b.employee_ids
        )
        total += sum(individual_bonuses.mapped('amount'))
        
        # Thưởng tập thể
        team_bonuses = salary.bonus_ids.filtered(
            lambda b: b.bonus_type == 'team'
        )
        total += sum(team_bonuses.mapped('amount'))
        
        # Thưởng khác (lễ, tháng 13, ...)
        other_bonuses = salary.bonus_ids.filtered(
            lambda b: b.bonus_type in ['holiday', 'month_13', 'other']
        )
        total += sum(other_bonuses.mapped('amount'))
        
        salary.bonus_amount = total

@api.depends('base_salary', 'bonus_amount')
def _compute_total_salary(self):
    """Tính tổng lương"""
    for salary in self:
        salary.total_salary = salary.base_salary + salary.bonus_amount
```

**Workflow Methods**:
```python
def action_submit(self):
    """Gửi để duyệt (Accountant)"""
    self.write({
        'state': 'submitted',
        'submitted_by': self.env.user.id,
        'submitted_date': fields.Datetime.now(),
    })

def action_approve(self):
    """Duyệt (Manager)"""
    self.write({
        'state': 'approved',
        'approved_by': self.env.user.id,
        'approved_date': fields.Datetime.now(),
    })

def action_post(self):
    """Đăng bút toán kế toán"""
    if not self.account_move_id:
        # Tạo bút toán
        move = self._create_accounting_entry()
        self.write({
            'state': 'posted',
            'account_move_id': move.id,
        })
    else:
        raise UserError(_('Bút toán đã được tạo rồi!'))

def action_reset_to_draft(self):
    """Quay lại nháp"""
    if self.state == 'posted':
        raise UserError(_('Không thể quay lại nháp khi đã đăng bút toán!'))
    self.write({
        'state': 'draft',
        'submitted_by': False,
        'submitted_date': False,
        'approved_by': False,
        'approved_date': False,
    })
```

**Accounting Method**:
```python
def _create_accounting_entry(self):
    """Tạo bút toán kế toán cho lương"""
    # Tìm journal cho lương
    journal = self.env['account.journal'].search([
        ('code', '=', 'SAL'),
        ('type', '=', 'general'),
    ], limit=1)
    
    if not journal:
        raise UserError(_('Chưa tạo journal cho lương!'))
    
    # Tìm tài khoản "Chi phí nhân viên" (6411) - Tài khoản Nợ
    expense_account = self.env['account.account'].search([
        ('code', '=', '6411'),
    ], limit=1)
    
    if not expense_account:
        raise UserError(_('Chưa tạo tài khoản "Chi phí nhân viên" (6411)!'))
    
    # Tìm tài khoản "Phải trả công nhân viên" (3341) - Tài khoản Có
    payable_account = self.env['account.account'].search([
        ('code', '=', '3341'),
    ], limit=1)
    
    if not payable_account:
        raise UserError(_('Chưa tạo tài khoản "Phải trả công nhân viên" (3341)!'))
    
    # Tạo bút toán
    move = self.env['account.move'].create({
        'move_type': 'entry',
        'date': self.month,
        'journal_id': journal.id,
        'ref': _('Lương %s - %s') % (self.employee_id.name, self.month.strftime('%m/%Y')),
        'line_ids': [
            Command.create({
                'account_id': expense_account.id,
                'debit': self.total_salary,
                'credit': 0.0,
                'name': _('Chi phí lương %s') % self.employee_id.name,
            }),
            Command.create({
                'account_id': payable_account.id,
                'debit': 0.0,
                'credit': self.total_salary,
                'name': _('Phải trả lương %s') % self.employee_id.name,
            }),
        ],
    })
    
    return move
```

**Views**:
- Tree view: Danh sách lương
- Form view: Form tính lương với workflow buttons
- Search view: Tìm kiếm theo nhân viên, tháng, trạng thái

---

#### 3.3. Data: Journal và Tài Khoản

**File**: `data/salary_journal_data.xml`

**Journal cho lương**:
```xml
<record id="journal_salary" model="account.journal">
    <field name="name">Lương</field>
    <field name="code">SAL</field>
    <field name="type">general</field>
    <field name="company_id" ref="base.main_company"/>
</record>
```

**File**: `data/account_data.xml` (nếu cần tạo tài khoản)

**Note**: Tài khoản 6411 nên đã có sẵn trong chart of accounts. Nếu chưa có thì tạo.

---

#### 3.4. Security và Access Rights

**File**: `security/ir.model.access.csv`

**Access Rights**:
```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_dental_role_manager,dental.role.manager,dental_hr.model_dental_role,dental_hr.group_dental_hr_manager,1,1,1,1
access_dental_bonus_accountant,dental.bonus.accountant,dental_hr.model_dental_bonus,dental_accounting.group_dental_accountant,1,1,1,0
access_dental_bonus_manager,dental.bonus.manager,dental_hr.model_dental_bonus,dental_hr.group_dental_hr_manager,1,1,1,1
access_dental_salary_accountant,dental.salary.accountant,dental_hr.model_dental_salary,dental_accounting.group_dental_accountant,1,1,1,0
access_dental_salary_manager,dental.salary.manager,dental_hr.model_dental_salary,dental_hr.group_dental_hr_manager,1,1,1,1
```

**Record Rules** (nếu cần):
- Accountant chỉ xem/sửa lương của mình tạo
- Manager xem tất cả

---

### Phase 4: Tích Hợp Báo Cáo Lợi Nhuận

#### 4.1. Extend Model: `dental.profit.report`

**File**: `dental_accounting/models/profit_report.py` (extend)

**Fields thêm vào**:
```python
salary_cost = fields.Float(
    'Chi phí lương',
    compute='_compute_profit_data',
    help='Tổng chi phí lương trong tháng'
)
```

**Method update**:
```python
@api.depends('month')
def _compute_profit_data(self):
    # ... existing code ...
    
    # Tính chi phí lương từ dental_hr
    if 'dental.salary' in self.env:
        salaries = self.env['dental.salary'].search([
            ('month', '>=', month_start),
            ('month', '<=', month_end),
            ('state', '=', 'posted'),  # Chỉ tính lương đã đăng
        ])
        report.salary_cost = sum(salaries.mapped('total_salary'))
    else:
        report.salary_cost = 0.0
    
    # Tổng chi phí = Chi phí vật tư + Chi phí khác + Chi phí lương
    report.total_cost = report.supply_cost + report.other_costs + report.salary_cost
```

**Views update**:
- Thêm field `salary_cost` vào profit report view

---

#### 4.2. Update Dependencies

**File**: `dental_accounting/__manifest__.py`

**Dependencies**:
```python
'depends': [
    # ... existing dependencies ...
    'dental_hr',  # Thêm dependency (optional, chỉ khi cần)
],
```

**Note**: Có thể không cần depend trực tiếp, chỉ cần check `'dental.salary' in self.env` như trên.

---

### Phase 5: Menu và Navigation

#### 5.1. Menu Structure

**File**: `views/hr_menu.xml`

**Menu items**:
```xml
<!-- Menu trong HR app -->
<menuitem id="menu_dental_hr_root"
          name="Nha khoa"
          parent="hr.menu_hr_root"
          sequence="100"/>

<!-- Roles -->
<menuitem id="menu_dental_roles"
          name="Vai trò"
          parent="menu_dental_hr_root"
          action="action_dental_role"
          sequence="10"/>

<!-- Bonus -->
<menuitem id="menu_dental_bonus"
          name="Thưởng"
          parent="menu_dental_hr_root"
          action="action_dental_bonus"
          sequence="20"/>

<!-- Salary -->
<menuitem id="menu_dental_salary"
          name="Lương"
          parent="menu_dental_hr_root"
          action="action_dental_salary"
          sequence="30"/>
```

---

## 🔄 Workflow

### Workflow Tính Lương

1. **Accountant tạo lương** (state: `draft`)
   - Chọn nhân viên
   - Chọn tháng
   - Hệ thống tự động tính lương cơ bản từ hợp đồng
   - Chọn các khoản thưởng trong tháng
   - Hệ thống tự động tính tổng lương

2. **Accountant gửi để duyệt** (state: `submitted`)
   - Click button "Gửi để duyệt"
   - Lưu thông tin người gửi và thời gian

3. **Manager duyệt** (state: `approved`)
   - Click button "Duyệt"
   - Lưu thông tin người duyệt và thời gian

4. **Accountant đăng bút toán** (state: `posted`)
   - Click button "Đăng bút toán"
   - Hệ thống tự động tạo `account.move`
   - Link bút toán với lương

---

## 📊 Tóm Tắt Phase

| Phase | Mô Tả | Ưu Tiên |
|-------|-------|---------|
| Phase 1 | Quản lý thông tin nhân viên cơ bản | Cao |
| Phase 2 | Quản lý nghỉ phép (tích hợp hr_holidays) | Trung bình |
| Phase 3 | Tính lương và thưởng | Cao |
| Phase 4 | Tích hợp báo cáo lợi nhuận | Trung bình |
| Phase 5 | Menu và navigation | Thấp |

---

## ⚠️ Lưu Ý

1. **Tài khoản kế toán**: 
   - Nợ: 6411 (Chi phí nhân viên)
   - Có: 3341 (Phải trả công nhân viên)

2. **Dependencies**:
   - `dental_accounting` không cần depend vào `dental_hr` (optional dependency)
   - Chỉ cần check `'dental.salary' in self.env` khi tính chi phí lương

3. **Workflow**:
   - Accountant tạo và gửi
   - Manager duyệt
   - Accountant đăng bút toán

4. **Testing**:
   - Test workflow tính lương
   - Test tạo bút toán kế toán
   - Test hiển thị chi phí lương trong báo cáo lợi nhuận

---

## 🚀 Bắt Đầu Triển Khai

Bắt đầu từ **Phase 1** → **Phase 3** → **Phase 2** → **Phase 4** → **Phase 5**

---

**Chúc bạn triển khai thành công! 🎉**

