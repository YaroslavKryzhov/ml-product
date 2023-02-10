from typing import Generator, AsyncGenerator
from ml_api.common.db.session import AsyncSession, Session
import logging


logger = logging.getLogger(__name__)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession() as db:
        logger.info('Create session!')
        yield db


def get_db() -> Generator:
    with Session() as db:
        logger.info('Create session!')
        yield db
