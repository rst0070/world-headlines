from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text
import logging


logger = logging.getLogger(__name__)


def get_async_engine(
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: str,
    db_name: str,
)-> AsyncEngine:
    return create_async_engine(
        f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

async def init_table(
    engine: AsyncEngine,
    table_name: str,
    table_structure: str,
    partition_by: str,
):
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name}(
                    {table_structure}
                )
                """
                )
            )

            await conn.execute(
                text(
                f"""
                CREATE TABLE IF NOT EXISTS {table_name}_{partition_by.replace("-", "_")} PARTITION OF {table_name} FOR VALUES IN ('{partition_by}')
                """
                )
            )
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise e