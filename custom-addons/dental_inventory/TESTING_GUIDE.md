# Dental Inventory Module - Testing Guide (Phase 1)

## 📋 Tổng Quan

Tài liệu này hướng dẫn test các tính năng của module `dental_inventory` trong Phase 1: Core Inventory Management.

**Module**: `dental_inventory`  
**Version**: 17.0.1.0.0  
**Dependencies**: `dental_clinic_management`, `dental_accounting`, `stock`, `purchase`

---

## ✅ Test Cases

### Test Case 1: Module Installation và Setup

**Mục đích**: Kiểm tra module được cài đặt và cấu hình đúng

**Các bước**:
1. Vào **Apps** → Tìm "Dental Inventory"
2. Click **Install** (hoặc **Upgrade** nếu đã cài)
3. Kiểm tra:
   - [ ] Module được cài đặt thành công, không có lỗi
   - [ ] Menu "Dental Inventory" xuất hiện trong **Inventory** app
   - [ ] Sub-menus: "Phân loại vật tư", "Vật tư nha khoa" xuất hiện

**Kết quả mong đợi**: Module cài đặt thành công, menu và views hiển thị đúng

---

### Test Case 2: Tạo Supply Categories

**Mục đích**: Kiểm tra tính năng phân loại vật tư (hierarchical)

**Các bước**:
1. Vào **Inventory** → **Dental Inventory** → **Phân loại vật tư**
2. Kiểm tra các categories mặc định đã được tạo:
   - [ ] Vật liệu trám (với sub-categories: Composite, Amalgam, GIC)
   - [ ] Dụng cụ (với sub-categories: Khoan, Kìm, Kẹp)
   - [ ] Thuốc (với sub-categories: Gây tê, Kháng sinh)
   - [ ] Vật liệu niềng răng (với sub-categories: Mắc cài, Dây cung)
   - [ ] Vật liệu phục hình
3. Tạo category mới:
   - Click **Create**
   - Nhập: Tên = "Vật liệu tẩy trắng", Mã = "BLEACHING"
   - Click **Save**
4. Tạo sub-category:
   - Click **Create**
   - Nhập: Tên = "Gel tẩy trắng", Mã = "BLEACH_GEL"
   - Chọn Parent = "Vật liệu tẩy trắng"
   - Click **Save**

**Kết quả mong đợi**:
- [ ] Categories mặc định hiển thị đúng
- [ ] Có thể tạo category mới
- [ ] Có thể tạo sub-category (hierarchical)
- [ ] Tree view hiển thị đúng cấu trúc parent-child

---

### Test Case 3: Tạo Dental Supply (Product)

**Mục đích**: Kiểm tra tính năng tạo vật tư nha khoa

**Các bước**:
1. Vào **Inventory** → **Dental Inventory** → **Vật tư nha khoa**
2. Click **Create**
3. Nhập thông tin:
   - **Product Name**: "Composite A2"
   - **Quan trọng**: Check **"Là vật tư nha khoa"** (`is_dental_supply`) TRƯỚC khi điền các thông tin khác
   - Sau khi check, kiểm tra tự động:
     - **Product Type**: Tự động = "Storable" (để có thể track tồn kho)
   - **Phân loại vật tư**: Chọn "Composite" (Vật liệu trám → Composite)
   - **Mức tồn kho tối thiểu**: 10
   - **Cost**: 50000 (VND)
   - **Sales Price**: 0 (vì không bán ra)
4. Click **Save**
5. Kiểm tra:
   - [ ] Tab "Vật tư nha khoa" xuất hiện trong form view
   - [ ] `is_dental_supply = True`
   - [ ] `type = 'product'` (Storable - để track tồn kho)
   - [ ] `supply_category_id` = "Composite"
   - [ ] `min_stock_level = 10`

**Kết quả mong đợi**:
- [ ] Product được tạo thành công
- [ ] Tự động set `type = 'product'` (Storable) khi check `is_dental_supply` để có thể track tồn kho
- [ ] Tab "Vật tư nha khoa" hiển thị đúng fields
- [ ] Product xuất hiện trong filter "Vật tư nha khoa"

