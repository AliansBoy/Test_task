from pydantic import BaseModel, conint, EmailStr
from application.schemas.game_schema import Game, GameBase


class UserBase(BaseModel):
    email: EmailStr
    age: conint(ge=0, le=100)
    name: str


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    games: list[Game] = []

    class Config:
        orm_mode = True


class GameUser(GameBase):
    id: int
    user: UserInDB

    class Config:
        orm_mode = True
