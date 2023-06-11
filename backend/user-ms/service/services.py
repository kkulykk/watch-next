import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm

import jwt as jwt
import passlib.hash as hsh
from passlib.context import CryptContext

from app.repository import database
from app.repository import models
from app.domain import schemas

import time

from typing import Annotated

import os

ACCESS_TOKEN_EXPIRE_SECONDS = 1800  # 30 minutes
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']     # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


async def get_user_by_uid(uid: int, db: orm.Session):
    return db.query(models.User).filter(models.User.id == uid).first()


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_friends_by_uid(uid: int, db: orm.Session):
    return db.query(models.Connection).filter(models.Connection.u1 == uid).all()+\
           db.query(models.Connection).filter(models.Connection.u2 == uid).all()


async def get_requests_to_user(to: int, db: orm.Session):
    return db.query(models.FriendRequest).filter(models.FriendRequest.to == to).all()


async def create_connection(name1: str, name2: str, db: orm.Session):
    """
    create connection between users with id=uid1 and id=uid2
    """
    user1 = await get_user_by_username(name1, db)
    if not user1:
        raise fastapi.HTTPException(
                        status_code=404,
                        detail=f"can't connect: user {name1} does not exist")
    user2 = await get_user_by_username(name2, db)
    if not user2:
        raise fastapi.HTTPException(
                        status_code=404,
                        detail=f"can't connect: user {name2} does not exist")
    uid1 = user1.id
    uid2 = user2.id
    if db.query(models.Connection).filter(models.Connection.u1 == uid1).filter(models.Connection.u2 == uid2).all() or\
       db.query(models.Connection).filter(models.Connection.u2 == uid1).filter(models.Connection.u1 == uid1).all():
        raise fastapi.HTTPException(
                        status_code=400,
                        detail=f"can't connect: connection already exists")
    connection = models.Connection(user1.id, user2.id)
    db.add(connection)
    db.commit()
    return f"added connection successfully"


async def remove_connection(uid1: int, uid2: int, db: orm.Session):
    """
    remove a connection
    have to make 2 queries, because the user can be u1 or u2 in the connection
    """
    c = db.query(models.Connection).filter(models.Connection.u1 == uid1).filter(models.Connection.u2 == uid2)
    c.delete()
    c = db.query(models.Connection).filter(models.Connection.u2 == uid1).filter(models.Connection.u2 == uid1)
    c.delete()
    db.commit()
    return f"removed connection successfully"


async def remove_connections(uid1: int, db: orm.Session):
    """
    remove all connections that contain this user
    (before deleting them)
    """
    c = db.query(models.Connection).filter(models.Connection.u1 == uid1)
    c.delete()
    c = db.query(models.Connection).filter(models.Connection.u2 == uid1)
    c.delete()
    db.commit()
    return f"removed connections of user successfully"


async def add_request(frm: int, to: int, db: orm.Session):
    c1 = db.query(models.Connection).filter(models.Connection.u1 == frm).filter(models.Connection.u2 == to)
    c2 = db.query(models.Connection).filter(models.Connection.u2 == to).filter(models.Connection.u2 == frm)
    if c1 or c2:
        return "connection exists"
    u1 = await get_user_by_uid(frm, db)
    u2 = await get_user_by_uid(to, db)
    if not u1 or not u2:
        return fastapi.HTTPException(
                        status_code=404,
                        detail="users don't exist")
    request = models.FriendRequest(frm, to)
    db.add(request)
    db.commit()
    return "request added"


async def accept_request(frm: int, to: int, db: orm.Session):
    request = await db.query(models.FriendRequest).filter(models.FriendRequest.frm == frm).filter(models.FriendRequest.to == to).first()
    if not request:
        raise fastapi.HTTPException(
                        status_code=404,
                        detail="request does not exist")
    create_connection(frm, to, db)
    db.delete(request)
    db.commit()
    return "request added"


async def create_user(email: str, username: str, password: str, db: orm.Session):
    """
    insert user with theese email, username
    into our database, along with a hashed password
    """
    user = await get_user_by_email(email, db)
    if user:
        raise fastapi.HTTPException(
                            status_code=400,
                            detail="email already in use")
    user_obj = models.User(
        username = username,
        email=email,
        hashed_password=password_context.hash(password)
		#hashed_password=hsh.bcrypt.hash(password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def delete_account(email: str, username: str, password: str, db: orm.Session):
    """
    delets account from database
    checks if email, username and password are correct
    """
    user = await get_user_by_email(email, db)
    if not user:
        raise fastapi.HTTPException(
                        status_code=404,
                        detail="no user with this email")
    if not user.verify_password(password):
        raise fastapi.HTTPException(
                        status_code=401,
                        detail="invalid password")
    if user.username != username:
        raise fastapi.HTTPException(
                        status_code=401,
                        detail="invalid username")
    await remove_connections(user.id, db)
    db.delete(user)
    db.commit()
    return "successfully deleted user"


async def login(username: str, password: str, db: orm.Session):
    """
    if credentials are valid return the corresponding user
    """
    user = await get_user_by_username(username, db)
    if not user:
        raise fastapi.HTTPException(
                        status_code=401,
                        detail="can't login: no such user")
    #if not user.verify_password(password):
    if not password_context.verify(password, user.hashed_password):
        raise fastapi.HTTPException(
                        status_code=401,
                        detail="can't login: invalid password")
    return user


async def create_token(user: models.User):
    """
    creates access token for user
    """
    payload = {
        "id": user.id,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS # in seconds
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return dict(access_token=token, token_type="bearer")


async def decode_and_validate_token(token: str, db: orm.Session):
    """
    token contains user info
    decode the token and return user corresponding to the data
    """
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    if time.time() > payload["expires"]:
        raise fastapi.HTTPException(
            status_code=401, detail="Expired token"
        )
    user = await get_user_by_uid(int(payload["id"]), db)
    if not user:
        raise fastapi.HTTPException(
            status_code=404, detail="No such user"
        )
    return user