**Lưu ý**: Tạo thêm 2-3 products khác để test sau:
- "Gây tê Lidocaine" (Thuốc → Gây tê)
- "Mắc cài kim loại" (Vật liệu niềng răng → Mắc cài)

**Lưu ý quan trọng về Tracking**:
- Vật tư nha khoa **KHÔNG** sử dụng lot tracking, chỉ quản lý theo số lượng
- Nếu bạn nhận được cảnh báo yêu cầu nhập lot/serial number khi confirm PO:
  1. Vào **Inventory** → **Products** → Tìm product cần fix (ví dụ: "Composite A2")
  2. Mở product form → Tab **"Vật tư nha khoa"**
  3. Kiểm tra **"Tracking"** = "No Tracking" (nếu không, đổi thành "No Tracking")
  4. Click **Save**
  5. Thử lại confirm PO

Hoặc chạy script để fix tất cả products một lần:
- Xem file `scripts/fix_tracking_now.py` để biết cách sử dụng

---

### Test Case 4: Nhập kho (Purchase Order → Receipt)

**Mục đích**: Kiểm tra workflow nhập kho vật tư từ nhà cung cấp

**Các bước**:
1. **Tạo nhà cung cấp** (nếu chưa có):
   - Vào **Contacts** → **Create**
   - Chọn radio button **"Company"** (thay vì "Individual")
   - Nhập: Name = "Công ty Vật tư Nha khoa ABC"
   - Vào tab **"Sales & Purchase"**:
     - Check **"Is a Vendor"** (hoặc để trống, sẽ tự động set khi tạo PO)
   - Click **Save**

2. **Tạo Purchase Order**:
   - Vào **Purchase** → **Purchase Orders** → **Create**
   - **Vendor**: Chọn "Công ty Vật tư Nha khoa ABC"
   - **Order Lines**: 
     - **Quan trọng**: Phải thêm và lưu từng dòng sản phẩm trước khi confirm
     - Click vào dòng trống trong bảng **"Order Lines"** (hoặc icon **"Add a line"**)
     - Trong dòng vừa tạo:
       - **Product**: Chọn "Composite A2" (gõ tên hoặc chọn từ dropdown)
       - **Description**: Tự động fill = "Composite A2" (có thể giữ nguyên)
       - **Quantity**: Nhập 20
       - **Unit Price**: Nhập 50000
       - **Tax**: Để trống hoặc chọn thuế (nếu cần)
     - **Click ra ngoài dòng đó hoặc nhấn Tab** để lưu dòng
       - Dòng sẽ được lưu và hiển thị **"Total"** = 1,000,000 (20 × 50000)
     - Click vào dòng trống tiếp theo để thêm sản phẩm thứ 2:
       - **Product**: Chọn "Gây tê Lidocaine"
       - **Quantity**: Nhập 10
       - **Unit Price**: Nhập 30000
       - Click ra ngoài để lưu dòng
   - **Kiểm tra trước khi confirm**:
     - [ ] Có ít nhất 2 dòng trong Order Lines
     - [ ] Mỗi dòng có Product, Quantity, Unit Price đã điền
     - [ ] Tổng số tiền ở cuối form hiển thị đúng
   - Click **Save** (nút ở góc trên bên trái) để lưu PO trước khi confirm
   - **Quan trọng**: Nếu màn hình hiển thị "Yêu cầu báo giá" (RFQ) thay vì "Đơn mua hàng" (Purchase Order):
     - Click nút **"Xác nhận đơn hàng"** (Confirm Order) ở góc trên bên phải
     - Điều này sẽ chuyển RFQ thành Purchase Order
   - Sau khi confirm, màn hình sẽ chuyển sang trạng thái "Đơn mua hàng" (Purchase Order)
   - **Kiểm tra sau khi confirm**:
     - [ ] Order Lines vẫn hiển thị đầy đủ (không bị mất)
     - [ ] Số lượng và giá tiền vẫn đúng

