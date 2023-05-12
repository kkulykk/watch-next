import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm

from app import services
from app import schemas 

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.responses import ORJSONResponse, PlainTextResponse
from fastapi_jwt_auth import AuthJWT

from pydantic.dataclasses import dataclass

import json

app = fastapi.FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return "Hello! I amd the user server"


@app.get("/hello/{name}")
async def hello(name: str):
    return f"Hello {name}! My name is user service!"


@app.get("/users", response_class=PlainTextResponse)
async def users(
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """
    for developers: see all users in db
    """
    users = await services.get_users(db)
    users = {f"{i}": str(u) for i,u in enumerate(users)}
    return PlainTextResponse(json.dumps(users,indent=2))


@app.get("/users/{username}", response_class=PlainTextResponse)
async def users(
    username: str,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """
    for developers: see all users in db
    """
    user = await services.get_user_by_username(db)
    user = vars(user)
    return PlainTextResponse(json.dumps(user,indent=2))


@app.get("/connections", response_class=PlainTextResponse)
async def connections(
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """
    for developers: see all connections in db
    """
    connections = await services.get_friends(db)
    connections = {f"{i}": str(u) for i,u in enumerate(connections)}
    return PlainTextResponse(json.dumps(connections,indent=2))


@app.get("/connections/{username}", response_class=PlainTextResponse)
async def connections(
    username: str,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """
    for developers: see all connections in db
    """
    user = services.get_user_by_username(username)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    connections = await services.get_friends_by_uid(user.id, db)
    connections = {f"{i}": str(u) for i,u in enumerate(connections)}
    return PlainTextResponse(json.dumps(connections,indent=2))


@app.post("/create")
async def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    additional_data: Annotated[schemas.AdditionalUserDataForm, Depends()],
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """
    creates user, returns token
    """
    user = await services.create_user(additional_data.email,\
                                      form_data.username,\
                                      form_data.password, db)
    return await services.create_token(user)


@app.post("/delete")
async def delete_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    additional_data: Annotated[schemas.AdditionalUserDataForm, Depends()],
    db: orm.Session = fastapi.Depends(services.get_db)
):
    return await services.delete_account(additional_data.email,
                                        form_data.username,
                                        form_data.password, db)


@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: orm.Session = Depends(services.get_db),
):
    """
    login, return token
    """
    user = await services.login(form_data.username, form_data.password, db)
    return await services.create_token(user)


@app.post("/friends/{username}")
async def get_friends(
    username: str,
    token: schemas.Token,
    db: orm.Session = Depends(services.get_db),
):
    """
    get all my friends
    """
    user = await services.decode_and_validate_token(token.token, db)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    if user.username != username:
        raise fastapi.HTTPException(status_code=401, detail="invalid username")
    return await services.get_friends_by_uid(user.id, db)


@app.post("/request/{username}/")
async def request(
    username: str,
    friend: str,
    token: schemas.Token,
    db: orm.Session = Depends(services.get_db),
):
    """
    become friend of a person with username
    !!! Later will add friend requests
    a table that stores all requests
    shows user all his requests
    if he accepts - connection is created when db is updated
    """
    user = await services.decode_and_validate_token(token.token, db)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    if user.username != username:
        raise fastapi.HTTPException(status_code=401, detail="invalid username")
    
    friend = await services.get_user_by_username(friend, db)
    if not friend:
        raise fastapi.HTTPException(status_code=404, detail="could not find friend")
    return await services.add_request(user.id, friend.id, db)


@app.post("/accept/{username}/")
async def accept(
    username: str,
    friend: str,
    token: schemas.Token,
    db: orm.Session = Depends(services.get_db),
):
    """
    become friend of a person with username
    by acepting their request
    !!! Later will add friend requests
    a table that stores all requests
    shows user all his requests
    if he accepts - connection is created when db is updated
    """
    user = await services.decode_and_validate_token(token.token, db)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    if user.username != username:
        raise fastapi.HTTPException(status_code=401, detail="invalid username")
    return await services.create_connection(username, friend, db)


@app.post("/unfriend/{username}/")
async def unfriend(
    username: str,
    friend: str,
    token: schemas.Token,
    db: orm.Session = Depends(services.get_db),
):
    """
    unfriend friend by username
    """
    user = await services.decode_and_validate_token(token.token, db)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    if user.username != username:
        raise fastapi.HTTPException(status_code=401, detail="invalid username")
    friend = await services.get_user_by_username(friend, db)
    if not friend:
        raise fastapi.HTTPException(status_code=404, detail=f"{friend.username} no such user")
    return await services.remove_connection(user.id, friend.id, db)


@app.post("/requests/{username}/")
async def requests(
    username: str,
    token: schemas.Token,
    db: orm.Session = Depends(services.get_db),
):
    user = await services.decode_and_validate_token(token.token, db)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="could not find user")
    if user.username != username:
        raise fastapi.HTTPException(status_code=401, detail="invalid username")
    return await services.get_requests_to_user(uid)


