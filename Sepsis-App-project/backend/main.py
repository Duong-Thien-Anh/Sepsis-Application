from flask import Flask
from app.models.database import init_db
from app.routes.patient_routes import patient_bp
from app.routes.predict_routes import predict_bp
from app.routes.statistics_routes import stats_bp
from app.routes.login_routes import login_bp   # 👈 thêm

app = Flask(__name__)

# Kết nối DB
init_db(app)

# Đăng ký route
app.register_blueprint(patient_bp, url_prefix="/api/patient")
app.register_blueprint(predict_bp, url_prefix="/api/predict")
app.register_blueprint(stats_bp, url_prefix="/api/statistics")
app.register_blueprint(login_bp, url_prefix="/api/auth")  # 👈 thêm

if __name__ == '__main__':
    app.run(debug=True)
