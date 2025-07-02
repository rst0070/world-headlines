from src.model.news import NewsArticle
from aiohttp import ClientSession
import xml.etree.ElementTree as ET
from playwright.async_api import Page, BrowserContext
from datetime import datetime
import asyncio
from typing import List
import logging


logger = logging.getLogger(__name__)


async def extract_gnews_rss(
    session: ClientSession,
    country_code: str,
    gnews_rss_url: str,
    datetime_from: datetime,
    datetime_until: datetime,
    max_num: int,
)-> List[NewsArticle]:
    """
    1. extract gnews rss
    2. filter by datetime
    3. filter by max_num
    4. return article list
    """
    async with session.get(gnews_rss_url) as response:
        content = await response.text()

    xml_root = ET.fromstring(content)
    article_list = []

    count = 0
    for item in xml_root.find("channel").findall("item"):
        pub_date = datetime.strptime(
            item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %Z"
        )
        # pub_date = pub_date.strftime("%Y-%m-%d %H:%M:%S")

        if pub_date < datetime_from or pub_date > datetime_until:
            continue
        else:
            count += 1

        if count >= max_num:
            break

        article = NewsArticle(
            country_code=country_code,
            url=item.find("link").text,
            title=item.find("title").text,
            description=item.find("title").text,
            image_url="",
            publish_date=pub_date,
            source=item.find("source").text,
        )
        article_list.append(article)

        logger.info(f"crawled article: {item.find('title').text}")

    return article_list

async def extract_article_details(
    browser_context: BrowserContext,
    article: NewsArticle,
)-> NewsArticle:
    """
    1. open url
    2. wait for page loaded
    3. extract details
    4. return details
    """
    try:
        page = await browser_context.new_page()
        # Navigate to the URL
        await page.goto(article.url)

        await page.wait_for_timeout(10000)
        # await page.evaluate("""
        #     () => {
        #         const interval = setInterval(() => {
        #             if (!window.location.href.includes('google.com')) {
        #                 clearInterval(interval);
        #             }
        #         }, 100);
        #     }""")

        article_url = page.url
        if article_url == "about:blank":
            return article

        # Extract meta tags concurrently
        tasks = [
            page.get_attribute("meta[property='og:image']", "content", timeout=1000),
            page.get_attribute("meta[property='og:description']", "content", timeout=1000),
        ]

        try:
            image_url, description = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            await page.close()
        except Exception as e:
            print(f"Error extracting meta tags: {e}")

        # Handle exceptions from individual extractions
        if isinstance(image_url, Exception):
            print(f"couldn't get image url: {image_url}")
            image_url = None
        if isinstance(description, Exception):
            print(f"couldn't get description: {description}")
            description = article.title

        article.url = article_url
        article.description = description
        if image_url:
            article.image_url = image_url

        return article

    except Exception as e:
        print(f"Error crawling article {article.url}: {e}")
        return article
