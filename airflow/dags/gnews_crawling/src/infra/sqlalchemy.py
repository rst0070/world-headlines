from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


def get_async_engine(
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: str,
    db_name: str,
):
    return create_async_engine(
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
