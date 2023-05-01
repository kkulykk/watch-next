from sqlalchemy import Column, Integer, String, ForeignKey
import sqlalchemy.orm as orm
import passlib.hash as hsh

from app import database


class User(database.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    hashed_password = Column(String(256))
    
    def __str__(self):
        return f"User<{self.id},{self.email},{self.username},{self.hashed_password}>"

    def verify_password(self, password: str):
        return hsh.bcrypt.verify(password, self.hashed_password)

class Connection(database.Base):
    __tablename__ = "friend"
    id = Column(Integer, primary_key=True, index=True)
    u1 = orm.mapped_column(ForeignKey("user.id"))
    u2 = orm.mapped_column(ForeignKey("user.id"))
    
    def __str__(self):
        return f"Connection<{self.u1},{self.u2}>"

database.Base.metadata.create_all(bind=database.engine)
