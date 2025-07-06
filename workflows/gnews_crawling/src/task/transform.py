import asyncio

from src.component.llm import LLMClient
from src.infra.litellm import get_litellm_router
from src.model.news import NewsArticle
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Any, List
from jinja2 import Template
import os
import json

PROMPT_EN_EXTRACTION = Template(
    open(
        os.path.join(
            os.path.dirname(__file__), 
            "../prompt/en_extraction.jinja2"
        )
    ).read()
)


async def transform_news_translation(
    news_articles: List[NewsArticle],
    llm_client: LLMClient,
) -> List[NewsArticle]:
    global PROMPT_EN_EXTRACTION

    input_articles = []

    for idx, news_article in enumerate(news_articles):
        input_articles.append(
            {
                "id": str(idx),
                "title": news_article.title,
                "description": news_article.description,
                "language": news_article.language
            }
        )

    response = await llm_client.generate_response(
        messages=[
            {
                "role": "user", 
                "content": PROMPT_EN_EXTRACTION.render(articles_json=json.dumps(input_articles, ensure_ascii=False))
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "save_en_article",
                    "description": "Save the translated article and keywords to the database",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Article ID"
                        },
                        "en_title": {
                            "type": "string",
                            "description": "English translation of the article title"
                        },
                        "en_description": {
                            "type": "string",
                            "description": "English translation of the article description"
                        },
                        "en_keywords": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of 3-5 relevant keywords in English",
                            "minItems": 3,
                            "maxItems": 5
                        }
                    },
                    "required": ["id", "en_title", "en_description", "en_keywords"]
                    }
                }
            }
        ],
        tool_choice="required"
    )

    transformed_articles = []

    for tool_call in response["tool_calls"]:
        article = news_articles[int(tool_call["arguments"]["id"])]
        article.en_title = tool_call["arguments"]["en_title"]
        article.en_description = tool_call["arguments"]["en_description"]
        article.en_keywords = tool_call["arguments"]["en_keywords"]
        transformed_articles.append(article)

    return transformed_articles

def transform_article_type(
    article: NewsArticle
)-> Dict[str, Any]:
    return asdict(article)
