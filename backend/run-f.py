from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from flask_mail import Mail, Message
from celery import Celery
import redis
import os

# ================================================= App Configuration =========================================================

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "aStrongSecretKey"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Redis Configuration
app.config["REDIS_URL"] = "redis://localhost:6379/0"
redis_client = redis.Redis.from_url(app.config["REDIS_URL"], decode_responses=True)

# Celery Configuration
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/2"
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# Flask-Mail Configuration
app.config["MAIL_SERVER"] = "smtpout.secureserver.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "info@---.in"
app.config["MAIL_PASSWORD"] = "-----@0411"
app.config["MAIL_DEFAULT_SENDER"] = "info@------.in"

mail = Mail(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

# ================================================= Models =========================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="employee")  # employee, manager, admin
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval required
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending, in_progress, completed
    deadline = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

with app.app_context():
    db.create_all()

# ================================================= Helper Functions =========================================================

def get_current_user():
    username = get_jwt_identity()
    return User.query.filter_by(username=username).first()

def role_required(required_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if user is None or user.role not in required_roles:
                return jsonify({"message": "Unauthorized access"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ================================================= Caching & Background Jobs =========================================================

def cache_set(key, value, expiration=300):
    redis_client.setex(key, expiration, value)

def cache_get(key):
    return redis_client.get(key)

@celery.task
def send_email(subject, recipient, body):
    """Background task for sending emails"""
    with app.app_context():
        msg = Message(subject, recipients=[recipient], body=body)
        mail.send(msg)

@celery.task
def send_daily_task_reminders():
    """Send daily task reminders to employees"""
    users = User.query.filter_by(role="employee").all()
    for user in users:
        tasks = Task.query.filter_by(assigned_user_id=user.id, status="pending").all()
        task_list = "\n".join([f"{task.title} - Due: {task.deadline}" for task in tasks])
        email_body = f"Hello {user.username},\n\nHere are your pending tasks:\n\n{task_list}"
        send_email.delay("Daily Task Reminder", user.email, email_body)

# ================================================= Authentication =========================================================

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'message': 'Username or Email already exists'})

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        send_email.delay("Welcome to Task Manager", email, "Your account has been created successfully.")
        return jsonify({'message': 'User registered successfully'})

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            return jsonify({"msg": "successfully logged in", "token": access_token})

        return jsonify({"msg": "email or password incorrect."})

# ================================================= User Approval =========================================================

class UserApprovalResource(Resource):
    @jwt_required()
    @role_required(["admin"])
    def get(self):
        users = User.query.filter_by(is_approved=False).all()
        return jsonify([user.username for user in users])

    @jwt_required()
    @role_required(["admin"])
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"})

        user.is_approved = True
        db.session.commit()
        send_email.delay("Account Approved", user.email, "Your account has been approved.")
        return jsonify({"message": "User approved successfully"})

# ================================================= Task Management =========================================================

class TaskResource(Resource):
    @jwt_required()
    @role_required(["admin", "manager"])
    def get(self, task_id=None):
        cache_key = f"task:{task_id}" if task_id else "tasks"
        cached_data = cache_get(cache_key)

        if cached_data:
            return jsonify(eval(cached_data))

        tasks = Task.query.all() if not task_id else [Task.query.get(task_id)]
        result = [{"id": t.id, "title": t.title, "status": t.status} for t in tasks]

        cache_set(cache_key, str(result), expiration=300)
        return jsonify(result)

# ================================================= Stats API =========================================================

class StatsResource(Resource):
    @jwt_required()
    @role_required(["admin", "manager"])
    def get(self):
        total_users = User.query.count()
        total_tasks = Task.query.count()
        completed_tasks = Task.query.filter_by(status="completed").count()

        return jsonify({
            "total_users": total_users,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks
        })

# ================================================= API Endpoints =========================================================

api.add_resource(SignupResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(TaskResource, '/tasks', '/task/<int:task_id>')
api.add_resource(UserApprovalResource, '/users/pending', '/users/<int:user_id>/approve')
api.add_resource(StatsResource, '/stats')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="127.0.0.1")
