import fastapi as fastapi
import fastapi.security as security
import jwt as jwt
import datetime as dt
import sqlalchemy.orm as orm
import passlib.hash as hsh

from app import database
from app import models
from app import schemas

from typing import Annotated

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/token")

JWT_SECRET = "myjwtsecret"

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_users(db : orm.Session):
    return db.query(models.User).all()

async def get_friends(db : orm.Session):
    return db.query(models.Connection).all()

async def get_user_by_username(username: str, db: orm.Session):
    return db.query(models.User).filter(models.User.username == username).first()

async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def get_friends_by_uid(uid: int, db: orm.Session):
    return db.query(models.Connection).filter(models.Connection.u1 == uid).all()+\
           db.query(models.Connection).filter(models.Connection.u2 == uid).all()

async def create_connection(uid1: int, uid2: int, db: orm.Session):
    if db.query(models.Connection).filter(models.Connection.u1 == uid1).filter(models.Connection.u2 == uid2).all()+\
       db.query(models.Connection).filter(models.Connection.u2 == uid1).filter(models.Connection.u2 == uid1).all():
        return "connection already exists"
    connection = models.Connection(uid1, uid2)
    db.add(connection)
    db.commit()
    return True                                     

async def create_user(email: str, username: str, password: str, db: orm.Session):
    user_obj = models.User(
        username = username,
        email=email,
		hashed_password=hsh.bcrypt.hash(password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def login(username: str, password: str, db: orm.Session):
    user = await get_user_by_username(username, db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    print("user", user)
    return user

async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return schemas.User.from_orm(user)
"""
async def get_friends_of_current_user(
    db: orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    user = get_current_user(db,token)
    return get_friends_by_user(user.id)
"""
def decode_token(token: str, db: orm.Session):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return user
