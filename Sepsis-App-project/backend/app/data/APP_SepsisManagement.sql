CREATE DATABASE APP_SepsisManagement;

-- Table: Account
CREATE TABLE Account (
    account_id INT PRIMARY KEY NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    role VARCHAR(50),
    status VARCHAR(50),
    created_date DATE,
    last_login DATETIME,
    note TEXT,
    is_2fa_enabled BIT,
    last_login_ip VARCHAR(100),
    login_method VARCHAR(50)
);

-- Table: Employee
CREATE TABLE Employee (
    employee_id VARCHAR(20) PRIMARY KEY NOT NULL,
    full_name VARCHAR(255),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    position VARCHAR(100),
    department VARCHAR(100),
    start_date DATE,
    salary DECIMAL(15,2),
    education_level VARCHAR(100),
    license_number VARCHAR(100),
    emergency_contact_name VARCHAR(255),
    emergency_contact_relation VARCHAR(50),
    emergency_contact_phone VARCHAR(20),
    photo_path VARCHAR(255),
    username_account VARCHAR(100) UNIQUE,
    CONSTRAINT fk_username_account FOREIGN KEY (username_account) REFERENCES Account(username)
);

-- Table: Patient
CREATE TABLE Patient (
    patient_id VARCHAR(20) PRIMARY KEY NOT NULL,
    full_name VARCHAR(255),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    blood_type VARCHAR(10),
    height_cm INT,
    weight_kg DECIMAL(5,2),
    medical_history TEXT,
    emergency_contact_name VARCHAR(255),
    emergency_contact_relation VARCHAR(50),
    emergency_contact_phone VARCHAR(20),
    photo_path VARCHAR(255)
);

-- Table: MedicalHistoryRecord
CREATE TABLE MedicalHistoryRecord (
    record_id VARCHAR(20) PRIMARY KEY NOT NULL,
    record_date DATE,
    record_type VARCHAR(100),
    description TEXT,
    patient_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- Table: Diagnosis
CREATE TABLE Diagnosis (
    diagnosis_id VARCHAR(20) PRIMARY KEY NOT NULL,
    diagnosis_date DATE,
    symptoms TEXT,
    diagnosis_result TEXT,
    diagnosis_name VARCHAR(255),
    note TEXT,
    record_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (record_id) REFERENCES MedicalHistoryRecord(record_id)
);

-- Table: TestResult
CREATE TABLE TestResult (
    result_id VARCHAR(20) PRIMARY KEY NOT NULL,
    test_type VARCHAR(100),
    test_date DATE,
    result TEXT,
    unit VARCHAR(50),
    reference_range VARCHAR(100),
    file_path VARCHAR(255),
    note TEXT,
    record_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (record_id) REFERENCES MedicalHistoryRecord(record_id)
);

-- Table: AIResult
CREATE TABLE AIResult (
    ai_result_id VARCHAR(20) PRIMARY KEY NOT NULL,
    prediction_time DATETIME,
    risk_score DECIMAL(5,2),
    sepsis_probability DECIMAL(5,2),
    suggested_treatment TEXT,
    ai_evaluation_result VARCHAR(255),
    ai_model_explanation TEXT,
    diagnosis_id VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY (diagnosis_id) REFERENCES Diagnosis(diagnosis_id)
);

-- Table: RecallAppointment
CREATE TABLE RecallAppointment (
    appointment_id VARCHAR(20) PRIMARY KEY NOT NULL,
    appointment_datetime DATETIME,
    message_content TEXT,
    email_status VARCHAR(50),
    note TEXT,
    patient_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- Table: ActivityLog
CREATE TABLE ActivityLog (
    log_id VARCHAR(20) PRIMARY KEY NOT NULL,
    timestamp DATETIME,
    activity_type VARCHAR(100),
    description TEXT,
    ip_address VARCHAR(50),
    affected_object_type VARCHAR(100),
    affected_object_id VARCHAR(20),
    username_account VARCHAR(100) NOT NULL,
    FOREIGN KEY (username_account) REFERENCES Account(username)
);


--TRIGGER--
CREATE TRIGGER trg_PreventDeleteLinkedAccount  --không cho xóa tài khoản đang hoạt động, tài khoản Admin--
ON Account
INSTEAD OF DELETE
AS
BEGIN
    -- Ngăn xóa tài khoản admin
    IF EXISTS (
        SELECT 1 FROM deleted WHERE role = 'admin'
    )
    BEGIN
        RAISERROR('Không được phép xóa tài khoản có vai trò ADMIN.', 16, 1);
        RETURN;
    END

    -- Ngăn xóa tài khoản đang được liên kết với nhân viên
    IF EXISTS (
        SELECT 1 FROM Employee
        WHERE username_account IN (SELECT username FROM deleted)
    )
    BEGIN
        RAISERROR('Không được xóa tài khoản đang liên kết với nhân viên.', 16, 1);
        RETURN;
    END

    -- Nếu không phải admin và không liên kết, cho phép xóa
    DELETE FROM Account
    WHERE username IN (SELECT username FROM deleted);
END;

--=====================================================================================================--
CREATE TRIGGER trg_CheckDiagnosisBeforeAIResult  --Không cho thêm AIResult nếu Diagnosis không tồn tại--
ON AIResult
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM inserted i
        WHERE NOT EXISTS (
            SELECT 1 FROM Diagnosis d WHERE d.diagnosis_id = i.diagnosis_id
        )
    )
    BEGIN
        RAISERROR('Cannot insert AIResult: Diagnosis ID does not exist.', 16, 1);
        RETURN;
    END

    INSERT INTO AIResult
    SELECT * FROM inserted;
END;

--=====================================================================================================--
CREATE TRIGGER trg_LogInsertPatient  -- Ghi log khi thêm mới bệnh nhân--
ON Patient
AFTER INSERT
AS
BEGIN
    INSERT INTO ActivityLog (
        log_id, timestamp, activity_type, description,
        ip_address, affected_object_type, affected_object_id, username_account
    )
    SELECT
        'LOG' + RIGHT('00000' + CAST(ABS(CHECKSUM(NEWID())) AS VARCHAR), 5),
        GETDATE(),
        'Insert',
        'New patient added: ' + full_name,
        '127.0.0.1',
        'Patient',
        patient_id,
        'system'
    FROM inserted;
END;

--=====================================================================================================--
CREATE TRIGGER trg_UniquePhoneEmailPatient  --Không cho trùng email hoặc phone của bệnh nhân--
ON Patient
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN Patient p ON i.phone = p.phone OR i.email = p.email
    )
    BEGIN
        RAISERROR('Phone or email already exists for another patient.', 16, 1);
        RETURN;
    END

    INSERT INTO Patient
    SELECT * FROM inserted;
