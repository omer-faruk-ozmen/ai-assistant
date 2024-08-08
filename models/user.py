from models import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    is_blocked = db.Column(db.Boolean,nullable=True,default=False)

    patients = db.relationship('Patient', backref='user', lazy=True)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
