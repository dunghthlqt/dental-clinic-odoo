# Dental Inventory Module - Kế Hoạch Triển Khai

## 📋 Tổng Quan

Module `dental_inventory` quản lý vật tư tiêu hao (consumables) cho phòng khám nha khoa, tích hợp với:
- **Odoo Stock**: Quản lý kho, tồn kho, stock moves
- **Odoo Purchase**: Quản lý đơn mua, nhà cung cấp
- **dental_clinic_management**: Sử dụng vật tư trong treatment sessions
- **dental_accounting**: Tính toán supply_cost tự động

**Odoo Version**: 17.0  
**Dependencies**: 
- `dental_clinic_management`
- `dental_accounting`
- `stock` (Odoo core)
- `purchase` (Odoo core)

---

## 🎯 Nguyên Tắc Thiết Kế

1. **Product Type**: Vật tư là `consumable` (tiêu hao), không phải `storable`
   - Có thể theo dõi tồn kho (on-hand quantity)
   - Không có inventory valuation (chỉ cần số lượng)
   - Có thể tracking theo lot

2. **Lot Tracking**:
   - Tracking theo lot (từ đơn mua)
   - Khi sử dụng: Tự động chọn lot (FIFO)
   - Không cần quản lý hạn sử dụng

3. **Cost Calculation**:
   - `unit_cost` lấy từ `purchase.order.line.price_unit` (giá mua thực tế)
   - Fallback về `product.standard_price` nếu chưa có PO
   - `total_cost = quantity * unit_cost`

4. **Purchase Workflow**: Đơn giản
   - Tạo PO trực tiếp → Receipt → Validate
   - Không cần RFQ workflow phức tạp

5. **Single Location**: Chỉ 1 kho trung tâm (không có kho con)

---

## 📦 Cấu Trúc Module

```
dental_inventory/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── dental_supply.py          # Extend product.product
│   ├── supply_category.py         # Phân loại vật tư
│   ├── supply_usage.py            # Extend supply.usage (từ dental_clinic_management)
│   ├── stock_move.py              # Extend stock.move
│   ├── stock_picking.py           # Extend stock.picking
│   └── purchase_order.py          # Extend purchase.order (nếu cần)
├── views/
│   ├── dental_supply_views.xml
│   ├── supply_category_views.xml
│   ├── supply_usage_views.xml
│   ├── stock_picking_views.xml
│   ├── purchase_order_views.xml
│   └── inventory_menu.xml
├── security/
│   ├── dental_inventory_security.xml
│   └── ir.model.access.csv
├── data/
│   ├── supply_categories.xml
│   └── default_warehouse.xml
└── reports/
    └── supply_usage_report.xml
```

---

## 🚀 GIAI ĐOẠN 1: Core Inventory Management

### 1. Module Setup

#### 1.1. Tạo Module Structure
- [ ] Tạo thư mục `dental_inventory/`
- [ ] Tạo `__init__.py` và `__manifest__.py`
- [ ] Tạo cấu trúc thư mục: `models/`, `views/`, `security/`, `data/`, `reports/`

