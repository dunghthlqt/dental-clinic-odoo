# Giải thích về Contact trong Inquiry

## Câu hỏi: Khi tạo inquiry mới, có bắt buộc phải tạo contact mới không?

**Trả lời: KHÔNG bắt buộc!** Bạn có 3 lựa chọn:

### 1. Tạo Inquiry KHÔNG có Contact (Khuyến nghị cho inquiry mới)
- **Khi nào dùng**: Khi khách hàng lần đầu liên hệ, chưa có trong hệ thống
- **Cách làm**: 
  - Để trống trường "Tổ chức/Liên hệ" (partner_id)
  - Chỉ điền tên vào trường "Thông tin" (name field)
  - Điền thông tin liên hệ: Email, Điện thoại, Facebook
- **Lợi ích**: 
  - Không tạo contact thừa trong hệ thống
  - Khi chuyển đổi thành bệnh nhân, hệ thống sẽ tự động tạo contact mới

### 2. Chọn Contact đã tồn tại
- **Khi nào dùng**: Khi khách hàng đã từng liên hệ trước đó
- **Cách làm**: 
  - Gõ tên vào trường "Tổ chức/Liên hệ"
  - Chọn từ danh sách gợi ý (autocomplete)
- **Lợi ích**: 
  - Liên kết inquiry với contact đã có
  - Xem lịch sử liên hệ trước đó

### 3. Tạo Contact mới ngay khi tạo Inquiry
- **Khi nào dùng**: Khi bạn chắc chắn muốn tạo contact ngay
- **Cách làm**: 
  - Click vào biểu tượng "+" bên cạnh trường "Tổ chức/Liên hệ"
  - Tạo contact mới
  - Chọn contact vừa tạo
- **Lưu ý**: Có thể tạo nhiều contact trùng lặp nếu không cẩn thận

## Khuyến nghị

**Cho inquiry mới**: Để trống trường "Tổ chức/Liên hệ", chỉ điền thông tin cơ bản. Khi chuyển đổi thành bệnh nhân, hệ thống sẽ tự động tạo contact mới từ thông tin inquiry.

## Cách hoạt động của Autocomplete

Khi bạn gõ tên vào trường "Tổ chức/Liên hệ", Odoo sẽ:
1. Tìm kiếm trong danh sách `res.partner` (Contacts)
2. Hiển thị danh sách gợi ý dựa trên:
   - Tên (name)
   - Email
   - Số điện thoại
3. Bạn có thể chọn từ danh sách hoặc tiếp tục gõ để tạo mới

**Lưu ý**: Autocomplete chỉ hiển thị, không bắt buộc phải chọn. Bạn có thể bỏ qua và để trống.

