"""
File cấu hình toàn bộ hệ thống Sepsis Application
Chứa các thiết lập về màu sắc, font chữ, kích thước và các cấu hình chung
"""

# ==================== THÔNG TIN ỨNG DỤNG ====================
APP_NAME = "Sepsis Management System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Team Name"
APP_DESCRIPTION = "Hệ thống quản lý bệnh nhân Sepsis"

# ==================== CẤU HÌNH CỬA SỔ CHÍNH ====================
WINDOW_CONFIG = {
    "title": APP_NAME,
    "geometry": "1400x800",
    "resizable": True,
    "min_width": 1200,
    "min_height": 700,
}

# ==================== MÀU SẮC HỆ THỐNG ====================
COLORS = {
    # Màu chính
    "primary": "#66B7FF",           # Xanh dương chính
    "primary_dark": "#5aa3e0",      # Xanh dương đậm (hover)
    "primary_light": "#E3F2FD",     # Xanh dương nhạt (selected)
    
    # Màu nền
    "background": "#F7F7F5",        # Nền chính (xám nhạt)
    "background_white": "white",    # Nền trắng
    "transparent": "transparent",   # Trong suốt
    
    # Màu text
    "text_primary": "black",        # Text chính
    "text_secondary": "#757575",    # Text phụ (xám)
    "text_white": "white",          # Text trắng
    
    # Màu viền
    "border_primary": "black",      # Viền đen
    "border_gray": "#E0E0E0",       # Viền xám
    
    # Màu button
    "button_success": "#45a049",    # Xanh lá (hover/success)
    "button_warning": "#FFA726",    # Cam (warning/edit)
    "button_danger": "#E91E63",     # Đỏ hồng (danger/delete)
    "button_info": "#2196F3",       # Xanh info
    "button_error": "#FE5858",      # Đỏ lỗi
    
    # Màu khác
    "avatar_bg": "#E0E0E0",         # Nền avatar
    "scrollbar": "#66B7FF",         # Màu scrollbar
    "scrollbar_hover": "#5aa3e0",   # Màu scrollbar hover
}

# ==================== FONT CHỮ ====================
FONTS = {
    "family": "Roboto",             # Font chính
    "family_fallback": "Arial",     # Font dự phòng
    
    # Kích thước font
    "size_small": 11,
    "size_normal": 13,
    "size_medium": 14,
    "size_large": 16,
    "size_xlarge": 18,
    "size_title": 22,
    "size_header": 24,
    
    # Trọng lượng font
    "weight_normal": "normal",
    "weight_bold": "bold",
}

# ==================== KÍCH THƯỚC COMPONENTS ====================
SIZES = {
    # Button
    "button_width_small": 40,
    "button_width_normal": 180,
    "button_width_large": 200,
    "button_height_small": 35,
    "button_height_normal": 40,
    "button_height_large": 45,
    
    # Input fields
    "entry_height_small": 35,
    "entry_height_normal": 40,
    "textbox_height": 80,
    
    # Icon
    "icon_small": (20, 20),
    "icon_medium": (24, 24),
    "icon_large": (32, 32),
    
    # Avatar
    "avatar_width": 200,
    "avatar_height": 283,
    
    # Border
    "border_width_thin": 2,
    "border_width_medium": 3,
    "border_width_thick": 4,
    
    # Corner radius
    "corner_radius_small": 5,
    "corner_radius_normal": 10,
    "corner_radius_medium": 13,
    "corner_radius_large": 15,
    "corner_radius_xlarge": 17,
    
    # Padding
    "padding_small": 5,
    "padding_normal": 10,
    "padding_medium": 15,
    "padding_large": 20,
}

# ==================== CẤU HÌNH POPUP ====================
POPUP_CONFIG = {
    "patient_detail": {
        "width": 1000,
        "height": 700,
        "resizable": False,
        "title": "Chi tiết bệnh nhân",
    },
    "add_patient": {
        "width": 600,
        "height": 500,
        "resizable": False,
        "title": "Thêm bệnh nhân mới",
    },
    "edit_patient": {
        "width": 600,
        "height": 500,
        "resizable": False,
        "title": "Chỉnh sửa thông tin bệnh nhân",
    },
    "confirm_delete": {
        "width": 400,
        "height": 200,
        "resizable": False,
        "title": "Xác nhận xóa",
    },
    "warning": {
        "width": 400,
        "height": 150,
        "resizable": False,
        "title": "Cảnh báo",
    },
}

