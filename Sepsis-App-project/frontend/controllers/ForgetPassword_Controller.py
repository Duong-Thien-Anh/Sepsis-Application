import customtkinter as ctk
import re
from services.api.config import load_environment, API_URL, TIMEOUT

class ForgetPasswordController:
    def __init__(self):
        load_environment()
        self.api_url = API_URL
        self.timeout = TIMEOUT

        

        self.email_entry = None
        self.error_label = None
        self.underline_frame = None
        self.send_button = None
        self.code_entries = []
        self.backSG_label = None

        # Các widget sẽ được gán sau
    def bind_widgets(self, email_entry=None, error_label=None, underline_frame=None, send_button=None):
        if email_entry is not None:
            self.email_entry = email_entry
        if error_label is not None:
            self.error_label = error_label
        if underline_frame is not None:
            self.underline_frame = underline_frame
        if send_button is not None:
            self.send_button = send_button

    # ========== VALIDATE EMAIL ==========
    def validate_email_format(self, email: str) -> bool:
        GMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        return re.fullmatch(GMAIL_REGEX, email) is not None

    # ========== CHECK EMAIL ==========
    def check_email(self, entry, error_label, min_length=5, max_length=30):
        text = entry.get()

        if text == "" or text == "Nhập email":
            error_label.configure(text="Vui lòng nhập email.", text_color="red")
            return False

        if len(text) > max_length:
            error_label.configure(text=f"Email không được vượt quá {max_length} ký tự.", text_color="red")
            return False

        if len(text) < min_length:
            error_label.configure(text=f"Email phải có ít nhất {min_length} ký tự.", text_color="red")
            return False

        if not self.validate_email_format(text):
            error_label.configure(text="Email không hợp lệ, chỉ chấp nhận @gmail.com", text_color="red")
            return False

        error_label.configure(text="")
        return True

    # ========== SET UP EMAIL ==========
    def setup_email_entry(self, entry, error_label, placeholder="Nhập email"):
        self.email_entry =entry
        def on_validate(new_value):
            if new_value == "" or new_value == placeholder:
                return True
            if len(new_value) > 30:
                return False
            return True

        vcmd = (entry.register(on_validate), "%P")
        entry.configure(validate="key", validatecommand=vcmd)

        entry.insert(0, placeholder)
        entry.configure(fg_color="white", text_color="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, ctk.END)
                entry.configure(text_color="black")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(text_color="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ========== CHECK OTP FOR BUTTON SEND CODE ==========
    def on_send_code(self, parent):
        if self.check_email(self.email_entry, self.error_label):
            print("✅ Email hợp lệ → tiếp tục gửi mã")
            # TODO: gọi API gửi mã OTP tại đây
            self.switch_to_code_input(parent)
        else:
            print("⚠️ Email không hợp lệ → dừng lại")

    # ========== SWITCH UI ==========
    def switch_to_code_input(self, parent):
        """Ẩn input + button cũ → Hiện 4 ô code + button xác nhận"""
        self.email_entry.destroy()
        self.send_button.destroy()
        self.error_label.destroy()
        self.underline_frame.destroy()
        

        title_label = ctk.CTkLabel(
            parent,
            text="Vui lòng nhập mã xác nhận !",
            font=("Arial", 20, "bold"),
            text_color="#66B7FF",
        )
        title_label.pack(pady=(25, 0))

        # ---- 4 ô nhập code ----
        code_frame = ctk.CTkFrame(parent, fg_color="#FFFFFF")
        code_frame.pack(pady=(20, 10))

        self.code_entries = []

        def on_key_release(event, idx):
            value = event.widget.get()

            # Xử lý phím Backspace
            if event.keysym == "BackSpace":
                if value == "" and idx > 0:
                    prev_entry = self.code_entries[idx - 1]
                    prev_entry.delete(0, ctk.END)
                    prev_entry.focus()
                return

            # Nếu paste nhiều ký tự
            if len(value) > 1:
                first_char = value[0]
                event.widget.delete(0, ctk.END)
                event.widget.insert(0, first_char)

                remaining = value[1:]
                next_idx = idx + 1
                while remaining and next_idx < len(self.code_entries):
                    next_entry = self.code_entries[next_idx]
                    if next_entry.get() == "":
                        next_entry.insert(0, remaining[0])
                        remaining = remaining[1:]
                    next_idx += 1

            elif len(value) == 1 and idx < len(self.code_entries) - 1:
                # Nhập 1 ký tự thì nhảy sang ô tiếp theo
                self.code_entries[idx + 1].focus()

        for i in range(4):
            entry = ctk.CTkEntry(
                code_frame,
                width=50,
                height=50,
                justify="center",
                font=("Arial", 18, "bold"),
            )
            entry.grid(row=0, column=i, padx=5)
            entry.bind("<KeyRelease>", lambda e, idx=i: on_key_release(e, idx))
            self.code_entries.append(entry)

        # ---- Button xác nhận ----
        confirm_btn = ctk.CTkButton(
            parent,
            text="Xác nhận",
            fg_color="#66B7FF",
            hover_color="#45a049",
            text_color="white",
            command=self.on_confirm_code,
            corner_radius=8,
            border_color="#000000",
            border_width=1,
            font=("Arial", 14, "bold"),
            width=100,
            height=45
        )
        confirm_btn.pack(pady=20)

    # ========= HANDLE CONFIRM =========
    def on_confirm_code(self):
        code = "".join([e.get() for e in self.code_entries])
        if len(code) == 4 and code.isdigit():
            print(f"✅ Code nhập: {code}")
        else:
            print("⚠️ Code chưa hợp lệ")
