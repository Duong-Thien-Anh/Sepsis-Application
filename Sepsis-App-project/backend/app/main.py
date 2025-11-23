"""
FastAPI Backend cho Sepsis Management Application
Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import patient
# from app.db.session import engine
# from app.models.models import Patient  # Import models để tạo tables

# Import Base từ db.session để tạo tables
# from app.db.session import Base

# Tạo tất cả tables nếu chưa có (TẮT ĐI khi SQL Server chưa sẵn sàng)
# Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI app
app = FastAPI(
    title="Sepsis Management API",
    description="API cho ứng dụng quản lý bệnh nhân Sepsis",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS middleware cho Desktop App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins (Desktop app)
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả HTTP methods
    allow_headers=["*"],  # Cho phép tất cả headers
)

# Đăng ký routes
app.include_router(
    patient.router,
    prefix="/api/v1/patient",
    tags=["Patient"]
)

# TODO: Thêm các routes khác
# app.include_router(employee.router, prefix="/api/v1/employee", tags=["Employee"])
# app.include_router(predict.router, prefix="/api/v1/predict", tags=["Predict"])
# app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["Statistics"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/", tags=["Root"])
def root():
    """Root endpoint"""
    return {
        "message": "Sepsis Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,  # Đổi sang port 3000
        reload=True  # Auto reload khi code thay đổi (dev mode)
    )
