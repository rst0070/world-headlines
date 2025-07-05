-- Create DATABASE
CREATE EXTENSION IF NOT EXISTS dblink;

DO $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'world_headlines') THEN
		PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE world_headlines');
	END IF;
END $$;

\c world_headlines;
---------------------- Create TABLE
----------------------

CREATE TABLE IF NOT EXISTS GNEWS_HEADLINE(
	country_code  char(2) primary key,
	country_name  text,
	url text,
	last_update timestamp
);

CREATE TABLE IF NOT EXISTS GNEWS_ARTICLES(
	country_code char(2),
	url text,
	title text,
	description text,
	image_url text,
	publish_date timestamp,
	source text,

	en_title text NULL,
	en_description text NULL,
	en_topics text[],
	en_keywords text[],

	-- primary key (country_code, url),
	foreign key (country_code) references GNEWS_HEADLINE(country_code)
)PARTITION BY LIST(date_trunc('day', publish_date));

---------------------- Create User & Grant permission
----------------------
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'wh_updater') THEN
        CREATE USER wh_updater WITH PASSWORD 'wh_updater';
    END IF;
END
$$;

GRANT 
	INSERT,SELECT,UPDATE 
ON
	GNEWS_HEADLINE --,ARCHIVED_ARTICLES
TO 
	wh_updater;

GRANT 
	INSERT,SELECT,UPDATE,DELETE 
ON
	GNEWS_ARTICLES, GNEWS_HEADLINE
TO 
	wh_updater;
---------------------- Insert data into HEADLINE
----------------------
-- check below for language code
-- https://cloud.google.com/translate/docs/languages?hl=ko

INSERT INTO GNEWS_HEADLINE (country_name, country_code, url)
VALUES 
	('United States', 'us', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3'),
	('Korea', 'kr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3'),
	('China', 'cn', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3'),
	('India', 'in', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtaHBHZ0pKVGlnQVAB?ceid=IN:hi&oc=3'),
	('German', 'de', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3'),
	('Franch', 'fr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3'),
	('Japan', 'jp', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3'),
	('Brasil', 'br', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?ceid=BR:pt-419&oc=3&hl=pt-BR&gl=BR'),
	('Russia', 'ru', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3'),
	('United Kingdom', 'gb', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3'),
	('Taiwan', 'tw', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?ceid=TW:zh-Hant&oc=3'),
	('Israel', 'il', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtbDNHZ0pKVENnQVAB?ceid=IL:he&oc=3'),
	('Lebanon', 'lb', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtRnlHZ0pNUWlnQVAB?ceid=LB:ar&oc=3');

-- CREATE TABLE HEADLINE_ARTICLES_us PARTITION OF HEADLINE_ARTICLES FOR VALUES IN ('us');
-- CREATE TABLE HEADLINE_ARTICLES_kr PARTITION OF HEADLINE_ARTICLES FOR VALUES IN ('kr');