# ==================== CẤU HÌNH BẢNG BỆNH NHÂN ====================
TABLE_CONFIG = {
    "row_height": 40,
    "header_height": 45,
    
    # Độ rộng cột
    "column_widths": {
        "STT": 50,
        "ID": 80,
        "Họ và tên": 150,
        "Ngày sinh": 100,
        "Giới tính": 80,
        "SDT": 120,
        "Email": 180,
        "Tác vụ": 130,
    },
    
    # Style
    "header_bg": "#66B7FF",
    "header_fg": "white",
    "row_bg": "white",
    "row_fg": "black",
    "selected_bg": "#E3F2FD",
    "selected_fg": "black",
}

# ==================== CẤU HÌNH FORM BỆNH NHÂN ====================
PATIENT_FORM_CONFIG = {
    # Danh sách các trường thông tin bệnh nhân
    "fields": [
        {"key": "id_bệnh_nhân", "label": "ID bệnh nhân:", "type": "entry", "required": False, "readonly": True},
        {"key": "họ_và_tên", "label": "Họ và tên:", "type": "entry", "required": True, "readonly": False},
        {"key": "ngày_sinh", "label": "Ngày sinh:", "type": "entry", "required": True, "readonly": False},
        {"key": "giới_tính", "label": "Giới tính:", "type": "entry", "required": True, "readonly": False},
        {"key": "số_điện_thoại", "label": "Số điện thoại:", "type": "entry", "required": True, "readonly": False},
        {"key": "email", "label": "Email:", "type": "entry", "required": False, "readonly": False},
        {"key": "địa_chỉ", "label": "Địa chỉ:", "type": "entry", "required": False, "readonly": False},
        {"key": "chức_vụ", "label": "Chức vụ:", "type": "entry", "required": False, "readonly": False},
        {"key": "ngày_bắt_đầu_làm_việc", "label": "Ngày bắt đầu làm việc:", "type": "entry", "required": False, "readonly": False},
        {"key": "cân_nặng_(kg)", "label": "Cân nặng (kg):", "type": "entry", "required": False, "readonly": False},
        {"key": "tiểu_sử_bệnh_lý", "label": "Tiểu sử bệnh lý:", "type": "textbox", "required": False, "readonly": False},
        {"key": "tên_người_thân", "label": "Tên người thân:", "type": "entry", "required": False, "readonly": False},
        {"key": "số_điện_thoại_người_thân", "label": "Số điện thoại người thân:", "type": "entry", "required": False, "readonly": False},
        {"key": "quan_hệ_người_thân", "label": "Quan hệ người thân:", "type": "entry", "required": False, "readonly": False},
        {"key": "ghi_chú", "label": "Ghi chú:", "type": "textbox", "required": False, "readonly": False},
    ],
    
    # Label width
    "label_width": 200,
}

# ==================== CẤU HÌNH API ====================
API_CONFIG = {
    "base_url": "http://localhost:8000",  # URL backend API
    "timeout": 30,  # Timeout (giây)
    
    # Endpoints
    "endpoints": {
        "login": "/api/login",
        "logout": "/api/logout",
        "patients": "/api/patients",
        "patient_detail": "/api/patients/{id}",
        "predict": "/api/predict",
        "statistics": "/api/statistics",
    },
}

# ==================== CẤU HÌNH DATABASE ====================
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "sepsis_management",
    "user": "root",
    "password": "",
}

# ==================== CẤU HÌNH FILE ====================
FILE_CONFIG = {
    # Thư mục lưu trữ
    "upload_dir": "uploads",
    "avatar_dir": "uploads/avatars",
    "export_dir": "exports",
    "temp_dir": "temp",
    
    # File types cho phép
    "allowed_image_types": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "allowed_export_types": [".pdf", ".xlsx", ".csv"],
    
    # Giới hạn kích thước file
    "max_avatar_size_mb": 5,
    "max_export_size_mb": 10,
}

# ==================== CẤU HÌNH VALIDATION ====================
VALIDATION_CONFIG = {
    "phone_pattern": r"^0\d{9}$",  # Số điện thoại Việt Nam (10 số, bắt đầu bằng 0)
    "email_pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Email chuẩn
    "date_format": "%d/%m/%Y",  # Định dạng ngày tháng
    
    # Độ dài tối thiểu/tối đa
    "min_name_length": 2,
    "max_name_length": 100,
    "min_password_length": 6,
    "max_password_length": 50,
}