#### 1.2. Manifest Configuration
```python
{
    'name': 'Dental Inventory',
    'version': '17.0.1.0.0',
    'category': 'Healthcare/Inventory',
    'summary': 'Inventory management for dental clinic supplies',
    'depends': [
        'base',
        'stock',
        'purchase',
        'dental_clinic_management',
        'dental_accounting',
    ],
    'data': [
        'security/dental_inventory_security.xml',
        'security/ir.model.access.csv',
        'data/supply_categories.xml',
        'data/default_warehouse.xml',
        'views/supply_category_views.xml',
        'views/dental_supply_views.xml',
        'views/supply_usage_views.xml',
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml',
        'views/inventory_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

---

### 2. Supply Category Model

#### 2.1. File: `models/supply_category.py`

**Mục đích**: Phân loại vật tư (hierarchical)

**Công việc**:
- [ ] Tạo model `dental.supply.category`:
  ```python
  _name = 'dental.supply.category'
  _description = 'Phân loại vật tư nha khoa'
  _parent_name = 'parent_id'
  _parent_store = True
  ```
- [ ] Fields:
  ```python
  name = fields.Char('Tên phân loại', required=True)
  code = fields.Char('Mã phân loại')
  parent_id = fields.Many2one('dental.supply.category', 'Phân loại cha')
  child_ids = fields.One2many('dental.supply.category', 'parent_id', 'Phân loại con')
  parent_path = fields.Char(index=True)
  ```
- [ ] Examples:
  - Vật liệu trám → Composite, Amalgam, GIC
  - Dụng cụ → Khoan, Kìm, Kẹp
  - Thuốc → Gây tê, Kháng sinh
  - Vật liệu niềng răng → Mắc cài, Dây cung

---

### 3. Extend Product Product (Dental Supply)

#### 3.1. File: `models/dental_supply.py`

**Mục đích**: Mở rộng `product.product` để quản lý vật tư nha khoa

**Công việc**:
- [ ] Inherit `product.product` model
- [ ] Thêm fields:
  ```python
  is_dental_supply = fields.Boolean(
      'Là vật tư nha khoa',
      default=False,
      help='Đánh dấu sản phẩm này là vật tư tiêu hao dùng trong điều trị'
  )
  
  supply_category_id = fields.Many2one(
      'dental.supply.category',
      string='Phân loại vật tư',
      help='Phân loại vật tư nha khoa'
  )
  
  min_stock_level = fields.Float(
      'Mức tồn kho tối thiểu',
      default=0.0,
      help='Cảnh báo khi tồn kho dưới mức này'
  )
  ```
- [ ] Override `default_get()`:
  - Nếu `is_dental_supply = True`:
    - `type = 'consu'` (consumable)
    - `tracking = 'lot'` (enable lot tracking)
- [ ] Domain cho views:
  - Filter chỉ hiển thị products có `is_dental_supply = True` trong supply-related views

---

### 4. Extend Supply Usage Model

#### 4.1. File: `models/supply_usage.py`

**Mục đích**: Mở rộng `supply.usage` (từ `dental_clinic_management`) để tích hợp với inventory

**Công việc**:
- [ ] Inherit `supply.usage` model
- [ ] Thêm fields:
  ```python
  product_id = fields.Many2one(
      'product.product',
      string='Vật tư',
      domain=[('is_dental_supply', '=', True)],
      help='Vật tư từ danh mục kho'
  )
  
  lot_id = fields.Many2one(
      'stock.lot',
      string='Lô',
      domain="[('product_id', '=', product_id)]",
      help='Lô vật tư (tự động chọn theo FIFO)'
  )
  
  unit_cost = fields.Float(
      'Đơn giá',
      compute='_compute_unit_cost',
      store=True,
      help='Giá mua vào của vật tư (từ PO hoặc standard_price)'
  )
  
  total_cost = fields.Float(
      'Tổng chi phí',
      compute='_compute_total_cost',
      store=True,
      help='Tổng chi phí = Số lượng × Đơn giá'
  )
  
  stock_move_id = fields.Many2one(
      'stock.move',
      string='Stock Move',
      readonly=True,
      help='Stock move được tạo khi sử dụng vật tư'
  )
  ```
- [ ] Computed methods:
  - `_compute_unit_cost()`:
    - Tìm `purchase.order.line` gần nhất có `product_id` và `price_unit`
    - Nếu không có → dùng `product.standard_price`
  - `_compute_total_cost()`: `quantity * unit_cost`
- [ ] `@api.onchange('product_id')`:
  - Khi chọn `product_id`:
    - Auto-fill `name` từ `product.name`
    - Auto-fill `supply_code` từ `product.default_code` (nếu có)
    - Auto-fill `unit_cost` từ computed method
- [ ] `@api.onchange('quantity')`:
  - Recompute `total_cost`
- [ ] Override `write()`:
  - Khi `session_id.status = 'completed'` và chưa có `stock_move_id`:
    - Tự động chọn lot (FIFO) nếu chưa có `lot_id`
    - Tạo `stock.move` (Outgoing) để trừ tồn kho
    - Link `stock_move_id` với `stock.move` vừa tạo
- [ ] Override `unlink()`:
  - Nếu có `stock_move_id` và chưa validate:
    - Hủy `stock.move`

---

### 5. Extend Stock Move

#### 5.1. File: `models/stock_move.py`

**Mục đích**: Link stock moves với supply usage và treatment sessions

**Công việc**:
- [ ] Inherit `stock.move` model
- [ ] Thêm fields:
  ```python
  supply_usage_id = fields.Many2one(
      'supply.usage',
      string='Supply Usage',
      help='Link với supply usage record'
  )
  
  treatment_session_id = fields.Many2one(
      'treatment.session',
      string='Treatment Session',
      related='supply_usage_id.session_id',
      store=True,
      help='Buổi điều trị sử dụng vật tư'
  )
  ```
- [ ] Override `_action_confirm()`:
  - Nếu có `supply_usage_id`:
    - Tự động chọn lot (FIFO) nếu chưa có `lot_id`
    - Validate stock move

---

### 6. Extend Stock Picking

#### 6.1. File: `models/stock_picking.py`

**Mục đích**: Mở rộng stock picking để hiển thị thông tin liên quan

**Công việc**:
- [ ] Inherit `stock.picking` model
- [ ] Thêm fields (cho Incoming):
  ```python
  supplier_id = fields.Many2one(
      'res.partner',
      string='Nhà cung cấp',
      domain=[('is_company', '=', True), ('supplier_rank', '>', 0)],
      help='Nhà cung cấp vật tư'
  )
  ```
- [ ] Computed fields:
  - `is_dental_supply_receipt`: True nếu tất cả products có `is_dental_supply = True`

---

### 7. Extend Purchase Order (Optional)

#### 7.1. File: `models/purchase_order.py`

**Mục đích**: Mở rộng PO để hiển thị thông tin dental supplies

**Công việc**:
- [ ] Inherit `purchase.order` model
- [ ] Computed fields:
  - `dental_supply_count`: Số lượng dental supplies trong PO
- [ ] Smart button: "Dental Supplies" (nếu có)

---

### 8. Views

#### 8.1. File: `views/supply_category_views.xml`

**Công việc**:
- [ ] Form view cho `dental.supply.category`:
  - `name`, `code`, `parent_id`
  - Tree view cho `child_ids`
- [ ] Tree view:
  - Columns: `name`, `code`, `parent_id`

#### 8.2. File: `views/dental_supply_views.xml`

**Công việc**:
- [ ] Extend form view của `product.product`:
  - Thêm tab "Dental Supply" (chỉ hiện khi `is_dental_supply = True`):
    - `is_dental_supply`
    - `supply_category_id`
    - `min_stock_level`
  - Thêm domain filter: `is_dental_supply = True` trong search view
- [ ] Tree view:
  - Thêm columns: `supply_category_id`, `min_stock_level`
- [ ] Kanban view (optional):
  - Cards hiển thị vật tư theo category

#### 8.3. File: `views/supply_usage_views.xml`

**Công việc**:
- [ ] Extend form view của `supply.usage` (từ `dental_clinic_management`):
  - Thay `supply_code` và `name` bằng `product_id` (Many2one)
  - Thêm `lot_id` (nếu cần hiển thị)
  - Thêm `unit_cost`, `total_cost` (readonly)
  - Thêm `stock_move_id` (readonly)
- [ ] Tree view:
  - Thay `supply_code`, `name` bằng `product_id`
  - Thêm `unit_cost`, `total_cost`

#### 8.4. File: `views/stock_picking_views.xml`

**Công việc**:
- [ ] Extend form view của `stock.picking`:
  - Thêm `supplier_id` (cho Incoming)
  - Smart button: "Dental Supplies" (nếu có)

#### 8.5. File: `views/purchase_order_views.xml`

**Công việc**:
- [ ] Extend form view của `purchase.order`:
  - Smart button: "Dental Supplies" (nếu có)

#### 8.6. File: `views/inventory_menu.xml`

**Công việc**:
- [ ] Tạo menu "Dental Inventory" trong Inventory app
- [ ] Sub-menus:
  - Supply Categories
  - Dental Supplies (Products filter: `is_dental_supply = True`)
  - Supply Usage Report

---

### 9. Security

#### 9.1. File: `security/dental_inventory_security.xml`

**Công việc**:
- [ ] Tạo security groups:
  - `group_dental_inventory_user`: Nhân viên kho
  - `group_dental_inventory_manager`: Quản lý kho
- [ ] Record rules:
  - User: Xem/sửa records của mình
  - Manager: Full access

#### 9.2. File: `security/ir.model.access.csv`

**Công việc**:
- [ ] Access rights cho:
  - `dental.supply.category`
  - Extend access cho `product.product`, `supply.usage`, `stock.move`, `stock.picking`

---

### 10. Data

#### 10.1. File: `data/supply_categories.xml`

**Công việc**:
- [ ] Default supply categories:
  - Vật liệu trám
  - Dụng cụ
  - Thuốc
  - Vật liệu niềng răng
  - Vật liệu phục hình

#### 10.2. File: `data/default_warehouse.xml`

**Công việc**:
- [ ] Tạo default warehouse (nếu chưa có)
- [ ] Tạo default location (kho chính)

---

### 11. Integration với Accounting

#### 11.1. File: `models/supply_usage.py` (update)

**Công việc**:
- [ ] Method `_get_unit_cost_from_po()`:
  - Tìm `purchase.order.line` gần nhất:
    - `product_id = self.product_id`
    - `order_id.state = 'purchase'` hoặc `'done'`
    - Order by `order_id.date_order desc`
  - Return `price_unit` từ PO line
  - Nếu không có → return `product.standard_price`

#### 11.2. Update `dental_accounting/models/supply_usage.py`

**Công việc**:
- [ ] Extend `supply.usage` trong `dental_accounting`:
  - Override `_compute_total_cost()` để sử dụng `unit_cost` từ inventory
  - Update `treatment._compute_supply_cost()` để tính từ `supply.usage.total_cost`

---

### 12. Testing Giai Đoạn 1

**Test Cases**:
- [ ] Tạo supply category → Tạo product với `is_dental_supply = True`
- [ ] Tạo Purchase Order → Receipt → Validate → Tồn kho được cập nhật
- [ ] Tạo Treatment Session → Chọn vật tư → Nhập số lượng
  - `unit_cost` tự động fill từ PO
  - `total_cost` tự động tính
- [ ] Complete Treatment Session → Stock move tự động tạo → Tồn kho trừ
- [ ] Kiểm tra `treatment.supply_cost` được cập nhật đúng

---

## 🔄 GIAI ĐOẠN 2: Advanced Features

### 1. Low Stock Alert

#### 1.1. File: `models/dental_supply.py` (update)

**Công việc**:
- [ ] Computed field:
  ```python
  is_low_stock = fields.Boolean(
      'Tồn kho thấp',
      compute='_compute_is_low_stock',
      help='True nếu tồn kho < min_stock_level'
  )
  ```
- [ ] Method `_compute_is_low_stock()`:
  - Lấy `stock.quant` cho product
  - So sánh với `min_stock_level`

#### 1.2. Cron Job

**Công việc**:
- [ ] Tạo cron job chạy hàng ngày:
  - Kiểm tra products có `is_low_stock = True`
  - Tạo activity/notification cho nhân viên kho

---

### 2. Supply Usage Report

#### 2.1. File: `models/supply_usage_report.py`

**Công việc**:
- [ ] Tạo transient model `dental.supply.usage.report`:
  - Date range filter
  - Group by: Product, Category, Treatment Type
  - Columns: Quantity used, Total cost

#### 2.2. File: `reports/supply_usage_report.xml`

**Công việc**:
- [ ] QWeb report template
- [ ] PDF layout

---

### 3. Stock Valuation Report (Optional)

**Công việc**:
- [ ] Dashboard hiển thị:
  - Tổng số lượng vật tư
  - Tổng giá trị (nếu cần)
  - Top 10 vật tư sử dụng nhiều nhất

---

## 📊 Tổng Kết Dependencies

### Giai Đoạn 1
- ✅ `dental_clinic_management` (đã có)
- ✅ `dental_accounting` (đã có)
- ✅ `stock` (Odoo core)
- ✅ `purchase` (Odoo core)

---

## 🔗 Integration Points

### 1. Product Product ↔ Supply Category
- Product có `supply_category_id`
- Category có `child_ids` (hierarchical)

### 2. Supply Usage ↔ Product Product
- `supply.usage` có `product_id`
- Auto-fill `unit_cost` từ PO hoặc `standard_price`

### 3. Supply Usage ↔ Stock Move
- `supply.usage` có `stock_move_id`
- `stock.move` có `supply_usage_id`
- Tự động tạo khi session completed

### 4. Supply Usage ↔ Treatment Session
- `supply.usage` có `session_id`
- `stock.move` có `treatment_session_id` (related)

### 5. Treatment ↔ Supply Cost
- `treatment.supply_cost` = sum(`session_ids.supply_ids.total_cost`)

### 6. Purchase Order ↔ Product Product
- PO line có `product_id`
- Lấy `price_unit` từ PO line để tính `unit_cost`

---

## 📝 Notes Quan Trọng

1. **Product Type**:
   - Vật tư là `consumable` (`type = 'consu'`)
   - Có thể tracking theo lot
   - Không có inventory valuation

2. **Lot Tracking**:
   - Tracking theo lot (từ đơn mua)
   - Tự động chọn lot (FIFO) khi sử dụng
   - Không cần quản lý hạn sử dụng

3. **Cost Calculation**:
   - `unit_cost` từ `purchase.order.line.price_unit`
   - Fallback về `product.standard_price`
   - `total_cost = quantity * unit_cost`

4. **Stock Movement**:
   - Tự động tạo `stock.move` khi session completed
   - Tự động trừ tồn kho
   - Tự động chọn lot (FIFO)

5. **Single Location**:
   - Chỉ 1 kho trung tâm
   - Không có kho con

---

## ✅ Checklist Hoàn Thành

### Giai Đoạn 1
- [ ] Module setup
- [ ] Supply Category model
- [ ] Extend product.product
- [ ] Extend supply.usage
- [ ] Extend stock.move
- [ ] Extend stock.picking
- [ ] Extend purchase.order (optional)
- [ ] Views
- [ ] Security
- [ ] Data
- [ ] Integration với Accounting
- [ ] Testing

### Giai Đoạn 2
- [ ] Low stock alert
- [ ] Supply usage report
- [ ] Stock valuation report (optional)

---

**Tài liệu này sẽ được cập nhật khi có thay đổi trong quá trình triển khai.**

