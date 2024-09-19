CREATE TABLE HEADLINE (
    country text,
    country_code text,
    src_lang text,
    url text,
    last_update text,
    primary key(country)
);

CREATE TABLE NEWS_ARTICLES (
    row_id integer primary key,
    url text,
    country text,
    source text,
    title text,
    description text,
    image_url text,
    publish_date text,
    src_lang text,
    foreign key (country) references HEADLINE(country)
);

-- check below for language code
-- https://cloud.google.com/translate/docs/languages?hl=ko

INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('United States', 'US', 'en', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('China', 'CN', 'zh', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('India', 'IN', 'en', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?ceid=IN:en&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('German', 'DE', 'de', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Franch', 'FR', 'fr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Japan', 'JP', 'ja', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Brasil', 'BR', 'pt', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?ceid=BR:pt-419&oc=3&hl=pt-BR&gl=BR', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Russia', 'RU', 'ru', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Korea', 'KR', 'ko', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('United Kingdom', 'GB', 'en', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3', 'none');
INSERT INTO HEADLINE (country, country_code, src_lang, url, last_update)
    VALUES ('Taiwan', 'TW', 'zh-TW','https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?ceid=TW:zh-Hant&oc=3', 'none');
