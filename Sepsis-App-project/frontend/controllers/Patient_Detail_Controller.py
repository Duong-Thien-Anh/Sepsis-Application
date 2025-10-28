from tkinter import filedialog
from PIL import Image
import os


class PatientDetailController:
    """Controller xử lý logic và sự kiện cho Patient Detail Component"""
    
    def __init__(self):
        """Khởi tạo controller"""
        self.avatar_image_path = None
        self.avatar_photo = None
        self.is_editing = False
    
    # ==================== AVATAR UPLOAD ====================
    
    def upload_avatar(self, avatar_label, on_success_callback=None, on_error_callback=None):
        """
        Xử lý tải ảnh đại diện từ máy tính
        
        Args:
            avatar_label: CTkLabel hiển thị ảnh
            on_success_callback: Callback(ctk_image, file_path) khi tải ảnh thành công
            on_error_callback: Callback(error_message) khi có lỗi
        
        Returns:
            tuple: (ctk_image, file_path) hoặc (None, None) nếu không chọn ảnh
        """
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return None, None
        
        try:
            # Mở và resize ảnh
            image = Image.open(file_path)
            
            # Tính toán kích thước mới giữ nguyên tỷ lệ
            avatar_width, avatar_height = 200, 283
            img_width, img_height = image.size
            
            # Tính tỷ lệ để fit vào khung
            ratio = min(avatar_width / img_width, avatar_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # Resize ảnh
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Lưu thông tin ảnh
            self.avatar_image_path = file_path
            
            print(f"📷 Đã tải ảnh: {os.path.basename(file_path)}")
            
            # Gọi callback nếu có
            if on_success_callback:
                on_success_callback(image, file_path)
            
            return image, file_path
            
        except Exception as e:
            error_msg = f"Không thể tải ảnh!\n{str(e)}"
            print(f"❌ Lỗi khi tải ảnh: {str(e)}")
            
            # Gọi callback lỗi nếu có
            if on_error_callback:
                on_error_callback(error_msg)
            
            return None, None
    
    # ==================== EDIT MODE ====================
    
    def toggle_edit_mode(self, entry_fields, edit_save_btn):
        """
        Chuyển đổi giữa chế độ xem và chế độ chỉnh sửa
        
        Args:
            entry_fields: Dictionary chứa các entry fields
            edit_save_btn: Nút Chỉnh sửa/Lưu
        
        Returns:
            bool: True nếu đang ở chế độ chỉnh sửa, False nếu đang ở chế độ xem
        """
        if not self.is_editing:
            # Chuyển sang chế độ chỉnh sửa
            self.is_editing = True
            
            # Mở khóa các trường
            self._unlock_fields(entry_fields)
            
            # Đổi nút thành "Lưu"
            edit_save_btn.configure(
                text="💾 Lưu",
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            
            print("✏️ Đã chuyển sang chế độ chỉnh sửa")
            return True
        else:
            # Lưu và khóa lại
            self.is_editing = False
            
            # Khóa lại các trường
            self._lock_fields(entry_fields)
            
            # Đổi nút về "Chỉnh sửa"
            edit_save_btn.configure(
                text="✏️ Chỉnh sửa",
                fg_color="#FFA726",
                hover_color="#FB8C00"
            )
            
            print("🔒 Đã khóa chế độ chỉnh sửa")
            return False
    
    def _unlock_fields(self, entry_fields):
        """Mở khóa tất cả các trường để chỉnh sửa"""
        from customtkinter import CTkTextbox
        
        for field_key, entry in entry_fields.items():
            if isinstance(entry, CTkTextbox):
                entry.configure(state="normal")
            else:
                entry.configure(state="normal")
    
    def _lock_fields(self, entry_fields):
        """Khóa tất cả các trường (read-only)"""
        from customtkinter import CTkTextbox
        
        for field_key, entry in entry_fields.items():
            if isinstance(entry, CTkTextbox):
                entry.configure(state="disabled")
            else:
                entry.configure(state="readonly")
    
    # ==================== SAVE CHANGES ====================
    
    def save_patient_data(self, entry_fields, patient_id=None, on_success_callback=None):
        """
        Lưu thông tin bệnh nhân
        
        Args:
            entry_fields: Dictionary chứa các entry fields
            patient_id: ID bệnh nhân (optional)
            on_success_callback: Callback(updated_data) khi lưu thành công
        
        Returns:
            dict: Dictionary chứa dữ liệu đã lưu
        """
        from customtkinter import CTkTextbox
        
        # Thu thập dữ liệu từ các fields
        updated_data = {}
        for field_key, entry in entry_fields.items():
            if isinstance(entry, CTkTextbox):
                value = entry.get("1.0", "end-1c")
            else:
                value = entry.get()
            updated_data[field_key] = value
        
        # Thêm avatar path nếu có
        if self.avatar_image_path:
            updated_data['avatar_path'] = self.avatar_image_path
        
        print(f"💾 Đã lưu thông tin bệnh nhân: {updated_data.get('họ_và_tên', 'N/A')}")
        print(f"📊 Dữ liệu: {updated_data}")
        
        # TODO: Gọi API hoặc database để lưu thay đổi
        # Example: self.api_client.update_patient(patient_id, updated_data)
        
        # Gọi callback nếu có
        if on_success_callback:
            on_success_callback(updated_data)
        
        return updated_data
    
    # ==================== EXPORT PDF ====================
    
    def export_to_pdf(self, patient_data, entry_fields=None, on_success_callback=None, on_error_callback=None):
        """
        Xuất thông tin bệnh nhân ra file PDF
        
        Args:
            patient_data: Dữ liệu bệnh nhân
            entry_fields: Dictionary chứa các entry fields (optional)
            on_success_callback: Callback(pdf_path) khi xuất thành công
            on_error_callback: Callback(error_message) khi có lỗi
        
        Returns:
            str: Đường dẫn file PDF hoặc None nếu có lỗi
        """
        try:
            patient_name = patient_data[2] if len(patient_data) > 2 else "Unknown"
            print(f"📄 Đang xuất PDF cho bệnh nhân: {patient_name}")
            
            # TODO: Implement chức năng xuất PDF
            # Example:
            # from reportlab.lib.pagesizes import letter
            # from reportlab.pdfgen import canvas
            # pdf_path = f"patient_{patient_id}.pdf"
            # c = canvas.Canvas(pdf_path, pagesize=letter)
            # ... add content ...
            # c.save()
            
            # Tạm thời trả về thông báo chưa implement
            if on_error_callback:
                on_error_callback("Chức năng xuất PDF đang được phát triển!")
            
            return None
            
        except Exception as e:
            error_msg = f"Lỗi khi xuất PDF: {str(e)}"
            print(f"❌ {error_msg}")
            
            if on_error_callback:
                on_error_callback(error_msg)
            
            return None
    
    # ==================== VALIDATION ====================
    
    def validate_patient_data(self, data):
        """
        Validate dữ liệu bệnh nhân trước khi lưu
        
        Args:
            data: Dictionary chứa dữ liệu bệnh nhân
        
        Returns:
            tuple: (is_valid, error_message)
        """
        errors = []
        
        # Kiểm tra họ tên
        if not data.get('họ_và_tên', '').strip():
            errors.append("Họ và tên không được để trống")
        
        # Kiểm tra ID
        if not data.get('id_bệnh_nhân', '').strip():
            errors.append("ID bệnh nhân không được để trống")
        
        # Kiểm tra số điện thoại
        phone = data.get('số_điện_thoại', '').strip()
        if phone and not phone.isdigit():
            errors.append("Số điện thoại chỉ được chứa chữ số")
        
        # Kiểm tra email
        email = data.get('email', '').strip()
        if email and '@' not in email:
            errors.append("Email không hợp lệ")
        
        if errors:
            return False, "\n".join(errors)
        
        return True, None
    
    # ==================== RESET ====================
    
    def reset_state(self):
        """Reset trạng thái controller về ban đầu"""
        self.avatar_image_path = None
        self.avatar_photo = None
        self.is_editing = False
        print("🔄 Đã reset trạng thái controller")
