# Dental Clinic Odoo Customization

## Modules
- **dental_crm**: Quản lý khách hàng và lịch hẹn nha khoa
- **dental_accounting**: Kế toán và thanh toán cho nha khoa  
- **dental_inventory**: Quản lý vật tư, thuốc, dụng cụ nha khoa

## Setup Instructions

### 1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/dental-clinic-odoo.git
cd dental-clinic-odoo
```

### 2. Cấu hình Odoo
Thêm đường dẫn vào `odoo.conf`:
```
addons_path = /path/to/odoo/addons,/path/to/dental-clinic-odoo/custom-addons
```

### 3. Restart Odoo
```bash
sudo systemctl restart odoo
# hoặc
~/odoo/odoo-bin -c odoo.conf
```

### 4. Activate modules
Vào Odoo → Apps → Update Apps List → Tìm và cài đặt module

## Git Workflow

### Tạo branch mới
```bash
git checkout -b feature/crm-appointment
```

### Commit changes
```bash
git add .
git commit -m "Add appointment booking feature"
```

### Push lên GitHub
```bash
git push origin feature/crm-appointment
```

### Tạo Pull Request trên GitHub để review
