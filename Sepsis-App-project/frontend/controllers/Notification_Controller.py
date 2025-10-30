"""
Controller xử lý logic cho hệ thống thông báo.
"""

class NotificationController:
    """Controller quản lý logic thông báo."""
    
    def __init__(self):
        """Khởi tạo controller với dữ liệu mẫu."""
        # Dữ liệu thông báo mẫu (sau này sẽ lấy từ API/Database)
        self.notifications = [
            {
                'id': 1,
                'type': 'info',
                'title': 'Cập nhật hệ thống',
                'message': 'Phiên bản 2.0 đã được cập nhật với nhiều tính năng mới',
                'time': '5 phút trước',
                'read': False
            },
            {
                'id': 2,
                'type': 'warning',
                'title': 'Cảnh báo bệnh nhân',
                'message': 'Bệnh nhân #BS123 có dấu hiệu nhiễm trùng huyết nghiêm trọng',
                'time': '10 phút trước',
                'read': False
            },
            {
                'id': 3,
                'type': 'reminder',
                'title': 'Nhắc nhở khám định kỳ',
                'message': 'Có 3 bệnh nhân cần được khám định kỳ trong ngày hôm nay',
                'time': '1 giờ trước',
                'read': True
            },
            {
                'id': 4,
                'type': 'system',
                'title': 'Sao lưu dữ liệu',
                'message': 'Quá trình sao lưu dữ liệu tự động đã hoàn tất thành công',
                'time': '2 giờ trước',
                'read': True
            },
            {
                'id': 5,
                'type': 'urgent',
                'title': '🚨 KHẨN CẤP',
                'message': 'Bệnh nhân #BS456 cần can thiệp y tế khẩn cấp ngay lập tức!',
                'time': '3 giờ trước',
                'read': False
            }
        ]
        
        # Filter hiện tại
        self.current_filter = 'all'  # all, unread, read
    
    # ==================== GETTERS ====================
    
    def get_all_notifications(self):
        """Lấy tất cả thông báo."""
        return self.notifications
    
    def get_recent_notifications(self, limit=3):
        """
        Lấy các thông báo gần nhất.
        
        Args:
            limit: Số lượng thông báo cần lấy (mặc định 3)
            
        Returns:
            Danh sách thông báo
        """
        return self.notifications[:limit]
    
    def get_filtered_notifications(self):
        """
        Lấy thông báo theo filter hiện tại.
        
        Returns:
            Danh sách thông báo đã lọc
        """
        if self.current_filter == 'unread':
            return [n for n in self.notifications if not n['read']]
        elif self.current_filter == 'read':
            return [n for n in self.notifications if n['read']]
        else:  # 'all'
            return self.notifications
    
    def get_unread_count(self):
        """
        Đếm số thông báo chưa đọc.
        
        Returns:
            Số lượng thông báo chưa đọc
        """
        return sum(1 for n in self.notifications if not n['read'])
    
    def get_notification_icon(self, notification_type):
        """
        Lấy icon cho loại thông báo.
        
        Args:
            notification_type: Loại thông báo (info, warning, reminder, system, urgent)
            
        Returns:
            Emoji icon
        """
        icons = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'reminder': '📅',
            'system': '⚙️',
            'urgent': '🚨'
        }
        return icons.get(notification_type, 'ℹ️')
    
    def get_notification_color(self, notification_type):
        """
        Lấy màu cho loại thông báo.
        
        Args:
            notification_type: Loại thông báo
            
        Returns:
            Mã màu hex
        """
        colors = {
            'info': '#2196F3',
            'warning': '#FF9800',
            'reminder': '#4CAF50',
            'system': '#9E9E9E',
            'urgent': '#F44336'
        }
        return colors.get(notification_type, '#2196F3')
    
    # ==================== SETTERS ====================
    
    def set_filter(self, filter_type):
        """
        Đặt filter cho thông báo.
        
        Args:
            filter_type: Loại filter ('all', 'unread', 'read')
        """
        if filter_type in ['all', 'unread', 'read']:
            self.current_filter = filter_type
    
    def get_current_filter(self):
        """Lấy filter hiện tại."""
        return self.current_filter
    
    # ==================== ACTIONS ====================
    
    def mark_as_read(self, notification_id):
        """
        Đánh dấu thông báo đã đọc.
        
        Args:
            notification_id: ID của thông báo
            
        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['read'] = True
                return True
        return False
    
    def mark_all_as_read(self):
        """Đánh dấu tất cả thông báo đã đọc."""
        for notif in self.notifications:
            notif['read'] = True
    
    def toggle_read_status(self, notification_id):
        """
        Chuyển đổi trạng thái đọc của thông báo.
        
        Args:
            notification_id: ID của thông báo
            
        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        for notif in self.notifications:
            if notif['id'] == notification_id:
                notif['read'] = not notif['read']
                return True
        return False
    
    def delete_notification(self, notification_id):
        """
        Xóa một thông báo.
        
        Args:
            notification_id: ID của thông báo
            
        Returns:
            True nếu thành công, False nếu không tìm thấy
        """
        for i, notif in enumerate(self.notifications):
            if notif['id'] == notification_id:
                self.notifications.pop(i)
                return True
        return False
    
    def delete_all_notifications(self):
        """Xóa tất cả thông báo."""
        self.notifications.clear()
    
    # ==================== VALIDATION ====================
    
    def has_notifications(self):
        """
        Kiểm tra có thông báo nào không.
        
        Returns:
            True nếu có thông báo, False nếu không
        """
        return len(self.notifications) > 0
    
    def has_unread_notifications(self):
        """
        Kiểm tra có thông báo chưa đọc không.
        
        Returns:
            True nếu có thông báo chưa đọc, False nếu không
        """
        return any(not n['read'] for n in self.notifications)
