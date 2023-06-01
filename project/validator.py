from pydantic import BaseModel, EmailStr, Field, validator
from .models import User
from werkzeug.security import generate_password_hash

class UserModel(BaseModel):
    username: str 
    email: EmailStr
    password: str

    @validator('username')
    def validate_username(cls, username: str) -> str:
        # Add any additional validation logic for the username
        # For example, checking for alphanumeric characters only
        if not username.isalnum():
            raise ValueError("Username must contain only alphanumeric characters")
        elif User.query.filter_by(username=username).first():
            raise ValueError("Username already exists.")
        
        return username

    @validator('password')
    def validate_password(cls, password: str) -> str:
        # Add any additional validation logic for the password
        # For example, enforcing password complexity requirements
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        elif not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter")
        elif len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")
        return generate_password_hash(password, method='sha256')
    
    @validator('email')
    def validate_email(cls, email: EmailStr) -> EmailStr:
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists.")
        return email
        
class PostModel(BaseModel):
    title:str   = Field(..., min_length=4, max_length=100)
    content:str = Field(..., min_length=4) 
    