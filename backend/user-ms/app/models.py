import datetime as _dt

from sqlalchemy import Column, Integer, String
import sqlalchemy.orm as orm
import passlib.hash as hsh

from app import database


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    hashed_password = Column(String(256))

    def verify_password(self, password: str):
        return hsh.bcrypt.verify(password, self.hashed_password)
