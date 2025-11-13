"""
Script kiểm tra kết nối MySQL Database
Chạy script này để verify:
1. MySQL server có đang chạy không
2. Credentials (.env) có đúng không
3. Database và tables có tồn tại không
4. Có thể query data được không
"""
import os
import sys
from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Màu sắc cho terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")

def print_header(message):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def test_mysql_connection():
    """Test 1: Kết nối MySQL bằng pymysql (raw connection)"""
    print_header("TEST 1: Kết nối MySQL Server")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    print_info(f"Đang kết nối tới: {user}@{host}:{port}")
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print_success(f"Kết nối MySQL server thành công!")
        print_info(f"MySQL Version: {connection.get_server_info()}")
        connection.close()
        return True
    except Exception as e:
        print_error(f"Không thể kết nối MySQL server: {e}")
        return False


def test_database_exists():
    """Test 2: Kiểm tra database có tồn tại không"""
    print_header("TEST 2: Kiểm tra Database")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Kiểm tra database
            cursor.execute("SHOW DATABASES LIKE %s", (database,))
            result = cursor.fetchone()
            
            if result:
                print_success(f"Database '{database}' tồn tại!")
                
                # Chọn database
                cursor.execute(f"USE {database}")
                print_success(f"Đã chọn database '{database}'")
                
                connection.close()
                return True
            else:
                print_error(f"Database '{database}' không tồn tại!")
                print_info("Chạy lệnh sau để tạo database:")
                print(f"    mysql -u {user} -p -e \"CREATE DATABASE {database};\"")
                connection.close()
                return False
                
    except Exception as e:
        print_error(f"Lỗi khi kiểm tra database: {e}")
        return False


def test_tables_exist():
    """Test 3: Kiểm tra các tables có tồn tại không"""
    print_header("TEST 3: Kiểm tra Tables")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    expected_tables = [
        'patient',
        'employee', 
        'account',
        'medicalhistoryrecord',
        'testresult',
        'airesult',
        'diagnosis',
        'recallappointment',
        'activitylog'
    ]
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]
            
            if not tables:
                print_error("Không có tables nào trong database!")
                print_info("Chạy file backup/database_mysql.sql để tạo tables")
                return False
            
            print_success(f"Tìm thấy {len(tables)} tables:")
            
            missing_tables = []
            for table in expected_tables:
                if table in tables:
                    print_success(f"  ✓ {table}")
                else:
                    print_error(f"  ✗ {table} (missing)")
                    missing_tables.append(table)
            
            if missing_tables:
                print_warning(f"Thiếu {len(missing_tables)} tables: {', '.join(missing_tables)}")
                return False
            else:
                print_success("Tất cả tables đều tồn tại!")
                return True
                
        connection.close()
        
    except Exception as e:
        print_error(f"Lỗi khi kiểm tra tables: {e}")
        return False


def test_sqlalchemy_connection():
    """Test 4: Kết nối qua SQLAlchemy (như app thật)"""
    print_header("TEST 4: Kết nối SQLAlchemy")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    try:
        # Tạo connection string
        DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"
        print_info(f"Connection string: mysql+pymysql://{user}:***@{host}:{port}/{database}")
        
        # Tạo engine
        engine = create_engine(DATABASE_URL, echo=False)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print_success("SQLAlchemy connection thành công!")
            
            # Test query
            result = connection.execute(text("SELECT DATABASE()"))
            current_db = result.fetchone()[0]
            print_success(f"Current database: {current_db}")
            
        return True
        
    except Exception as e:
        print_error(f"SQLAlchemy connection thất bại: {e}")
        return False


def test_query_data():
    """Test 5: Query dữ liệu từ tables"""
    print_header("TEST 5: Query Dữ Liệu")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Query Patient table
            cursor.execute("SELECT COUNT(*) as count FROM patient")
            patient_count = cursor.fetchone()['count']
            print_info(f"Patient table: {patient_count} records")
            
            # Query Employee table
            cursor.execute("SELECT COUNT(*) as count FROM employee")
            employee_count = cursor.fetchone()['count']
            print_info(f"Employee table: {employee_count} records")
            
            # Query Account table
            cursor.execute("SELECT COUNT(*) as count FROM account")
            account_count = cursor.fetchone()['count']
            print_info(f"Account table: {account_count} records")
            
            # Nếu có data, show sample
            if patient_count > 0:
                cursor.execute("SELECT patient_id, full_name, gender FROM patient LIMIT 3")
                patients = cursor.fetchall()
                print_success(f"\nSample patients (top 3):")
                for p in patients:
                    print(f"  - {p['patient_id']}: {p['full_name']} ({p['gender']})")
            else:
                print_warning("Patient table trống (chưa có dữ liệu)")
            
            print_success("\nQuery dữ liệu thành công!")
            return True
            
        connection.close()
        
    except Exception as e:
        print_error(f"Lỗi khi query dữ liệu: {e}")
        return False


