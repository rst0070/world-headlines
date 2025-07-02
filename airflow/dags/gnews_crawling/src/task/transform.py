from src.model.news import NewsArticle
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Any

def transform_article_type(
    article: NewsArticle
)-> Dict[str, Any]:
    # if isinstance(article.publish_date, datetime):
    #     article.publish_date = article.publish_date.strftime("%Y-%m-%d %H:%M:%S")

    return asdict(article)







