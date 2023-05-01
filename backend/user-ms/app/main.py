import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm

from app import services
from app import schemas 

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.responses import ORJSONResponse, PlainTextResponse

from pydantic.dataclasses import dataclass

import json

app = fastapi.FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/allusers", response_class=PlainTextResponse)
async def users(
    db: orm.Session = fastapi.Depends(services.get_db)
):
    users = await services.get_users(db)
    users = {f"{i}": str(u) for i,u in enumerate(users)}
    return PlainTextResponse(json.dumps(users,indent=2))

@app.get("/connections", response_class=PlainTextResponse)
async def users(
    db: orm.Session = fastapi.Depends(services.get_db)
):
    connections = await services.get_friends(db)
    connections = {f"{i}": str(u) for i,u in enumerate(connections)}
    return PlainTextResponse(json.dumps(connections,indent=2))

@app.get("/")
async def root():
    return "Hello World!"

@app.get("/hello/{name}")
async def hello(name: str):
    return f"Hello {name}!"

@app.post("/create")
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    additional_data: Annotated[schemas.AdditionalUserDataForm, Depends()],
    db: orm.Session = fastapi.Depends(services.get_db)
):
    db_user = await services.get_user_by_email(additional_data.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")
    user = await services.create_user(additional_data.email,\
                                      form_data.username,\
                                      form_data.password, db)
    return await services.create_token(user)

async def get_current_user(
    db: orm.Session = fastapi.Depends(services.get_db),
    token: str = fastapi.Depends(oauth2_scheme),
):
    return services.get_current_user(db, token)

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: orm.Session = Depends(services.get_db),
):
    user = await services.login(form_data.username, form_data.password, db)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await services.create_token(user)

@app.post("/friends/{token}")
async def get_friends(
    token: str,# = Depends(services.oauth2schema),
    db: orm.Session = Depends(services.get_db),
):
    user = services.decode_token(token, db)
    print(user)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="no such user")
    return await services.get_friends_by_uid(user.id, db)

@app.get("/uc/{uid}")
async def get_friends_by_id(
    uid: int,
    db: orm.Session = Depends(services.get_db),
):
    return await services.get_friends_by_uid(uid, db)


@app.post("/connect/{token}/{friend}")
async def create_friend_connection(
    token: str,
    friend: str,
    db: orm.Session = Depends(services.get_db),
):
    user = services.decode_token(token, db)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="no such user")
    friend = await services.get_user_by_username(friend, db)
    return await services.create_connection(user.id, friend.id, db)

@app.get("/friends/{uid}")
async def get_friends_by_uid(
    uid: int,
    token: str = Depends(oauth2_scheme),
):
    return "friends"

@app.get("/add_friend/{uid}{email}")
async def get_friends_by_email(
    uid: int,
    email: str,
    token: str = Depends(oauth2_scheme),
):
    return "friends"


"""
@app.post("/token")
async def generate_token(
    user: schemas.UserLogin,
    db: orm.Session = Depends(services.get_db),
):
    user = await services.login(user.username, user.password, db)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await services.create_token(user)


@app.get("/cu")
async def get_current_user(
    db: orm.Session = Depends(services.get_db),
    token: str = Depends(services.oauth2schema),
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return schemas.User.from_orm(user)

@app.get("/users/me")
async def read_users_me(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user
"""
