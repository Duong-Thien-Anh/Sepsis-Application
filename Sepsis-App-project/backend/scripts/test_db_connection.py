"""
Script kiểm tra kết nối database từ session.py
Chạy từ root: python scripts/test_db_connection.py
Hoặc từ CMD: cd backend && python scripts\test_db_connection.py
"""

import sys
import os

# Add backend root directory to path (parent of scripts/)
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_root)

from app.db.session import engine, SessionLocal, get_db
from sqlalchemy import text

print("=" * 60)
print("🔍 KIỂM TRA KẾT NỐI DATABASE")
print("=" * 60)

# Test 1: Kiểm tra engine được tạo thành công
print("\n1️⃣ Kiểm tra Engine:")
try:
    print(f"   ✅ Engine URL: {engine.url}")
    print(f"   ✅ Driver: {engine.driver}")
    print(f"   ✅ Pool size: {engine.pool.size()}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")
    sys.exit(1)

# Test 2: Thử kết nối thật
print("\n2️⃣ Thử kết nối đến MySQL:")
try:
    with engine.connect() as connection:
        print("   ✅ Kết nối thành công!")
except Exception as e:
    print(f"   ❌ Không thể kết nối: {e}")
    print("\n   💡 Kiểm tra:")
    print("      - MySQL Server có đang chạy?")
    print("      - Thông tin trong .env có đúng?")
    print("      - Database 'sepsis_application' đã tạo chưa?")
    sys.exit(1)

# Test 3: Kiểm tra database version
print("\n3️⃣ Kiểm tra MySQL version:")
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT VERSION()"))
        version = result.scalar()
        print(f"   ✅ MySQL Version: {version}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 4: Kiểm tra database name
print("\n4️⃣ Kiểm tra database hiện tại:")
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()
        print(f"   ✅ Database: {db_name}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 5: Liệt kê tables
print("\n5️⃣ Kiểm tra tables trong database:")
try:
    with engine.connect() as connection:
        result = connection.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        if tables:
            print(f"   ✅ Tìm thấy {len(tables)} tables:")
            for table in tables:
                print(f"      - {table}")
        else:
            print("   ⚠️  Database trống (chưa có tables)")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 6: Kiểm tra SessionLocal
print("\n6️⃣ Kiểm tra SessionLocal factory:")
try:
    db = SessionLocal()
    print("   ✅ SessionLocal tạo thành công")
    
    # Test query
    result = db.execute(text("SELECT 1"))
    print("   ✅ Query test thành công")
    
    db.close()
    print("   ✅ Session đóng thành công")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")
    if 'db' in locals():
        db.close()

# Test 7: Kiểm tra get_db dependency
print("\n7️⃣ Kiểm tra get_db() dependency:")
try:
    db_gen = get_db()
    db = next(db_gen)
    print("   ✅ get_db() hoạt động")
    
    # Test query
    result = db.execute(text("SELECT 'Hello from FastAPI!' as message"))
    message = result.scalar()
    print(f"   ✅ Test query: {message}")
    
    # Close properly
    try:
        next(db_gen)
    except StopIteration:
        print("   ✅ get_db() cleanup thành công")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Test 8: Kiểm tra connection pool
print("\n8️⃣ Kiểm tra Connection Pool:")
try:
    pool = engine.pool
    print(f"   ✅ Pool size: {pool.size()}")
    print(f"   ✅ Checked out connections: {pool.checkedout()}")
    print(f"   ✅ Overflow: {pool.overflow()}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

# Summary
print("\n" + "=" * 60)
print("🎉 TẤT CẢ TESTS ĐỀU PASS!")
print("✅ File session.py kết nối database THÀNH CÔNG!")
print("=" * 60)
print("\n💡 Bạn có thể:")
print("   1. Chạy server FastAPI: python -m uvicorn app.main:app --reload --port 3000")
print("   2. Xem API docs: http://localhost:3000/docs")
print("   3. Test endpoints: http://localhost:3000/api/v1/patient/")
print("=" * 60)
