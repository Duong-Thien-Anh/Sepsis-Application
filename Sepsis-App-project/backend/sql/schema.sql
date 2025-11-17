-- TODO: Viet Nam letters are still have some issues.
DROP DATABASE IF EXISTS sepsis;
CREATE DATABASE sepsis;
USE sepsis;

-- Enable to store Viet Nam letters
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = utf8mb4_unicode_ci;

-- ============= Account Table =============
CREATE TABLE Account (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'inactive',
    created_date DATE DEFAULT (CURRENT_DATE),
    last_login DATETIME,
    note TEXT,
    is_2fa_enabled TINYINT(1) DEFAULT 0,
    is_enabled TINYINT(1) DEFAULT 1,
    last_login_ip VARCHAR(100),
    login_method VARCHAR(50) DEFAULT 'password'
);

-- ============= Employee Table =============
CREATE TABLE Employee (
    code CHAR(10) PRIMARY KEY,
    account_id INTEGER UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
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

    CONSTRAINT fk_id_account 
        FOREIGN KEY (account_id) REFERENCES Account(id)
        ON DELETE CASCADE
);

-- ============= Patient Table =============
CREATE TABLE Patient (
    patient_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(255),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other'),
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
    photo_path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============= MedicalHistoryRecord =============
CREATE TABLE MedicalHistoryRecord (
    record_id VARCHAR(20) PRIMARY KEY,
    record_date DATE,
    record_type VARCHAR(100),
    description TEXT,
    patient_id VARCHAR(20) NOT NULL,
    employee_code CHAR(20) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_code) REFERENCES Employee(code) ON DELETE RESTRICT
);

-- ============= Diagnosis =============
CREATE TABLE Diagnosis (
    diagnosis_id VARCHAR(20) PRIMARY KEY,
    diagnosis_date DATE,
    symptoms TEXT,
    diagnosis_result TEXT,
    diagnosis_name VARCHAR(255),
    note TEXT,
    record_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (record_id) REFERENCES MedicalHistoryRecord(record_id) ON DELETE CASCADE
);

-- ============= TestResult =============
CREATE TABLE TestResult (
    result_id VARCHAR(20) PRIMARY KEY,
    test_type VARCHAR(100),
    test_date DATE,
    result TEXT,
    unit VARCHAR(50),
    reference_range VARCHAR(100),
    file_path VARCHAR(255),
    note TEXT,
    record_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (record_id) REFERENCES MedicalHistoryRecord(record_id) ON DELETE CASCADE
);

-- ============= AIResult =============
CREATE TABLE AIResult (
    ai_result_id VARCHAR(20) PRIMARY KEY,
    prediction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    risk_score DECIMAL(5,2),
    sepsis_probability DECIMAL(5,2),
    suggested_treatment TEXT,
    ai_evaluation_result VARCHAR(255),
    ai_model_explanation TEXT,
    diagnosis_id VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY (diagnosis_id) REFERENCES Diagnosis(diagnosis_id) ON DELETE CASCADE
);

-- ============= RecallAppointment =============
CREATE TABLE RecallAppointment (
    appointment_id VARCHAR(20) PRIMARY KEY,
    appointment_datetime DATETIME,
    message_content TEXT,
    email_status VARCHAR(50),
    note TEXT,
    patient_id VARCHAR(20) NOT NULL,
    employee_code CHAR(20) NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_code) REFERENCES Employee(code) ON DELETE RESTRICT
);

-- ============= ActivityLog =============
CREATE TABLE ActivityLog (
    log_id VARCHAR(20) PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    activity_type VARCHAR(100),
    description TEXT,
    ip_address VARCHAR(50),
    affected_object_type VARCHAR(100),
    affected_object_id VARCHAR(20),
    account_id INTEGER NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Account(id) ON DELETE CASCADE
);

-- =============================================
-- CONSTRAINTS & VALIDATIONS
-- =============================================

-- Email format
ALTER TABLE Account 
ADD CONSTRAINT chk_EmailFormat 
CHECK (email REGEXP '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}$');

-- Phone: only digits, 9-11 chars, start with 0
ALTER TABLE Account
ADD CONSTRAINT chk_PhoneFormat 
CHECK (phone REGEXP '^0[0-9]{8,10}$');

-- Same for Patient & Employee
ALTER TABLE Patient 
ADD CONSTRAINT chk_patient_phone CHECK (phone REGEXP '^0[0-9]{8,10}$');

-- =============================================
-- TRIGGERS (MySQL syntax)
-- =============================================

DELIMITER $$

-- 1. Prevent delete Admin or linked Account
CREATE TRIGGER trg_PreventDeleteLinkedAccount
BEFORE DELETE ON Account
FOR EACH ROW
BEGIN
    IF OLD.role = 'admin' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Không được phép xóa tài khoản ADMIN.';
    END IF;
    
    IF EXISTS (SELECT 1 FROM Employee WHERE username_account = OLD.username) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Không được xóa tài khoản đang liên kết với nhân viên.';
    END IF;
END$$

-- 2. Prevent AIResult if Diagnosis not exist
CREATE TRIGGER trg_CheckDiagnosisBeforeAIResult
BEFORE INSERT ON AIResult
FOR EACH ROW
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Diagnosis WHERE diagnosis_id = NEW.diagnosis_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Diagnosis ID does not exist.';
    END IF;
END$$

-- 3. Log when insert Patient
CREATE TRIGGER trg_LogInsertPatient
AFTER INSERT ON Patient
FOR EACH ROW
BEGIN
    INSERT INTO ActivityLog (
        log_id, timestamp, activity_type, description,
        ip_address, affected_object_type, affected_object_id, username_account
    ) VALUES (
        CONCAT('LOG', LPAD(FLOOR(RAND() * 99999), 5, '0')),
        NOW(),
        'Insert',
        CONCAT('New patient added: ', NEW.full_name),
        '127.0.0.1',
        'Patient',
        NEW.patient_id,
        'system'
    );
END$$

-- 4. Prevent duplicate phone/email in Patient
CREATE TRIGGER trg_UniquePhoneEmailPatient
BEFORE INSERT ON Patient
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM Patient 
        WHERE phone = NEW.phone OR email = NEW.email
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Phone or email already exists.';
    END IF;
END$$

DELIMITER ;
