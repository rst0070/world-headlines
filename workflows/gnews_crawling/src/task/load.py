from src.model.news import NewsArticle
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from typing import List


async def load_news_article_batch(
    engine: AsyncEngine,
    table_name: str,
    article_list: List[NewsArticle],
):
    async with engine.begin() as conn:
        await conn.execute(
            text(
                f"""
                INSERT INTO {table_name} (country_code, url, title, description, image_url, publish_date, source, en_title, en_description, en_keywords)
                VALUES (:country_code, :url, :title, :description, :image_url, :publish_date, :source, :en_title, :en_description, :en_keywords)
                """
            ),
            article_list,
        )