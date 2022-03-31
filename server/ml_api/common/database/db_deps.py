from typing import Generator,  AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ml_api.common.config import DATABASE_URL, DATABASE_ASYNC_URL

# async connection for users
async_engine = create_async_engine(DATABASE_ASYNC_URL)
AsyncSession = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as db:
        yield db

# standard connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator:
    with Session() as db:
        yield db
