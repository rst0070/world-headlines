# Headline RSS
- US(`EN-US`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3
- China(`ZH`)
    - https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3
- German(`DE`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3
- Japan(`JA`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3
- India(`EN-GB`)
    - https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?ceid=IN:en&oc=3
- United Kingdom(`EN-GB`)
    - https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3
- franch(`FR`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3
- Russia(`RU`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3
- Korean(`KO`)
    - https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3




# News image
If follow the news site, you can find main image by `head > meta(property="og:image")`


# Note

```python
 
    @classmethod
    def getTranslatedNewsArticlesByCountryAndLangauge(country_name:str, target_lang:str) -> List[NewsArticle]:
        """
        returns translated news articles by headline country and target language.
        It needs subquery to fetch between info of original article and translated article.
        """
        
        res = DBRepository._cursor.execute(
            f"""
            SELECT 
                o.url, o.country, o.source, t.title, o.image_url, o.publish_date
            FROM 
                (
                    SELECT 
                        url, country, source, image_url, publish_date 
                    FROM
                        NEWS_ARTICLES
                    WHERE
                        country = '{country_name}'
                ) o 
                INNER JOIN
                (
                    SELECT
                        url, title
                    FROM
                        TRANSLATED_ARTICLES
                    WHERE
                        language = '{target_lang}'
                ) t
                ON
                o.url = t.url
            """
        )
        
        articles: List[NewsArticle] = []
        
        for data_t in res.fetchall:
            articles.append(
                NewsArticle(
                    url = data_t[0],
                    country=data_t[1], 
                    source=data_t[2],
                    title=data_t[3],
                    image_url=data_t[4],
                    publish_date=data_t[5]
                )
            )
        
        return articles
```