def test_crud_operations():
    """Test 6: Test CRUD operations (Create, Read, Update, Delete)"""
    print_header("TEST 6: CRUD Operations")
    
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "sepsis_application")
    
    test_patient_id = "TEST_BN001"
    
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # CREATE
            print_info("Testing CREATE...")
            cursor.execute("""
                INSERT INTO patient (patient_id, full_name, gender, date_of_birth, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (test_patient_id, "Test Patient", "Nam", "1990-01-01", "0123456789"))
            connection.commit()
            print_success("✓ CREATE successful")
            
            # READ
            print_info("Testing READ...")
            cursor.execute("SELECT * FROM patient WHERE patient_id = %s", (test_patient_id,))
            result = cursor.fetchone()
            if result and result['patient_id'] == test_patient_id:
                print_success(f"✓ READ successful: {result['full_name']}")
            else:
                print_error("✗ READ failed")
                return False
            
            # UPDATE
            print_info("Testing UPDATE...")
            cursor.execute("""
                UPDATE patient 
                SET full_name = %s 
                WHERE patient_id = %s
            """, ("Test Patient Updated", test_patient_id))
            connection.commit()
            
            cursor.execute("SELECT full_name FROM patient WHERE patient_id = %s", (test_patient_id,))
            result = cursor.fetchone()
            if result['full_name'] == "Test Patient Updated":
                print_success("✓ UPDATE successful")
            else:
                print_error("✗ UPDATE failed")
                return False
            
            # DELETE
            print_info("Testing DELETE...")
            cursor.execute("DELETE FROM patient WHERE patient_id = %s", (test_patient_id,))
            connection.commit()
            
            cursor.execute("SELECT * FROM patient WHERE patient_id = %s", (test_patient_id,))
            result = cursor.fetchone()
            if result is None:
                print_success("✓ DELETE successful")
            else:
                print_error("✗ DELETE failed")
                return False
            
            print_success("\nTất cả CRUD operations hoạt động tốt!")
            return True
            
        connection.close()
        
    except Exception as e:
        print_error(f"Lỗi trong CRUD operations: {e}")
        # Cleanup: xóa test record nếu có
        try:
            connection = pymysql.connect(
                host=host, port=port, user=user, password=password,
                database=database, charset='utf8mb4'
            )
            cursor = connection.cursor()
            cursor.execute("DELETE FROM patient WHERE patient_id = %s", (test_patient_id,))
            connection.commit()
            connection.close()
        except:
            pass
        return False


def print_summary(results):
    """In tổng kết kết quả"""
    print_header("KẾT QUẢ TỔNG HỢP")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.RESET} - {test_name}")
    
    print(f"\n{Colors.BOLD}Tổng kết:{Colors.RESET}")
    print(f"  Passed: {Colors.GREEN}{passed}/{total}{Colors.RESET}")
    print(f"  Failed: {Colors.RED}{failed}/{total}{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TẤT CẢ TESTS ĐỀU PASS!{Colors.RESET}")
        print(f"{Colors.GREEN}Database connection hoàn toàn sẵn sàng!{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  MỘT SỐ TESTS FAILED{Colors.RESET}")
        print(f"{Colors.YELLOW}Kiểm tra lại cấu hình database hoặc .env file{Colors.RESET}")


def main():
    """Main function - chạy tất cả tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║      MySQL DATABASE CONNECTION TEST SCRIPT             ║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════════════════════╝{Colors.RESET}")
    
    # Kiểm tra .env file
    if not os.path.exists('.env'):
        print_error(".env file không tồn tại!")
        print_info("Tạo file .env với nội dung:")
        print("""
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=sepsis_application
        """)
        sys.exit(1)
    
    print_success(".env file tồn tại")
    
    # Chạy tất cả tests
    results = {
        "MySQL Server Connection": test_mysql_connection(),
        "Database Exists": test_database_exists(),
        "Tables Exist": test_tables_exist(),
        "SQLAlchemy Connection": test_sqlalchemy_connection(),
        "Query Data": test_query_data(),
        "CRUD Operations": test_crud_operations()
    }
    
    # In tổng kết
    print_summary(results)
    
    # Exit code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
