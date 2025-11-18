-- =============================================
--                  SAMPLE DATA 
-- =============================================

INSERT INTO Account (id, username, password_hash, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method) VALUES
(1, 'user1', '$2a$04$SKvbUbs365RKgNnVcdWs2eHqickqVQnSFveB2s0HUTIPEOmZGxnB2','user1@example.com', '0912345678', 'admin', 'active', '2024-01-01', '2024-06-01 08:00:00', NULL, 0, '192.168.1.1', 'password'),
(2, 'user2', '$2a$04$SKvbUbs365RKgNnVcdWs2eHqickqVQnSFveB2s0HUTIPEOmZGxnB2', 'user2@example.com', '0912345679', 'user', 'active', '2024-01-01', '2024-06-02 09:00:00', NULL, 0, '192.168.1.2', 'password'),
(3, 'user3', '$2a$04$SKvbUbs365RKgNnVcdWs2eHqickqVQnSFveB2s0HUTIPEOmZGxnB2', 'user3@example.com', '0912345680', 'user', 'inactive', '2024-01-01', '2024-06-03 10:00:00', NULL, 0, '192.168.1.3', 'password'),
(4, 'user4', '$2a$04$SKvbUbs365RKgNnVcdWs2eHqickqVQnSFveB2s0HUTIPEOmZGxnB2', 'user4@example.com', '0912345681', 'user', 'active', '2024-01-01', '2024-06-04 11:00:00', NULL, 0, '192.168.1.4', 'password'),
(5, 'user5', '$2a$04$SKvbUbs365RKgNnVcdWs2eHqickqVQnSFveB2s0HUTIPEOmZGxnB2',  'user5@example.com', '0912345682', 'user', 'inactive', '2024-01-01', '2024-06-05 12:00:00', NULL, 0, '192.168.1.5', 'password');


INSERT INTO Profile (employee_code, full_name, date_of_birth, gender, address, position, department, start_date, salary, education_level, license_number, emergency_contact_name, emergency_contact_relation, emergency_contact_phone, photo_path, account_id) VALUES
('EMP001', 'Nguyễn Thị Hoa', '1985-03-15', 'Female', '123 Lê Lợi, Q.1, TP.HCM', 'Bác sĩ Nội', 'Nội khoa', '2010-06-01', 25000000.00, 'Đại học Y Hà Nội', 'BS123456', 'Nguyễn Văn Hùng', 'Chồng', '0911222333', '/images/hoa.png', 1),
('EMP002', 'Trần Văn Long', '1979-08-21', 'Male', '456 Nguyễn Trãi, Q.5, TP.HCM', 'Trưởng khoa', 'Ngoại khoa', '2005-01-15', 40000000.00, 'Đại học Y Dược TP.HCM', 'BS654321', 'Trần Thị Lan', 'Vợ', '0908333444', '/images/long.png', 2);


-- Final check
SELECT 'Database created successfully! 🎉' AS status;
SELECT COUNT(*) AS total_accounts FROM Account;
SELECT COUNT(*) AS total_patients FROM Patient;
