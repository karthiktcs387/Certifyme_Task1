from flask import Flask, send_from_directory
from extensions import db
from datetime import timedelta
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qatar-admin-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qatar_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

db.init_app(app)

from auth import auth_bp
from opportunities import opp_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(opp_bp, url_prefix='/api/opportunities')

# Path to the sky folder where HTML/CSS/JS live
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sky')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'admin.html')

@app.route('/admin.css')
def css():
    return send_from_directory(FRONTEND_DIR, 'admin.css')

@app.route('/admin.js')
def js():
    return send_from_directory(FRONTEND_DIR, 'admin.js')

with app.app_context():
    import models
    db.create_all()
    print('Database tables created.')

if __name__ == '__main__':
    app.run(debug=True)