3. **Receive Products**:
   - Trong PO, click **Receive Products**
   - Kiểm tra:
     - [ ] Receipt (Stock Picking) được tạo
     - [ ] Field "Nhà cung cấp" (`supplier_id`) tự động fill từ PO
     - [ ] Products và quantities đúng
   - Click **Validate** trên Receipt form
     - **Lưu ý**: Vật tư nha khoa không cần nhập lot/serial number, chỉ cần validate để nhập kho

4. **Kiểm tra tồn kho**:
   - Vào **Inventory** → **Products** → Tìm "Composite A2"
   - Click vào product → Kiểm tra:
     - [ ] **On Hand**: 20
     - [ ] **Available**: 20
     - [ ] Smart button **"On Hand"** hiển thị đúng quantity

**Kết quả mong đợi**:
- [ ] PO được tạo và confirm thành công
- [ ] Receipt được tạo tự động
- [ ] Validate receipt thành công
- [ ] Tồn kho được cập nhật đúng (20 cho Composite A2, 10 cho Gây tê)

---

### Test Case 5: Sử dụng vật tư trong Treatment Session

**Mục đích**: Kiểm tra tính năng sử dụng vật tư trong điều trị

**Các bước**:
1. **Tạo Treatment Session**:
   - Vào **Clinic Management** → **Hồ sơ điều trị** → Chọn hoặc tạo treatment
   - Vào tab **"Buổi điều trị"** → Click **Create**
   - Nhập: **Ngày thực hiện** = hôm nay
   - **Status** = "Đã lên lịch"

2. **Thêm vật tư sử dụng**:
   - Vào tab **"Vật tư sử dụng"**
   - Click **Add a line** (hoặc click vào dòng trống)
   - **Vật tư** (`product_id`): 
     - Click vào field "Vật tư" (sẽ hiện dropdown search)
     - **Quan trọng**: Gõ tên product (ví dụ: "Composite" hoặc "A2") để tìm kiếm
     - Nếu không thấy "Composite A2" trong kết quả tìm kiếm:
       - Có thể product chưa được set `is_dental_supply = True`
       - Vào **Inventory** → **Dental Inventory** → **Vật tư nha khoa** → Tìm "Composite A2"
       - Mở product form → Kiểm tra checkbox **"Là vật tư nha khoa"** đã được check chưa
       - Nếu chưa, check nó và click **Save**
       - Quay lại Treatment Session và thử search lại
     - Chọn "Composite A2" từ dropdown
   - Kiểm tra tự động fill:
     - [ ] **Tên vật tư** (`name`) tự động = "Composite A2"
     - [ ] **Mã vật tư** (`supply_code`) tự động = product code (nếu có)
     - [ ] **Đơn giá** (`unit_cost`) tự động = 50000 (từ PO line)
     - [ ] **Số lượng** (`quantity`) = 1 (default)
   - Nhập **Số lượng**: 2
   - Kiểm tra:
     - [ ] **Tổng chi phí** (`total_cost`) tự động = 2 × 50000 = 100000
   - Thêm vật tư thứ 2:
     - **Vật tư**: "Gây tê Lidocaine"
     - **Số lượng**: 1
     - Kiểm tra `unit_cost` = 30000, `total_cost` = 30000

3. **Complete Treatment Session**:
   - **Status**: Đổi thành "Đã hoàn thành"
   - Click **Save**
   - Kiểm tra:
     - [ ] Stock moves tự động được tạo
     - [ ] Tồn kho tự động trừ:
       - Composite A2: 20 - 2 = 18
       - Gây tê Lidocaine: 10 - 1 = 9

4. **Kiểm tra Stock Moves**:
   - Vào **Inventory** → **Operations** → **All Operations**
   - Tìm stock move có Origin = "Treatment Session: [ID]"
   - Kiểm tra:
     - [ ] Stock move có `supply_usage_id` link đúng
     - [ ] Stock move có `treatment_session_id` link đúng
     - [ ] Stock move đã được validate (state = "Done")
     - [ ] Quantity đúng (2 cho Composite A2, 1 cho Gây tê)

