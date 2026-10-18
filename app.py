from flask import Flask
from flask_login import LoginManager
from database import db
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "aicmdss_secret_key_2026"  # change this to anything random
app.permanent_session_lifetime = timedelta(hours=8)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"        # redirect here if not logged in
login_manager.login_message = "Please login to access this page."

# Load user for session management
from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# Register blueprints (each module gets its own file)
from routes.auth_routes import auth_bp
app.register_blueprint(auth_bp)

from routes.dashboard_routes import dashboard_bp
app.register_blueprint(dashboard_bp)

from routes.complaint_routes import complaint_bp
app.register_blueprint(complaint_bp)

from routes.ai_routes import ai_bp
app.register_blueprint(ai_bp)

from routes.fir_routes import fir_bp
app.register_blueprint(fir_bp)

from routes.assignment_routes import assignment_bp
app.register_blueprint(assignment_bp)

from routes.reports_routes import reports_bp
app.register_blueprint(reports_bp)

from routes.freeze_routes import freeze_bp
app.register_blueprint(freeze_bp)

if __name__ == "__main__":
    app.run(debug=True)