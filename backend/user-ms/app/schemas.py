from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from fastapi import Form

@dataclass
class AdditionalUserDataForm:
    email: str = Form()

class User(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str
    class Config:
        orm_mode = True
