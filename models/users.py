# models/user.py
from extenction import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @staticmethod
    def register(username, password):        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return None,"user exists"      
        hashed_pw = generate_password_hash(password)
        
        new_user = User(username=username, password_hash=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.id

    @staticmethod
    def login(username, password):
    
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            return user.id
        
        return None,"wrong userName or PassWord"