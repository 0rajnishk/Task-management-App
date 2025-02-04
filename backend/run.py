from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Api, Resource

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = 'supersecretkey'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

### 📌 USER TABLE (Authentication & Roles)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="employee")  # employee, manager, admin
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval required
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: A user can have multiple tasks
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_approved": self.is_approved,
            "created_at": self.created_at
        }


### 📌 TASK TABLE (Task Management)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")  # pending, in_progress, completed
    deadline = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Key: Assigned User (Only employees or managers can be assigned)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "deadline": self.deadline.strftime('%Y-%m-%d') if self.deadline else None,
            "assigned_user": self.assigned_user.username if self.assigned_user else None,
            "created_at": self.created_at
        }


with app.app_context():
    db.create_all() 


# @app.route('/hello')
# def hello():
#     return "hello"

class Hello(Resource):
    def get(self):
        return "Hello world from Hello class"

class Login(Resource):
    def post(self):
        data = request.get_json()
        credentials = data['credentials']
        password = data['password']

        user = User.query.filter_by(username=credentials).first() or User.query.filter_by(email=credentials).first()

        if user:
            if user.check_password(password):
                access_token = create_access_token(identity=user.username)
                return jsonify({"message":"Successfully logged in!!!", "credentials":credentials, "token":access_token})
            else:
                return {"message":"Incorrect password!!!"}
        else:
            return {"message":"Invalid User name or email. Please register!!!"}

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"message":"User name or email already exists!!!"}
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        return {"message":"Registered successfully!!!", "username":username, "email":email}

api.add_resource(Hello, '/hello')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5050, host="0.0.0.0")