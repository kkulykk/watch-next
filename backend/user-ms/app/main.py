import fastapi as fastapi
import fastapi.security as security
import sqlalchemy.orm as orm

from app import services
from app import schemas 

app = fastapi.FastAPI()

@app.get("/")
async def root():
	return "Hello World!"

@app.get("/hello/{name}")
async def hello(name: str):
	return f"Hello {name}!"

@app.post("/api/create")
async def create_user(
    user: schemas.UserCreate,
	db: orm.Session = fastapi.Depends(services.get_db)
):
    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await services.create_user(user, db)
    return await services.create_token(user)

@app.post("/api/login")
async def login(
    user: schemas.UserLogin,
    db: orm.Session = fastapi.Depends(services.get_db),
):
    user = await services.login(user, db)
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")
    return await services.create_token(user)

"""
@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(_services.get_db),
):
    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user)
"""