**Kết quả mong đợi**:
- [ ] Có thể chọn vật tư từ dropdown (chỉ hiện products có `is_dental_supply = True`)
- [ ] `unit_cost` tự động fill từ PO line (hoặc `standard_price`)
- [ ] `total_cost` tự động tính = `quantity × unit_cost`
- [ ] Khi session completed, stock moves tự động tạo
- [ ] Tồn kho tự động trừ đúng số lượng

---

### Test Case 6: Tự động tính Supply Cost trong Treatment

**Mục đích**: Kiểm tra tích hợp với Accounting - tự động tính `supply_cost`

**Các bước**:
1. **Kiểm tra Treatment có supply_cost**:
   - Vào **Clinic Management** → **Hồ sơ điều trị** → Chọn treatment đã có sessions với vật tư
   - Vào tab **"Kế toán"**
   - Kiểm tra:
     - [ ] **Chi phí vật tư** (`supply_cost`) tự động tính = tổng `supply.usage.total_cost`
     - [ ] Nếu có 2 sessions:
       - Session 1: Composite A2 (2 × 50000 = 100000) + Gây tê (1 × 30000 = 30000) = 130000
       - Session 2: Composite A2 (1 × 50000 = 50000) = 50000
       - **Tổng supply_cost** = 180000

2. **Tạo session mới với vật tư**:
   - Thêm session mới với vật tư
   - Complete session
   - Kiểm tra:
     - [ ] `supply_cost` tự động cập nhật (tăng thêm)

3. **Kiểm tra Profit**:
   - Trong tab **"Kế toán"**, kiểm tra:
     - [ ] **Lợi nhuận** (`profit`) = **Doanh thu** (`revenue`) - **Chi phí vật tư** (`supply_cost`)
     - Nếu chưa có thanh toán: `revenue = 0`, `profit = -supply_cost`

**Kết quả mong đợi**:
- [ ] `supply_cost` tự động tính từ tổng `supply.usage.total_cost` của tất cả sessions
- [ ] `supply_cost` tự động cập nhật khi thêm/xóa/sửa supply usage
- [ ] `profit` tự động tính = `revenue - supply_cost`

---

---

### Test Case 8: Low Stock Alert

**Mục đích**: Kiểm tra cảnh báo tồn kho thấp

**Các bước**:
1. **Set min_stock_level**:
   - Vào **Inventory** → **Dental Inventory** → **Vật tư nha khoa**
   - Chọn "Composite A2"
   - **Mức tồn kho tối thiểu**: 10
   - Click **Save**

2. **Kiểm tra khi tồn kho > min_stock_level**:
   - Nếu tồn kho = 20 (> 10):
     - [ ] **Tồn kho thấp** (`is_low_stock`) = False
     - [ ] Không có cảnh báo

3. **Kiểm tra khi tồn kho < min_stock_level**:
   - Sử dụng vật tư để giảm tồn kho xuống < 10
   - Refresh product form
   - Kiểm tra:
     - [ ] **Tồn kho thấp** (`is_low_stock`) = True
     - [ ] Có thể filter "Tồn kho thấp" trong search view

**Kết quả mong đợi**:
- [ ] `is_low_stock` tự động tính = True nếu `qty_available < min_stock_level`
- [ ] Filter "Tồn kho thấp" hoạt động đúng

---

### Test Case 9: Purchase Order Smart Button

**Mục đích**: Kiểm tra smart button "Vật tư nha khoa" trong PO

**Các bước**:
1. **Tạo PO với dental supplies**:
   - Tạo PO với "Composite A2" và "Gây tê Lidocaine"
   - Kiểm tra:
     - [ ] Smart button **"Vật tư nha khoa"** xuất hiện
     - [ ] Số lượng = 2 (2 dental supplies)

2. **Click smart button**:
   - Click **"Vật tư nha khoa"**
   - Kiểm tra:
     - [ ] Mở view chỉ hiển thị PO lines có `is_dental_supply = True`
     - [ ] Chỉ hiện "Composite A2" và "Gây tê Lidocaine"
     - [ ] Không hiện products khác (nếu có)

