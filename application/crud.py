from application.schemas import game_schema, user_schema
from .database import database

from .models import users, games


async def get_user(user_id: int):
    user = dict(await database.fetch_one(users.select().where(users.c.id == user_id)))
    list_item = await database.fetch_all(games.select().where(games.c.user_id == user["id"]))
    user.update({"games": [dict(result) for result in list_item]})
    return user


async def get_user_by_email(email: str):
    return await database.fetch_one(users.select().where(users.c.email == email))


async def get_users(skip: int = 0, limit: int = 100):
    results = await database.fetch_all(users.select().offset(skip).limit(limit))
    return [dict(result) for result in results]


async def create_user(user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = users.insert().values(email=user.email, hashed_password=fake_hashed_password,
                                    name=user.name, age=user.age)
    user_id = await database.execute(db_user)
    return user_schema.User(**user.dict(), id=user_id)


async def create_user_game(game: game_schema.GameCreate, user_id: int):
    query = games.insert().values(**game.dict(), user_id=user_id)
    game_id = await database.execute(query)
    return game_schema.Game(**game.dict(), id=game_id, user_id=user_id)


async def get_games(skip: int = 0, limit: int = 100):
    query = games.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def get_item_user(game_id: int):
    game = dict(await database.fetch_one(games.select().where(games.c.id == game_id)))
    print(game)
    user = dict(await database.fetch_one(users.select().where(users.c.id == game["user_id"])))
    print(user)
    game.update({"user": user})
    return game
