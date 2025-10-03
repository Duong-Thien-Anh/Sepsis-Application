from flask_sqlalchemy import SQLAlchemy
import urllib

db = SQLAlchemy()

def init_db(app):
    # Chuỗi kết nối SQL Server
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # hoặc tên server SQL Server của bạn
        "DATABASE=APP_SepsisManagement;"
        "Trusted_Connection=yes;"
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Gắn db vào app
    db.init_app(app)
