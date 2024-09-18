# Headline RSS

Things to know.
- url cannot be unique in NEWS_ARTICLES table. (sometimes the article is copied over countries)
- translation costs a lot. so try to translate from user's browser
- you cannot get original url of news article by just using request api.
    - you need to use browser crawling. so that, to get url used in this app, browser crawling is neccesary
    - it means that you cannot determine which article to crawl before crawl it

## Google News Headline rss links
check `updater/db_init.sql`  

## News image
If follow the news site, you can find main image by `head > meta(property="og:image")`


## Webapp

https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts