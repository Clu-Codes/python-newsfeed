from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()

# creating a user class that inherits from the Base class.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    # uses assert keyword to check if an email address contains at @. if it does not, then it throws an error preventing the return statement from running. 
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email

        return email
    
    # checks if the password is greater than 4 characters, if it is, then password is encrypted
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 4

        return bcrypt.hashpw(password.encode('utf-8'), salt)