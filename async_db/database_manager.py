import logging
import os
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import Base  # предполагается, что Base декларативный

logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self, db_url: str, echo: bool = False):
        self.db_url = db_url
        self.engine = create_async_engine(db_url, echo=echo)
        self.AsyncSessionFactory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def init_db(self):
        logger.debug(f"Creating app Database with url {self.engine.url}")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self.AsyncSessionFactory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                # logger.error(str(e))
                raise
            finally:
                await session.close()

    def get_session(self) -> AsyncSession:
        return self.AsyncSessionFactory()


manager = DBManager(os.getenv("DB_URL"))