3. **PO không có dental supplies**:
   - Tạo PO chỉ với products thường (không phải dental supplies)
   - Kiểm tra:
     - [ ] Smart button **"Vật tư nha khoa"** không xuất hiện (hoặc hiện 0)

**Kết quả mong đợi**:
- [ ] Smart button chỉ hiện khi có dental supplies trong PO
- [ ] Click smart button mở view filtered đúng
- [ ] Số lượng hiển thị đúng

---

### Test Case 10: Stock Picking Smart Button

**Mục đích**: Kiểm tra smart button "Vật tư nha khoa" trong Stock Picking

**Các bước**:
1. **Tạo Receipt với dental supplies**:
   - Tạo PO với dental supplies → Receive Products
   - Kiểm tra:
     - [ ] Field **"Nhà cung cấp"** (`supplier_id`) tự động fill từ PO
     - [ ] Smart button **"Vật tư nha khoa"** xuất hiện (nếu có dental supplies)

2. **Click smart button**:
   - Click **"Vật tư nha khoa"**
   - Kiểm tra:
     - [ ] Mở view filtered chỉ hiển thị dental supplies

**Kết quả mong đợi**:
- [ ] `supplier_id` tự động fill từ PO
- [ ] Smart button hoạt động đúng

---

### Test Case 11: Xóa Supply Usage

**Mục đích**: Kiểm tra khi xóa supply usage, stock move được hủy đúng

**Các bước**:
1. **Tạo session với vật tư và complete**:
   - Tạo Treatment Session → Thêm vật tư → Complete
   - Kiểm tra stock move đã được tạo

2. **Xóa supply usage**:
   - Vào session → Tab "Vật tư sử dụng"
   - Xóa 1 supply usage
   - Kiểm tra:
     - [ ] Stock move liên kết được hủy (nếu chưa validate)
     - [ ] Tồn kho được restore (nếu stock move đã validate, cần tạo reverse move)

**Kết quả mong đợi**:
- [ ] Khi xóa supply usage, stock move được xử lý đúng
- [ ] Tồn kho được cập nhật đúng

---

### Test Case 12: Unit Cost từ Standard Price (Fallback)

**Mục đích**: Kiểm tra `unit_cost` fallback về `standard_price` nếu chưa có PO

**Các bước**:
1. **Tạo product chưa có PO**:
   - Tạo product "Test Supply" với `is_dental_supply = True`
   - **Cost**: 25000
   - Chưa tạo PO cho product này

2. **Sử dụng vật tư**:
   - Tạo Treatment Session → Thêm "Test Supply"
   - Kiểm tra:
     - [ ] **Đơn giá** (`unit_cost`) = 25000 (từ `standard_price`)
     - [ ] **Tổng chi phí** = `quantity × 25000`

3. **Tạo PO cho product**:
   - Tạo PO với "Test Supply", Unit Price: 30000
   - Receive và Validate

4. **Sử dụng lại vật tư**:
   - Tạo Treatment Session mới → Thêm "Test Supply"
   - Kiểm tra:
     - [ ] **Đơn giá** (`unit_cost`) = 30000 (từ PO line, không phải standard_price)

**Kết quả mong đợi**:
- [ ] Nếu chưa có PO: `unit_cost` = `standard_price`
- [ ] Nếu có PO: `unit_cost` = `purchase.order.line.price_unit` (PO gần nhất)

---

## 🐛 Common Issues và Troubleshooting

### Issue 1: Module không cài được
**Nguyên nhân**: Dependencies chưa được cài
**Giải pháp**: Cài đặt `dental_clinic_management` và `dental_accounting` trước

### Issue 2: Không thấy menu "Dental Inventory"
**Nguyên nhân**: Module chưa được upgrade hoặc cache
**Giải pháp**: 
- Upgrade module
- Clear cache: Developer mode → Clear cache
- Restart Odoo server

### Issue 3: `unit_cost` = 0 hoặc không tự động fill
**Nguyên nhân**: 
- Product chưa có `standard_price`
- Chưa có PO với product này
**Giải pháp**: 
- Set `standard_price` cho product
- Hoặc tạo PO với product này