# ==================== CẤU HÌNH MESSAGES ====================
MESSAGES = {
    # Success messages
    "success_add": "✅ Thêm bệnh nhân thành công!",
    "success_update": "✅ Cập nhật thông tin thành công!",
    "success_delete": "✅ Xóa bệnh nhân thành công!",
    "success_export": "✅ Xuất file thành công!",
    "success_login": "✅ Đăng nhập thành công!",
    
    # Error messages
    "error_required_field": "❌ Vui lòng điền đầy đủ các trường bắt buộc!",
    "error_invalid_phone": "❌ Số điện thoại không hợp lệ! (10 số, bắt đầu bằng 0)",
    "error_invalid_email": "❌ Email không hợp lệ!",
    "error_invalid_date": "❌ Ngày tháng không hợp lệ! (dd/mm/yyyy)",
    "error_file_too_large": "❌ File quá lớn! (Tối đa {max_size}MB)",
    "error_invalid_file_type": "❌ Loại file không được hỗ trợ!",
    "error_network": "❌ Lỗi kết nối mạng! Vui lòng thử lại.",
    "error_server": "❌ Lỗi server! Vui lòng liên hệ quản trị viên.",
    "error_not_found": "❌ Không tìm thấy dữ liệu!",
    "error_permission": "❌ Bạn không có quyền thực hiện thao tác này!",
    
    # Warning messages
    "warning_no_selection": "⚠️ Vui lòng chọn bệnh nhân!",
    "warning_confirm_delete": "⚠️ Bạn có chắc chắn muốn xóa bệnh nhân này?",
    "warning_unsaved_changes": "⚠️ Có thay đổi chưa được lưu! Bạn có muốn tiếp tục?",
    
    # Info messages
    "info_loading": "⏳ Đang tải dữ liệu...",
    "info_processing": "⏳ Đang xử lý...",
    "info_exporting": "⏳ Đang xuất file...",
}

# ==================== CẤU HÌNH ICON/EMOJI ====================
ICONS = {
    "search": "🔍",
    "add": "+",
    "delete": "-",
    "edit": "✏️",
    "save": "💾",
    "export": "📄",
    "upload": "📤",
    "download": "📥",
    "back": "◀",
    "forward": "▶",
    "refresh": "🔄",
    "info": "📋",
    "warning": "⚠️",
    "error": "❌",
    "success": "✅",
    "user": "👤",
    "logout": "🚪",
    "settings": "⚙️",
    "home": "🏠",
    "patient": "🏥",
    "statistics": "📊",
    "ai": "🤖",
}

# ==================== CẤU HÌNH ANIMATION ====================
ANIMATION_CONFIG = {
    "enable": True,
    "duration_fast": 100,    # ms
    "duration_normal": 200,  # ms
    "duration_slow": 300,    # ms
    "easing": "ease-in-out",
}

# ==================== CẤU HÌNH LOG ====================
LOG_CONFIG = {
    "enable": True,
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    "file_path": "logs/app.log",
    "max_file_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# ==================== CẤU HÌNH THEME ====================
THEME_CONFIG = {
    "default_theme": "light",  # light, dark
    "appearance_mode": "System",  # System, Light, Dark
    "color_theme": "blue",  # blue, green, dark-blue
}

# ==================== HÀM HELPER LẤY CẤU HÌNH ====================

def get_color(key):
    """Lấy màu từ config"""
    return COLORS.get(key, "#000000")

def get_font(size="normal", weight="normal", family=None):
    """Tạo font từ config"""
    import customtkinter as ctk
    font_family = family or FONTS["family"]
    font_size = FONTS.get(f"size_{size}", FONTS["size_normal"])
    font_weight = FONTS.get(f"weight_{weight}", FONTS["weight_normal"])
    return ctk.CTkFont(family=font_family, size=font_size, weight=font_weight)

def get_size(key):
    """Lấy kích thước từ config"""
    return SIZES.get(key, 0)

def get_popup_config(popup_type):
    """Lấy cấu hình popup"""
    return POPUP_CONFIG.get(popup_type, {})

def get_message(key, **kwargs):
    """Lấy message và format với kwargs"""
    message = MESSAGES.get(key, "")
    if kwargs:
        return message.format(**kwargs)
    return message

def get_api_endpoint(endpoint_key, **kwargs):
    """Lấy API endpoint và format với kwargs"""
    endpoint = API_CONFIG["endpoints"].get(endpoint_key, "")
    if kwargs:
        return API_CONFIG["base_url"] + endpoint.format(**kwargs)
    return API_CONFIG["base_url"] + endpoint

# ==================== EXPORT ALL ====================
__all__ = [
    "APP_NAME", "APP_VERSION", "APP_AUTHOR", "APP_DESCRIPTION",
    "WINDOW_CONFIG", "COLORS", "FONTS", "SIZES", "POPUP_CONFIG",
    "TABLE_CONFIG", "PATIENT_FORM_CONFIG", "API_CONFIG", "DATABASE_CONFIG",
    "FILE_CONFIG", "VALIDATION_CONFIG", "MESSAGES", "ICONS",
    "ANIMATION_CONFIG", "LOG_CONFIG", "THEME_CONFIG",
    "get_color", "get_font", "get_size", "get_popup_config",
    "get_message", "get_api_endpoint"
]
