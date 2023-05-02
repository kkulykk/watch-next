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


async def get_user_by_uid(uid: str, db: orm.Session):
    return db.query(models.User).filter(models.User.id == uid).first()


async def get_user_by_username(username: str, db: orm.Session):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(email: str, db: orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_friends_by_uid(uid: int, db: orm.Session):
    return db.query(models.Connection).filter(models.Connection.u1 == uid).all()+\
           db.query(models.Connection).filter(models.Connection.u2 == uid).all()


async def create_connection(uid1: int, uid2: int, db: orm.Session):
    """
    create connection between users with id=uid1 and id=uid2
    """
    user1 = await get_user_by_uid(uid1, db)
    if not user1:
        raise fastapi.HTTPException(
                        status_code=401,
                        detail=f"can't connect: user with id={uid1} does not exist")
    user2 = await get_user_by_uid(uid2, db)
    if not user2:
        raise fastapi.HTTPException(
                        status_code=401,
                        detail=f"can't connect: user with id={uid2} does not exist")
    if db.query(models.Connection).filter(models.Connection.u1 == uid1).filter(models.Connection.u2 == uid2).all()+\
       db.query(models.Connection).filter(models.Connection.u2 == uid1).filter(models.Connection.u2 == uid1).all():
        raise fastapi.HTTPException(
                        status_code=400,
                        detail=f"can't connect: connection already exists")
    connection = models.Connection(uid1, uid2)
    db.add(connection)
    db.commit()
    return f"added connection {uid1}-{uid2} successfully"


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
    return f"removed connection {uid1}-{uid2} successfully"


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
    return f"removed connections of user {uid1} successfully"


async def create_user(email: str, username: str, password: str, db: orm.Session):
    """
    insert user with theese email, username
    into our database, along with a hashed password
    """
    user = await get_user_by_email(email, db)
    if user:
        raise fastapi.HTTPException(
                            status_code=401,
                            detail="email already in use")
    user_obj = models.User(
        username = username,
        email=email,
		hashed_password=hsh.bcrypt.hash(password)
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
                        status_code=401,
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
    if not user.verify_password(password):
        raise fastapi.HTTPException(
                        status_code=401,
                        detail="can't login: invalid password")
    return user


async def create_token(user: models.User):
    """
    creates access token for user
    """
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


def decode_token(token: str, db: orm.Session):
    """
    token contains user info
    decode the token and return user corresponding to the data
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return user


"""
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
"""
async def get_friends_of_current_user(
    db: orm.Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2schema),
):
    user = get_current_user(db,token)
    return get_friends_by_user(user.id)
"""