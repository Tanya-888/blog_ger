from db import Session
import hashlib
from model.models import User

class UserController:
    @staticmethod
    def register(username, password, repeat_password):
        if password != repeat_password:
            raise ValueError("Passwords do not match")

        with Session as session:
            existing_user = session.query(User).filter_by(name=username).first()
            if existing_user:
                raise ValueError("Username already taken")

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            new_user = User(name=username, password=hashed_password)

            session.add(new_user)

            session.commit()

            session.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def login(username, password):
        
        with Session as session:
            existing_user = session.query(User).filter_by(name=username).first()
            if not existing_user:
                raise ValueError("Invalid username or password")

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if existing_user.password != hashed_password:
                raise ValueError("Invalid username or password")
        
        return existing_user
    
    @staticmethod
    def check_user(username, hashed_password):
        with Session as session:
            existing_user = session.query(User).filter_by(name=username).first()
            if not existing_user:
                raise ValueError("Invalid credentials")

            if existing_user.password != hashed_password:
                raise ValueError("Invalid credentials")
        
        return

    @staticmethod
    def get_users():
        with Session as session:
            users = session.query(User).all()
        
        return users