### Issue 4: Stock move không tự động tạo khi complete session
**Nguyên nhân**: 
- Session chưa có `product_id` trong supply usage
- Warehouse chưa được cấu hình
**Giải pháp**: 
- Đảm bảo supply usage có `product_id` (không phải chỉ `name`)
- Cấu hình warehouse trong Inventory → Configuration → Warehouses

### Issue 5: `supply_cost` không tự động tính
**Nguyên nhân**: 
- Supply usage chưa có `total_cost`
- `total_cost` chưa được store
**Giải pháp**: 
- Đảm bảo supply usage có `product_id` và `quantity`
- Recompute: Developer mode → Technical → Database Structure → Models → `dental.treatment` → Recompute

### Issue 6: Không tìm thấy product khi search trong "Vật tư sử dụng"
**Nguyên nhân**: 
- Product chưa được set `is_dental_supply = True`
- Domain filter `[('is_dental_supply', '=', True)]` chỉ hiển thị products có `is_dental_supply = True`
**Giải pháp**: 
1. Vào **Inventory** → **Dental Inventory** → **Vật tư nha khoa**
2. Tìm product cần sử dụng (ví dụ: "Composite A2")
3. Mở product form → Kiểm tra checkbox **"Là vật tư nha khoa"** (`is_dental_supply`)
4. Nếu chưa check, check nó và click **Save**
5. Quay lại Treatment Session và thử search lại
6. Nếu vẫn không thấy, thử:
   - Refresh trang (F5)
   - Clear browser cache
   - Restart Odoo server

### Issue 7: Order Lines biến mất sau khi Confirm PO
**Nguyên nhân**: 
- Order lines chưa được lưu trước khi confirm
- Có thể do click Confirm quá nhanh trước khi Odoo lưu các thay đổi
**Giải pháp**: 
- **Quan trọng**: Sau khi thêm mỗi dòng sản phẩm, phải:
  1. Click ra ngoài dòng đó (hoặc nhấn Tab) để lưu dòng
  2. Đợi dòng được lưu (có thể thấy Total được tính tự động)
  3. Mới thêm dòng tiếp theo
- Click **Save** (nút ở góc trên bên trái) trước khi Confirm Order
- Kiểm tra lại Order Lines trước khi confirm:
  - Có ít nhất 1 dòng với Product đã chọn
  - Quantity và Unit Price đã điền
  - Total đã được tính
- Nếu order lines vẫn biến mất:
  - Refresh trang (F5)
  - Kiểm tra lại PO có ở trạng thái "Draft" hay "Purchase Order"
  - Nếu ở "Purchase Order" nhưng không có lines, có thể cần tạo lại PO

---

## 📊 Test Summary Checklist

Sau khi hoàn thành tất cả test cases, kiểm tra:

- [.] Module cài đặt thành công
- [.] Supply Categories hoạt động đúng (hierarchical)
- [.] Tạo Dental Supplies thành công
- [.] Nhập kho (PO → Receipt) hoạt động đúng
- [.] Sử dụng vật tư trong Treatment Session hoạt động đúng
- [.] Tự động trừ tồn kho khi complete session
- [.] Tự động tính `supply_cost` trong Treatment

- [ ] Low stock alert hoạt động đúng
- [ ] Smart buttons trong PO và Stock Picking hoạt động đúng
- [ ] Unit cost từ PO và fallback về standard_price hoạt động đúng
- [ ] Tích hợp với Accounting (`supply_cost` tự động tính)

---

## 📝 Notes

1. **Test Environment**: Nên test trên test database trước khi deploy production
2. **Data Backup**: Backup database trước khi test các tính năng xóa/sửa
3. **Developer Mode**: Bật Developer Mode để xem thêm thông tin debug
4. **Logs**: Kiểm tra Odoo logs nếu có lỗi: `tail -f /var/log/odoo/odoo.log`

---

**Tài liệu này sẽ được cập nhật khi có thay đổi trong module.**

