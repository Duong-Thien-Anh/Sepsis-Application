# Hệ thống Thông báo (Notification System)

## Tổng quan
Hệ thống thông báo được tách riêng theo mô hình MVC để dễ bảo trì và mở rộng.

## Cấu trúc File

### 1. **Notification_Controller.py** (Controller - Logic)
📍 Đường dẫn: `frontend/controllers/Notification_Controller.py`

**Chức năng:**
- Quản lý dữ liệu thông báo
- Xử lý logic nghiệp vụ (đọc/chưa đọc, lọc, xóa)
- Cung cấp API cho UI component

**Các phương thức chính:**
```python
# Getters
- get_all_notifications()          # Lấy tất cả thông báo
- get_recent_notifications(limit)  # Lấy N thông báo gần nhất
- get_filtered_notifications()     # Lấy thông báo theo filter
- get_unread_count()              # Đếm số thông báo chưa đọc
- get_notification_icon(type)     # Lấy icon theo loại
- get_notification_color(type)    # Lấy màu theo loại

# Setters
- set_filter(filter_type)          # Đặt filter ('all', 'unread', 'read')

# Actions
- mark_as_read(notification_id)    # Đánh dấu đã đọc
- mark_all_as_read()               # Đánh dấu tất cả đã đọc
- toggle_read_status(id)           # Chuyển đổi trạng thái đọc
- delete_notification(id)          # Xóa 1 thông báo
- delete_all_notifications()       # Xóa tất cả

# Validation
- has_notifications()              # Kiểm tra có thông báo không
- has_unread_notifications()       # Kiểm tra có chưa đọc không
```

---

### 2. **Notification_Component.py** (View - Giao diện)
📍 Đường dẫn: `frontend/gui/Components/Notification_Component.py`

**Chức năng:**
- Tạo button thông báo với badge
- Hiển thị dropdown menu (3 thông báo gần nhất)
- Tạo notification items trong dropdown
- Xử lý tương tác người dùng (click, hover)

**Các phương thức chính:**
```python
- create_notification_button(parent_frame)  # Tạo button thông báo
- toggle_dropdown(parent_frame)             # Toggle dropdown menu
- show_dropdown(parent_frame)               # Hiển thị dropdown
- create_dropdown_item(parent, notification) # Tạo item trong dropdown
- on_mark_all_read(dropdown)                # Xử lý đánh dấu tất cả
- show_full_popup()                         # Mở popup đầy đủ
```

**Tính năng đặc biệt:**
- **Single-click:** Toggle dropdown menu (350x400px)
- **Double-click:** Mở full notification popup (900x700px)
- **Badge đỏ:** Hiển thị số thông báo chưa đọc
- **Hover effect:** Đổi màu button khi hover

---

### 3. **Notification_Full_Popup.py** (View - Popup đầy đủ)
📍 Đường dẫn: `frontend/gui/Components/Notification_Full_Popup.py`

**Chức năng:**
- Hiển thị popup 900x700px với tất cả thông báo
- Filter thông báo (Tất cả / Chưa đọc / Đã đọc)
- Quản lý thông báo (đọc, xóa, xóa tất cả)

**Các phương thức chính:**
```python
- show()                              # Hiển thị popup
- create_header(parent)               # Tạo header
- create_filter_buttons(parent)       # Tạo nút filter
- create_notification_list(parent)    # Tạo danh sách
- display_notifications()             # Hiển thị thông báo
- create_notification_card(parent, notification) # Tạo card

# Event Handlers
- on_filter_change(filter_type)       # Xử lý thay đổi filter
- on_mark_all_read()                  # Đánh dấu tất cả đã đọc
- on_toggle_read(notification_id)     # Toggle trạng thái đọc
- on_delete(notification_id)          # Xóa thông báo
- on_delete_all()                     # Xóa tất cả
- refresh()                           # Làm mới UI
```

---

### 4. **Header_Component.py** (Integration)
📍 Đường dẫn: `frontend/gui/Components/Header_Component.py`

**Cách sử dụng:**
```python
from gui.Components.Notification_Component import NotificationUI

class HeaderFormUI(ctk.CTkFrame):
    def __init__(self, master, parent_component=None):
        super().__init__(master, fg_color="#F7F7F5")
        
        # Khởi tạo Notification UI Component
        self.notification_ui = NotificationUI(self)
    
    def create_notification_button(self, parent, count=0, command=None):
        """Tạo button thông báo."""
        return self.notification_ui.create_notification_button(parent)
```

---

## Luồng hoạt động

### 1. Khởi tạo
```
Header_Component.__init__()
    └─> NotificationUI(self)
          └─> NotificationController()
```

### 2. Hiển thị button
```
Header_Component.create_notification_button()
    └─> NotificationUI.create_notification_button()
          └─> NotificationController.get_unread_count()
```

### 3. Single-click (Dropdown)
```
User clicks button (1 click)
    └─> NotificationUI.toggle_dropdown()
          ├─> NotificationController.get_recent_notifications(3)
          └─> NotificationUI.show_dropdown()
                └─> NotificationUI.create_dropdown_item() × 3
```

### 4. Double-click (Full Popup)
```
User clicks button (2 clicks)
    └─> NotificationUI.show_full_popup()
          └─> NotificationFullPopup(controller).show()
                ├─> NotificationController.get_all_notifications()
                └─> display_notifications()
```

