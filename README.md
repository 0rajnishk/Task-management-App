## Task Management API Documentation

### Authentication
#### `/login`
**Method:** POST  
**Access:** Public  
**Description:** Authenticate users and generate an access token for session management. Requires email and password.

#### `/register`
**Method:** POST  
**Access:** Public  
**Description:** Allows new users to register. Requires name, email, username, password.

---

### User Verification (Admin Only)
#### `/users/pending`
**Method:** GET  
**Access:** Admin  
**Description:** Fetch a list of users who have registered but are pending approval.

#### `/users/<id>/approve`
**Method:** PUT  
**Access:** Admin  
**Description:** Approve a pending user account, granting them access based on their role.

#### `/users/<id>/reject`
**Method:** DELETE  
**Access:** Admin  
**Description:** Reject a pending user registration, removing them from the system.

---

### User Management
#### `/users`
**Method:** GET  
**Access:** Admin, Manager  
**Description:** Fetch a list of all registered users in the system.

#### `/user/<id>`
**Method:** GET  
**Access:** Admin  
**Description:** Retrieve detailed information about a specific user by their ID.

#### `/users/<id>`
**Method:** PUT  
**Access:** Admin  
**Description:** Update the details of a specific user, such as name, role, or status.

#### `/users/<id>`
**Method:** DELETE  
**Access:** Admin  
**Description:** Permanently remove a user from the system.

---

### Task Management
#### `/tasks`
**Method:** GET  
**Access:** Admin  
**Description:** Retrieve all tasks in the system.

#### `/tasks/mine`
**Method:** GET  
**Access:** Employee  
**Description:** Fetch a list of tasks assigned to the currently authenticated employee.

#### `/task/<id>`
**Method:** GET  
**Access:** Assigned Users, Manager, Admin  
**Description:** Retrieve details of a specific task by its ID.

#### `/tasks`
**Method:** POST  
**Access:** Manager, Admin  
**Description:** Create a new task. Requires title, description, deadline, and optionally an assigned employee.

#### `/task/<id>`
**Method:** PUT  
**Access:** Manager, Admin  
**Description:** Update task details such as title, description, or deadline.

#### `/task/<id>/status`
**Method:** PUT  
**Access:** Assigned Employee, Manager, Admin  
**Description:** Update the status of a task (e.g., pending, in-progress, completed).

#### `/task/<id>/assign`
**Method:** PUT  
**Access:** Manager  
**Description:** Assign a task to a specific employee.

#### `/tasks/<id>`
**Method:** DELETE  
**Access:** Admin  
**Description:** Remove a task from the system.

---

### Statistics & Reports
#### `/stats`
**Method:** GET  
**Access:** Admin, Manager  
**Description:** Retrieve system-wide statistics, such as total tasks, completed tasks, and user activity reports.











-------------------

--------
---
---






















## Task Management API Documentation

### Authentication
#### `/login`
**Method:** POST  
**Access:** Public  
**Description:** Authenticate users and generate an access token for session management. Requires email and password.

#### `/register`
**Method:** POST  
**Access:** Public  
**Description:** Allows new users to register. Requires name, email, password, and role (e.g., employee, manager, admin).

---

### User Verification (Admin Only)
#### `/users/pending`
**Method:** GET  
**Access:** Admin  
**Description:** Fetch a list of users who have registered but are pending approval.

#### `/users/<id>/approve`
**Method:** PUT  
**Access:** Admin  
**Description:** Approve a pending user account, granting them access based on their role.

#### `/users/<id>/reject`
**Method:** DELETE  
**Access:** Admin  
**Description:** Reject a pending user registration, removing them from the system.

---

### User Management
#### `/users`
**Method:** GET  
**Access:** Admin, Manager  
**Description:** Fetch a list of all registered users in the system.

#### `/user/<id>`
**Method:** GET  
**Access:** Admin  
**Description:** Retrieve detailed information about a specific user by their ID.

#### `/users/<id>`
**Method:** PUT  
**Access:** Admin  
**Description:** Update the details of a specific user, such as name, role, or status.

#### `/users/<id>`
**Method:** DELETE  
**Access:** Admin  
**Description:** Permanently remove a user from the system.

---

### Task Management
#### `/tasks`
**Method:** GET  
**Access:** Admin  
**Description:** Retrieve all tasks in the system.

#### `/tasks/mine`
**Method:** GET  
**Access:** Employee  
**Description:** Fetch a list of tasks assigned to the currently authenticated employee.

#### `/task/<id>`
**Method:** GET  
**Access:** Assigned Users, Manager, Admin  
**Description:** Retrieve details of a specific task by its ID.

#### `/tasks`
**Method:** POST  
**Access:** Manager, Admin  
**Description:** Create a new task. Requires title, description, deadline, and optionally an assigned employee.

#### `/task/<id>`
**Method:** PUT  
**Access:** Manager, Admin  
**Description:** Update task details such as title, description, or deadline.

#### `/task/<id>/status`
**Method:** PUT  
**Access:** Assigned Employee, Manager, Admin  
**Description:** Update the status of a task (e.g., pending, in-progress, completed).

#### `/task/<id>/assign`
**Method:** PUT  
**Access:** Manager  
**Description:** Assign a task to a specific employee.

#### `/tasks/<id>`
**Method:** DELETE  
**Access:** Admin  
**Description:** Remove a task from the system.

---

### Statistics & Reports
#### `/stats`
**Method:** GET  
**Access:** Admin, Manager  
**Description:** Retrieve system-wide statistics, such as total tasks, completed tasks, and user activity reports.

---

### Implementation in Flask

The following Flask API endpoints implement the above functionalities:

```python
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["JWT_SECRET_KEY"] = "aStrongSecretKey"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="employee")
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    deadline = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

with app.app_context():
    db.create_all()

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
        return {username: username, email: email}

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

api.add_resource(SignupResource, '/register')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="127.0.0.1")
```