END;

--=====================================================================================================--
--check email--
ALTER TABLE Account
ADD CONSTRAINT chk_EmailFormat CHECK (
    email LIKE '_%@_%._%'
);

--=====================================================================================================--
--check SĐT--
ALTER TABLE Account
ADD CONSTRAINT chk_PhoneFormat CHECK (
    phone NOT LIKE '%[^0-9]%' AND LEN(phone) BETWEEN 9 AND 11
);

--=====================================================================================================--
--check mã quốc gia--
CREATE TRIGGER trg_ValidatePhone
ON Account
AFTER INSERT, UPDATE
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM inserted
        WHERE phone NOT LIKE '0%' OR phone LIKE '%[^0-9]%'
    )
    BEGIN
        RAISERROR('Số điện thoại không hợp lệ: phải bắt đầu bằng 0 và chỉ chứa số.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;




-- Xóa trigger cũ (nếu cần)
DROP TRIGGER IF EXISTS trg_PreventDeleteLinkedAccount;

--thêm dữ liệu---
--bảng Account--
INSERT INTO Account (account_id, username, password_hash, full_name, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method)
VALUES (1, 'user1', 'hashed_pw_1', 'Nguyễn Văn An', 'user1@example.com', '0912345678', 'admin', 'active', '2024-01-01', '2024-06-01 08:00:00', NULL, 0, '192.168.1.1', 'password');

INSERT INTO Account (account_id, username, password_hash, full_name, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method)
VALUES (2, 'user2', 'hashed_pw_2', 'Trần Thị Bình', 'user2@example.com', '0912345679', 'user', 'active', '2024-01-01', '2024-06-02 09:00:00', NULL, 0, '192.168.1.2', 'password');

INSERT INTO Account (account_id, username, password_hash, full_name, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method)
VALUES (3, 'user3', 'hashed_pw_3', 'Phạm Văn Cường', 'user3@example.com', '0912345680', 'user', 'inactive', '2024-01-01', '2024-06-03 10:00:00', NULL, 0, '192.168.1.3', 'password');

INSERT INTO Account (account_id, username, password_hash, full_name, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method)
VALUES (4, 'user4', 'hashed_pw_4', 'Lê Thị Duyên', 'user4@example.com', '0912345681', 'user', 'active', '2024-01-01', '2024-06-04 11:00:00', NULL, 0, '192.168.1.4', 'password');

INSERT INTO Account (account_id, username, password_hash, full_name, email, phone, role, status, created_date, last_login, note, is_2fa_enabled, last_login_ip, login_method)
VALUES (5, 'user5', 'hashed_pw_5', 'Hoàng Quốc Đạt', 'user5@example.com', '0912345682', 'user', 'inactive', '2024-01-01', '2024-06-05 12:00:00', NULL, 0, '192.168.1.5', 'password');

--=======Bảng employee=================--
INSERT INTO Employee (employee_id, full_name, date_of_birth, gender, phone, email, address, position, department, start_date, salary, education_level, license_number, emergency_contact_name, emergency_contact_relation, emergency_contact_phone, photo_path, username_account)
VALUES 
('EMP001', 'Nguyễn Thị Hoa', '1985-03-15', 'Female', '0909123456', 'hoa.nguyen@hospital.com', '123 Lê Lợi, Q.1, TP.HCM', 'Bác sĩ Nội', 'Nội khoa', '2010-06-01', 25000000.00, 'Đại học Y Hà Nội', 'BS123456', 'Nguyễn Văn Hùng', 'Chồng', '0911222333', '/images/hoa.png', 'user1'),

('EMP002', 'Trần Văn Long', '1979-08-21', 'Male', '0909234567', 'long.tran@hospital.com', '456 Nguyễn Trãi, Q.5, TP.HCM', 'Trưởng khoa', 'Ngoại khoa', '2005-01-15', 40000000.00, 'Đại học Y Dược TP.HCM', 'BS654321', 'Trần Thị Lan', 'Vợ', '0908333444', '/images/long.png', 'user2'),

('EMP003', 'Lê Minh Tuấn', '1990-11-02', 'Male', '0909345678', 'tuan.le@hospital.com', '789 Trường Chinh, Q.Tân Bình', 'Điều dưỡng', 'Hồi sức cấp cứu', '2015-09-01', 18000000.00, 'Cao đẳng Điều dưỡng', 'DD789456', 'Lê Văn Hòa', 'Cha', '0909444555', '/images/tuan.png', 'user3'),

('EMP004', 'Phạm Thị Hà', '1987-05-30', 'Female', '0909456789', 'ha.pham@hospital.com', '321 Cách Mạng, Q.3, TP.HCM', 'Y tá trưởng', 'Khoa sản', '2012-03-20', 22000000.00, 'Cao đẳng Y tế', 'YT112233', 'Phạm Văn An', 'Cha', '0909555666', '/images/ha.png', 'user4'),

('EMP005', 'Đỗ Quang Huy', '1983-12-11', 'Male', '0909567890', 'huy.do@hospital.com', '654 Nguyễn Văn Cừ, Q.10, TP.HCM', 'Bác sĩ Xét nghiệm', 'Khoa xét nghiệm', '2008-07-15', 27000000.00, 'Đại học Y Huế', 'XN334455', 'Đỗ Thị Thanh', 'Mẹ', '0909666777', '/images/huy.png', 'user5');

--========bảng patient================--
INSERT INTO Account (account_id, username, role, created_date)
VALUES (999, 'system', 'admin', GETDATE());

INSERT INTO Patient (patient_id, full_name, date_of_birth, gender, phone, email, address, blood_type, height_cm, weight_kg, medical_history, emergency_contact_name, emergency_contact_relation, emergency_contact_phone, photo_path)
VALUES 
('PAT001', 'Lê Thị Mai', '1992-04-10', 'Female', '0911222333', 'mai.le@gmail.com', '101 Hùng Vương, Q.5, TP.HCM', 'O+', 160, 50.5, 'Tiền sử huyết áp thấp.', 'Lê Văn Hòa', 'Cha', '0988111222', '/images/patient1.png'),

('PAT002', 'Nguyễn Văn Bình', '1985-11-20', 'Male', '0912333444', 'binh.nguyen@gmail.com', '55 Nguyễn Du, Q.1, TP.HCM', 'A-', 172, 68.0, 'Tiền sử tiểu đường.', 'Nguyễn Thị Hà', 'Vợ', '0909222333', '/images/patient2.png'),

('PAT003', 'Trần Thị Hương', '1990-07-05', 'Female', '0913444555', 'huong.tran@gmail.com', '200 Cộng Hòa, Q.Tân Bình', 'B+', 158, 48.0, 'Dị ứng kháng sinh nhóm beta-lactam.', 'Trần Văn Sơn', 'Chồng', '0908333444', '/images/patient3.png'),

('PAT004', 'Phạm Văn Cường', '1978-03-18', 'Male', '0914555666', 'cuong.pham@gmail.com', '33 Điện Biên Phủ, Q.Bình Thạnh', 'AB-', 175, 75.3, 'Bệnh tim bẩm sinh.', 'Phạm Thị Thu', 'Vợ', '0909555666', '/images/patient4.png'),

('PAT005', 'Đỗ Thị Lan', '1988-09-12', 'Female', '0915666777', 'lan.do@gmail.com', '88 Hoàng Văn Thụ, Q.Phú Nhuận', 'A+', 162, 53.7, 'Tiền sử nhiễm trùng tiết niệu.', 'Đỗ Văn Hùng', 'Anh trai', '0909666777', '/images/patient5.png');

--=======bảng MedicalHistoryRecord===========--
INSERT INTO MedicalHistoryRecord (record_id, record_date, record_type, description, patient_id, employee_id)
VALUES 
('REC001', '2024-01-10', 'Initial Checkup', 'Khám tổng quát ban đầu với triệu chứng sốt và mệt mỏi.', 'PAT001', 'EMP001'),
('REC002', '2024-01-15', 'Follow-up', 'Theo dõi tình trạng sau điều trị bằng kháng sinh.', 'PAT002', 'EMP002'),
('REC003', '2024-02-01', 'Emergency', 'Cấp cứu do huyết áp tụt đột ngột.', 'PAT003', 'EMP003'),
('REC004', '2024-02-20', 'Routine Examination', 'Khám định kỳ không phát hiện bất thường.', 'PAT004', 'EMP004'),
('REC005', '2024-03-05', 'Initial Checkup', 'Bệnh nhân có triệu chứng buồn nôn và sốt nhẹ.', 'PAT005', 'EMP005');

SELECT * FROM Patient;
SELECT * FROM Employee;

--=======bảng Diagnosis===========--
INSERT INTO Diagnosis (diagnosis_id, diagnosis_date, symptoms, diagnosis_result, diagnosis_name, note, record_id)
VALUES 
('DIA001', '2024-01-10', 'Sốt cao, mệt mỏi', 'Bạch cầu tăng, nghi nhiễm trùng', 'Nhiễm trùng huyết mức độ nhẹ', 'Tiếp tục theo dõi trong 24h', 'REC001'),
('DIA002', '2024-01-15', 'Khó thở, nhiệt độ cơ thể không ổn định', 'Tình trạng cải thiện sau kháng sinh', 'Hồi phục sau nhiễm trùng huyết', 'Đã đáp ứng thuốc tốt', 'REC002'),
('DIA003', '2024-02-01', 'Choáng, da tái, nhịp tim nhanh', 'Huyết áp tụt, nghi sốc nhiễm trùng', 'Sốc nhiễm trùng', 'Cần theo dõi sát ICU', 'REC003'),
('DIA004', '2024-02-20', 'Không có triệu chứng đặc biệt', 'Các chỉ số bình thường', 'Khỏe mạnh', 'Chưa cần can thiệp y tế', 'REC004'),
('DIA005', '2024-03-05', 'Buồn nôn, sốt nhẹ, huyết áp thấp', 'CRP tăng nhẹ, dấu hiệu nhiễm trùng nhẹ', 'Nghi nhiễm trùng huyết nhẹ', 'Đề nghị xét nghiệm bổ sung', 'REC005');

--=======bảng TestResult===========--
INSERT INTO TestResult (result_id, test_type, test_date, result, unit, reference_range, file_path, note, record_id)
VALUES 
('RES001', 'CRP', '2024-01-10', '22.5', 'mg/L', '0-10', '/files/crp_PAT001.pdf', 'CRP tăng cao, gợi ý viêm', 'REC001'),
('RES002', 'Công thức máu', '2024-01-15', 'WBC: 13.4', '10^9/L', '4.0-10.0', '/files/cbc_PAT002.pdf', 'Bạch cầu tăng nhẹ', 'REC002'),
('RES003', 'Lactate', '2024-02-01', '4.1', 'mmol/L', '< 2.0', '/files/lactate_PAT003.pdf', 'Lactate tăng cao, nguy cơ sốc nhiễm trùng', 'REC003'),
('RES004', 'C-reactive protein', '2024-02-20', '5.3', 'mg/L', '0-10', '/files/crp_PAT004.pdf', 'CRP bình thường', 'REC004'),
('RES005', 'Procalcitonin', '2024-03-05', '0.9', 'ng/mL', '< 0.5', '/files/pct_PAT005.pdf', 'PCT tăng nhẹ, theo dõi tiếp', 'REC005');

--=======bảng AIResult===========--
INSERT INTO AIResult (ai_result_id, prediction_time, risk_score, sepsis_probability, suggested_treatment, ai_evaluation_result, ai_model_explanation, diagnosis_id)
VALUES 
('AI001', '2024-01-10 08:30:00', 78.5, 0.82, 'Kháng sinh phổ rộng, truyền dịch', 'Nguy cơ cao', 'Mô hình dự đoán theo chỉ số CRP và WBC tăng', 'DIA001'),
('AI002', '2024-01-15 09:00:00', 45.0, 0.40, 'Tiếp tục theo dõi, chưa cần can thiệp', 'Nguy cơ trung bình', 'WBC giảm dần, CRP hạ', 'DIA002'),
('AI003', '2024-02-01 07:45:00', 91.3, 0.95, 'Chuyển ICU, truyền kháng sinh mạnh', 'Nguy cơ rất cao', 'Lactate tăng và huyết áp giảm mạnh', 'DIA003'),
('AI004', '2024-02-20 10:15:00', 10.2, 0.05, 'Không cần điều trị', 'Nguy cơ thấp', 'Không có dấu hiệu bất thường', 'DIA004'),
('AI005', '2024-03-05 08:50:00', 60.0, 0.60, 'Theo dõi thêm, cân nhắc dùng kháng sinh', 'Nguy cơ trung bình', 'PCT và CRP tăng nhẹ, triệu chứng mơ hồ', 'DIA005');

--=======bảng RecallAppointment===========--
INSERT INTO RecallAppointment (appointment_id, appointment_datetime, message_content, email_status, note, patient_id, employee_id)
VALUES 
('APP001', '2024-01-17 09:00:00', 'Mời bạn Lê Thị Mai tái khám sau xét nghiệm CRP.', 'Đã gửi', 'Lịch hẹn định kỳ sau 1 tuần', 'PAT001', 'EMP001'),
('APP002', '2024-01-22 10:30:00', 'Nhắc tái khám kiểm tra tiểu đường.', 'Đã gửi', 'Tiểu đường cần theo dõi liên tục', 'PAT002', 'EMP002'),
('APP003', '2024-02-05 08:00:00', 'Hẹn gặp để đánh giá lại hiệu quả điều trị.', 'Đã gửi', 'Bệnh nhân có đáp ứng tốt với thuốc', 'PAT003', 'EMP003'),
('APP004', '2024-02-28 14:00:00', 'Tái khám định kỳ bệnh tim bẩm sinh.', 'Đã gửi', 'Lịch tái khám 1 tháng/lần', 'PAT004', 'EMP004'),
('APP005', '2024-03-10 09:30:00', 'Theo dõi nhiễm trùng tiết niệu.', 'Chưa gửi', 'Gửi nhắc hẹn qua email bệnh nhân', 'PAT005', 'EMP005');

--=======bảng ActivityLog===========--
INSERT INTO ActivityLog (log_id, timestamp, activity_type, description, ip_address, affected_object_type, affected_object_id, username_account)
VALUES 
('LOG001', '2024-01-10 08:05:00', 'Đăng nhập', 'Tài khoản user1 đăng nhập vào hệ thống', '192.168.1.10', 'Account', 'user1', 'user1'),
('LOG002', '2024-01-15 09:22:00', 'Thêm bệnh nhân', 'Thêm mới bệnh nhân Lê Thị Mai', '192.168.1.11', 'Patient', 'PAT001', 'user1'),
('LOG003', '2024-01-20 14:10:00', 'Tạo hồ sơ khám', 'Tạo hồ sơ khám bệnh cho PAT003', '192.168.1.12', 'MedicalHistoryRecord', 'REC003', 'user3'),
('LOG004', '2024-02-02 10:00:00', 'Chẩn đoán', 'Chẩn đoán sepsis nguy cơ cao cho PAT002', '192.168.1.13', 'Diagnosis', 'DIA002', 'user2'),
('LOG005', '2024-03-01 08:45:00', 'Tạo lịch hẹn', 'Tạo lịch tái khám cho PAT005', '192.168.1.14', 'RecallAppointment', 'APP005', 'user5');


--==================thêm cột=======================--
-- Thêm 2 trường timestamp vào bảng Patient
ALTER TABLE Patient 
ADD created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE();

-- Tạo trigger để tự động cập nhật updated_at khi có thay đổi
CREATE TRIGGER trg_UpdatePatientTimestamp
ON Patient
AFTER UPDATE
AS
BEGIN
    UPDATE Patient 
    SET updated_at = GETDATE()
    WHERE patient_id IN (SELECT patient_id FROM inserted);
END;