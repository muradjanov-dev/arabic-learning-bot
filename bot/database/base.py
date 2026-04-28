from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from bot.config import settings


class Base(DeclarativeBase):
    pass


def _build_connect_args(url: str) -> dict:
    """Tweak asyncpg connection per environment."""
    args: dict = {}
    # Railway internal Postgres doesn't speak SSL
    if "railway.internal" in url:
        args["ssl"] = False
    return args


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=_build_connect_args(settings.DATABASE_URL),
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
