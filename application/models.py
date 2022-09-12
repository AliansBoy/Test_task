from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("name", String),
    Column("hashed_password", String),
    Column("age", Integer)
)


games = Table(
    "games",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("user_id", Integer, ForeignKey("users.id"))
)
