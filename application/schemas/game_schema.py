from pydantic import BaseModel
# from application.schemas.user_schema import User


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    user_id: int
    # users: list[User] = []

    class Config:
        orm_mode = True
