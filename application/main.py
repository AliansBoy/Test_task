from typing import List

from fastapi import FastAPI, HTTPException

from application import crud
from application.schemas import game_schema, user_schema
from .database import metadata, engine, database

metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=user_schema.User)
async def create_user(user: user_schema.UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


@app.get("/users/", response_model=list[user_schema.User])
async def read_users(skip: int = 0, limit: int = 100):
    users = await crud.get_users(skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=user_schema.User)
async def read_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=game_schema.Game)
async def create_item_for_user(user_id: int, game: game_schema.GameCreate):
    return await crud.create_user_game(game=game, user_id=user_id)


@app.get("/items/", response_model=List[game_schema.Game])
async def read_items(skip: int = 0, limit: int = 100):
    return await crud.get_games(skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=user_schema.GameUser)
async def read_item(game_id: int):
    return await crud.get_item_user(game_id=game_id)
