# Dental Inquiry Module

Module quản lý inquiry bệnh nhân nha khoa - Extend Odoo CRM để phù hợp với workflow nha khoa.

## Cài đặt

1. Đảm bảo module `dental_clinic_management` đã được cài đặt (optional nhưng khuyến nghị)
2. Update Apps List trong Odoo
3. Tìm và cài đặt module "Dental Patient Inquiry Management"

## Tính năng

- ✅ Capture inquiries từ phone, Facebook, website
- ✅ Schedule consultations
- ✅ Track follow-ups
- ✅ Convert inquiries to patients
- ✅ Integration với dental clinic module
- ✅ Calendar integration cho appointments

## Workflow

1. **Tạo Inquiry**: Receptionist tạo inquiry từ thông tin khách hàng
2. **Schedule Consultation**: Đặt lịch tư vấn
3. **Consultation**: Bác sĩ tư vấn và ghi chú
4. **Convert to Patient**: Chuyển đổi inquiry thành bệnh nhân
5. **Treatment**: Tự động tạo hồ sơ điều trị (nếu clinic module installed)

## Security Groups

- **Receptionist**: Tạo và quản lý inquiries
- **Dentist**: Tư vấn và convert inquiries
- **Manager**: Full access

## Dependencies

- `base`
- `crm`
- `calendar`
- `contacts`
- `mail`
- `dental_clinic_management` (optional, nhưng khuyến nghị)

## Notes

- Module này extend Odoo CRM, không tạo models mới
- Tương thích với Odoo 17.0
- Sử dụng inheritance pattern để tối ưu