### 5. Đánh dấu đã đọc
```
User clicks "Đọc tất cả"
    └─> NotificationUI.on_mark_all_read()
          └─> NotificationController.mark_all_as_read()
```

### 6. Xóa thông báo
```
User clicks "Xóa"
    └─> NotificationFullPopup.on_delete(id)
          ├─> NotificationController.delete_notification(id)
          └─> refresh()
```

---

## Cấu trúc dữ liệu Notification

```python
notification = {
    'id': int,              # ID duy nhất
    'type': str,            # Loại: 'info', 'warning', 'reminder', 'system', 'urgent'
    'title': str,           # Tiêu đề
    'message': str,         # Nội dung
    'time': str,            # Thời gian (relative, ví dụ: "5 phút trước")
    'read': bool            # Trạng thái đọc
}
```

---

## Các loại thông báo

| Loại | Icon | Màu | Mô tả |
|------|------|-----|-------|
| `info` | ℹ️ | `#2196F3` (Xanh dương) | Thông tin chung |
| `warning` | ⚠️ | `#FF9800` (Cam) | Cảnh báo |
| `reminder` | 📅 | `#4CAF50` (Xanh lá) | Nhắc nhở |
| `system` | ⚙️ | `#9E9E9E` (Xám) | Thông báo hệ thống |
| `urgent` | 🚨 | `#F44336` (Đỏ) | Khẩn cấp |

---

## UI Specifications

### Button Thông báo
- **Kích thước:** 50x50px
- **Hình dạng:** Tròn (corner_radius=30)
- **Màu nền:** Trắng
- **Border:** 2px đen
- **Hover:** Đỏ (#FE5858)
- **Badge:** Đỏ, hiển thị số thông báo chưa đọc

### Dropdown Menu
- **Kích thước:** 350x400px
- **Vị trí:** Dưới button, bên trái
- **Nội dung:** 3 thông báo gần nhất
- **Header:** Xanh dương (#66B7FF)
- **Button:** "Đọc tất cả", "Xem tất cả"

### Full Popup
- **Kích thước:** 900x700px
- **Vị trí:** Center màn hình
- **Filter:** Tất cả / Chưa đọc / Đã đọc
- **Header:** Xanh dương (#66B7FF)
- **Actions:** Đọc tất cả, Xóa tất cả
- **Notification Card:**
  - Border màu theo loại thông báo
  - Background: Trắng (đã đọc) / #E3F2FD (chưa đọc)
  - Actions: "Đánh dấu đã đọc/chưa đọc", "Xóa"

---

## Tích hợp với Backend (TODO)

### API Endpoints cần tạo:
```python
GET    /api/notifications              # Lấy danh sách thông báo
GET    /api/notifications/unread       # Lấy thông báo chưa đọc
POST   /api/notifications/{id}/read    # Đánh dấu đã đọc
POST   /api/notifications/read-all     # Đánh dấu tất cả đã đọc
DELETE /api/notifications/{id}         # Xóa thông báo
DELETE /api/notifications/all          # Xóa tất cả
```

### WebSocket (Realtime):
```python
# Nhận thông báo mới realtime
ws://api/notifications/stream
```

### Cập nhật Controller:
```python
# Thay thế dữ liệu mẫu bằng API call
def get_all_notifications(self):
    response = requests.get('http://api/notifications')
    return response.json()
```

---

## Ưu điểm của kiến trúc này

✅ **Tách biệt rõ ràng:** View - Controller - Logic
✅ **Dễ bảo trì:** Thay đổi UI không ảnh hưởng logic
✅ **Dễ mở rộng:** Thêm loại thông báo mới dễ dàng
✅ **Tái sử dụng:** Controller có thể dùng cho nhiều UI
✅ **Dễ test:** Test logic độc lập với UI
✅ **Clean Code:** Mỗi file có trách nhiệm rõ ràng

---

## Hướng dẫn bảo trì

### Thêm loại thông báo mới:
1. Cập nhật `NotificationController.get_notification_icon()`
2. Cập nhật `NotificationController.get_notification_color()`
3. Không cần sửa UI!

### Thay đổi giao diện:
1. Chỉ sửa `Notification_Component.py` hoặc `Notification_Full_Popup.py`
2. Logic vẫn hoạt động bình thường

### Tích hợp API:
1. Sửa các method trong `NotificationController`
2. Thay dữ liệu mẫu bằng API call
3. UI tự động cập nhật

---

## Ví dụ sử dụng

### Thêm thông báo mới:
```python
# Trong controller
notification = {
    'id': 6,
    'type': 'info',
    'title': 'Thông báo mới',
    'message': 'Nội dung thông báo',
    'time': 'Vừa xong',
    'read': False
}
controller.notifications.insert(0, notification)
```

### Lấy số thông báo chưa đọc:
```python
unread_count = controller.get_unread_count()
print(f"Có {unread_count} thông báo chưa đọc")
```

### Filter thông báo:
```python
controller.set_filter('unread')
unread_notifications = controller.get_filtered_notifications()
```

---

## Liên hệ & Hỗ trợ

Nếu có thắc mắc hoặc cần hỗ trợ, vui lòng tạo issue trong repository.

**Version:** 1.0  
**Last Updated:** 2024-10-30  
**Author:** Sepsis Application Team
