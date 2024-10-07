# world-headlines-airflow
This is for automating update process of [world-headlines](https://world-headlines.github.io).  
First version of updater was vanila python code, but because of that the process gets more need for monitoring, 
I decided to migrate the process to apache airflow. 

  
## DB design
__Tables__  
- `HEADLINE`
    - country: `text`
    - country_code: `text`
        - for webpages identity
    - url: `text`
    - last_update: `datetime2`
- `HEADLINE_ARTICLES`
    - row_id
        - pk - because unpreditable situation can be caused if you use article's url as pk
        - [identity in mssql](https://learn.microsoft.com/ko-kr/sql/t-sql/statements/create-table-transact-sql-identity-property?view=sql-server-ver16)
    - country_code: `text`
    - source: `text`
    - title: `text`
    - description: `text`
    - image_url: `text`
    - publish_date: `datetime2`
        - UTC(==GMT) based
- `CRAWLED_ARTICLES`
    - same as `HEADLINE_ARTICLES`

### Country codes
[ISO_3166-1_alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) provides country identity as 2-characters.  
We will use this, but small letters.  

## Dag design

- get metadata (countries, urls)
- task_group by country
    - sensor checking if update exists
        - (need: gnews_url, identity of country)
    - crawl headline into `CRAWLED_ARTICLES` 
        - (need: gnews_url, identity of country)
    - delete old articles in `HEADLINE_ARTICLES` 
        - (need: identity of country)
    - insert new articles into `HEADLINE_ARTICLES` 
        - (need: identity of country)
    - delete crawled articles
- copy DB data to local storage (e.g. sqlite)
- pull & update production repo of static webpage