# Import core components
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialise SQLAlchemy database
db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    user_id  = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(20), unique=True, nullable=False)
    email    = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role     = db.Column(db.String, nullable=False, default='regular')

    # Password hashing, storing and validation
    def set_password(self, raw_password: str):
        self.password = generate_password_hash(raw_password, method='pbkdf2:sha256')

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)

    # Expose user_id as .id attribute for Flask login
    @property
    def id(self):
        return self.user_id

# Opportunity Model
class Opportunity(db.Model):
    __tablename__ = 'Opportunities'

    opportunity_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    business_unit = db.Column(db.String(20), nullable=False)

    # Relationship to User Model
    submitted_by = db.Column(
        db.Integer,
        db.ForeignKey('Users.user_id'),
        nullable=False
    )
    submitter = db.relationship('User', backref='opportunities')

    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    predicted_benefits = db.Column(db.Text, nullable=False)
    business_criticality = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='New')

    value_score = db.Column(db.Integer)
    effort_score = db.Column(db.Integer)

# Seed default admin function
def create_admin_if_not_exists():
    admin_email = 'admin@example.com'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(name='Admin', email=admin_email, role='admin')
        admin.set_password('Admin!')
        db.session.add(admin)
        db.session.commit()