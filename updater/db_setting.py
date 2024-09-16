import sqlite3

connection = sqlite3.connect('world_headline.db')
cursor = connection.cursor()

COUNTRY_HEADLINE_URL = {
    'United States' : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3',
    'China'         : 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3',
    'German'        : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3',
    'Japan'         : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3',
    'India'         : 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?ceid=IN:en&oc=3',
    'United Kingdom': 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3',
    'Franch'        : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3',
    'Russia'        : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3',
    'Korea'        : 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3'
}

src_lang_by_counrty = {
            'United States' : 'EN',
            'China'         : 'ZH',
            'German'        : 'DE',
            'Japan'         : 'JA',
            'India'         : 'EN',
            'United Kingdom': 'EN',
            'Franch'        : 'FR',
            'Russia'        : 'RU',
            'Korea'         : 'KO'
        }
    
target_lang_by_country = {
            'United States' : 'EN-US',
            'China'         : 'ZH',
            'German'        : 'DE',
            'Japan'         : 'JA',
            'India'         : 'EN-GB',
            'United Kingdom': 'EN-GB',
            'Franch'        : 'FR',
            'Russia'        : 'RU',
            'Korea'         : 'KO'                       
        }

cursor.execute("""
    CREATE TABLE HEADLINE (
        country text,
        src_lang text,
        target_lang text,
        url text,
        last_update text,
        primary key(country)
    ); 
""")

cursor.execute("""    
    CREATE TABLE NEWS_ARTICLES (
        url text,
        country text,
        source text,
        title text,
        image_url text,
        publish_date text,
        src_lang text,
        target_lang text,
        primary key (url, target_lang),
        foreign key (country) references HEADLINE(country)
    );            
""")

for country in COUNTRY_HEADLINE_URL.keys():
    
    src_lang = src_lang_by_counrty[country]
    target_lang = target_lang_by_country[country]
    url = COUNTRY_HEADLINE_URL[country]
    
    cursor.execute(f"""
                   INSERT INTO HEADLINE (country, src_lang, target_lang, url, last_update)
                   VALUES ('{country}', '{src_lang}','{target_lang}', '{url}', 'none')
                   """)
    
connection.commit()
connection.close()