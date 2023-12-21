"""Database connections"""

import contextlib
import json
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
import pydantic.json
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from lawgpt.config import settings
from lawgpt.models.dbModels import User

url = URL(
    drivername=settings.DATABASE.DRIVER,
    username=settings.DATABASE.get('USERNAME', None),
    password=settings.DATABASE.get('PASSWORD', None),
    host=settings.DATABASE.get('HOST', None),
    port=settings.DATABASE.get('PORT', None),
    database=settings.DATABASE.get('NAME', None),
    query=settings.DATABASE.get('QUERY', None),
)


def _custom_json_serializer(*args, **kwargs) -> str:
    """
    Encodes json in the same way that pydantic does.
    """
    return json.dumps(*args, default=pydantic.json.pydantic_encoder, **kwargs)

engine = create_async_engine(url, echo=settings.DATABASE.PRINT_SQL, json_serializer=_custom_json_serializer)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

# 使得 get_async_session_context 和 get_user_db_context 可以使用async with语法

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)