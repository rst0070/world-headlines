from src.infra.logging import init_logging, shutdown_logging
from src.infra.aiohttp import get_session, shutdown_sessions
from src.infra.playwright import get_browser_context, shutdown_browser
from src.infra.sqlalchemy import get_async_engine, init_table
from src.component.worker_item import worker_supervisor
from src.component.worker_batch import worker_batch_supervisor
from src.model.news import NewsArticle
from src.infra.env import load_env

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import List, Tuple, Dict

from src.task.extract import extract_gnews_rss, extract_article_details
from src.task.transform import transform_article_type
from src.task.load import load_news_article_batch
import asyncio
from datetime import datetime, timedelta
import logging
import os

init_logging(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

GNEWS_RSS_URLS = [
    ('us', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3'),
	('kr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3'),
	#('cn', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3'),
	#('in', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtaHBHZ0pKVGlnQVAB?ceid=IN:hi&oc=3'),
	#('de', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3'),
	#('fr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3'),
	#('jp', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3'),
	#('br', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?ceid=BR:pt-419&oc=3&hl=pt-BR&gl=BR'),
	#('ru', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3'),
	#('gb', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3'),
	#('tw', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?ceid=TW:zh-Hant&oc=3'),
	#('il', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtbDNHZ0pKVENnQVAB?ceid=IL:he&oc=3'),
	#('lb', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtRnlHZ0pNUWlnQVAB?ceid=LB:ar&oc=3')
]

async def main(
    dst_table_name: str,
    datetime_from: datetime,
    datetime_until: datetime,
):

    ## init infra
    logger.info("Initializing infra")
    load_env()

    sql_engine = get_async_engine(
        db_user=os.getenv("WORLD_HEADLINES_DB_USER"),
        db_password=os.getenv("WORLD_HEADLINES_DB_PASSWORD"),
        db_host=os.getenv("WORLD_HEADLINES_DB_HOST"),
        db_port=int(os.getenv("WORLD_HEADLINES_DB_PORT")),
        db_name=os.getenv("WORLD_HEADLINES_DB_NAME"),
    )

    await init_table(
        sql_engine,
        dst_table_name,
        NewsArticle.get_table_structure(),
    )
    
    
    logger.info("Infra initialized")
    
    ## define tasks

    async def task1(
        item: Tuple[str, str],
        params: Dict
    )-> List[NewsArticle]:
        return await extract_gnews_rss(
            get_session(),
            item[0],
            item[1],
            params["datetime_from"],
            params["datetime_until"],
            params["max_num"],
        )

    async def task2(
        item: NewsArticle,
        params
    )-> NewsArticle:
        return await extract_article_details(
            await get_browser_context(),
            item,
        )

    async def task3(
        item: NewsArticle,
        params: Dict
    ):
        return transform_article_type(
            item
        )

    async def task4(
        batch: List[NewsArticle],
        params: Dict
    ):
        await load_news_article_batch(
            params["engine"],
            params["table_name"],
            batch,
        )
    
    num_step1_workers = 2
    num_step2_workers = 20
    num_step3_workers = 20
    num_step4_workers = 1

    queue0 = asyncio.Queue()
    queue1 = asyncio.Queue()
    queue2 = asyncio.Queue()
    queue3 = asyncio.Queue()
    
    steps = [
        worker_supervisor(
            "extract_gnews_rss",
            task1,
            num_workers=num_step1_workers,
            input_queue=queue0,
            output_queue=queue1,
            num_next_workers=num_step2_workers,
            params={
                "datetime_from": datetime_from,
                "datetime_until": datetime_until,
                "max_num":5
            }
        ),
        worker_supervisor(
            "extract_article_details",
            task2,
            num_workers=num_step2_workers,
            input_queue=queue1,
            output_queue=queue2,
            num_next_workers=num_step3_workers,
        ),
        worker_supervisor(
            "transform_article_type",
            task3,
            num_workers=num_step3_workers,
            input_queue=queue2,
            output_queue=queue3,
            num_next_workers=num_step4_workers,
        ),
        worker_batch_supervisor(
            "load_articles",
            task4,
            num_workers=num_step4_workers,
            input_queue=queue3,
            input_batch_size=1,

            params={
                "engine":sql_engine,
                "table_name":dst_table_name,
            },
        ),
    ]

    ## feed initializing data
    for item in GNEWS_RSS_URLS:
        queue0.put_nowait(item)
    
    for _ in range(num_step1_workers):
        queue0.put_nowait(None)
    
    ## run
    await asyncio.gather(*steps, return_exceptions=True)
    
    ## shutdown infra
    await shutdown_sessions()
    await shutdown_browser()
    shutdown_logging()


if __name__ == "__main__":
    time_now = datetime.now()
    asyncio.run(
        main(
            datetime_from=time_now - timedelta(hours=1),
            datetime_until=time_now,
            dst_table_name="GNEWS_ARTICLES",
        )
    )