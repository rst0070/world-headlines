---------------------- DATABASE
----------------------
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'world_headlines')
BEGIN
	CREATE DATABASE world_headlines
END;
USE world_headlines;
---------------------- Create TABLE
----------------------

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='HEADLINE' AND xtype='U')
BEGIN
	CREATE TABLE HEADLINE (
		country_code nvarchar(2) primary key,
		country_name nvarchar(60), -- longest eng name of country is 56 long. 4 more character, in case.
		url nvarchar(MAX),
		last_update datetime2
	)
END;

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='HEADLINE_ARTICLES' AND xtype='U')
BEGIN
	CREATE TABLE HEADLINE_ARTICLES (
		row_id int IDENTITY(1, 1) primary key,
		country_code nvarchar(2) not null,
		url nvarchar(MAX),
		title nvarchar(MAX),
		description nvarchar(MAX),
		image_url nvarchar(MAX),
		publish_date datetime2,
		source nvarchar(MAX),
		foreign key (country_code) references HEADLINE(country_code)
	)
END;

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CRAWLED_ARTICLES' AND xtype='U')
BEGIN
	CREATE TABLE CRAWLED_ARTICLES (
		row_id int IDENTITY(1, 1) primary key,
		country_code nvarchar(2) not null,
		url nvarchar(MAX),
		title nvarchar(MAX),
		description nvarchar(MAX),
		image_url nvarchar(MAX),
		publish_date datetime2,
		source nvarchar(MAX),
		foreign key (country_code) references HEADLINE(country_code)
	)
END;
---------------------- Create User & Grant permission
----------------------

IF NOT EXISTS (SELECT * FROM master.sys.server_principals WHERE name = 'wh_updater')
BEGIN
    CREATE LOGIN [wh_updater] WITH PASSWORD = N'WorldHeadlinesUpdater99!'
END;

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'wh_updater')
BEGIN
    CREATE USER [wh_updater] FOR LOGIN [wh_updater]
END;

GRANT INSERT,SELECT,UPDATE,DELETE ON OBJECT::dbo.HEADLINE TO wh_updater;
GRANT INSERT,SELECT,UPDATE,DELETE ON OBJECT::dbo.HEADLINE_ARTICLES TO wh_updater;
GRANT INSERT,SELECT,UPDATE,DELETE ON OBJECT::dbo.CRAWLED_ARTICLES TO wh_updater;
---------------------- Insert data into HEADLINE
----------------------
-- check below for language code
-- https://cloud.google.com/translate/docs/languages?hl=ko

INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('United States', 'us', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?ceid=US:en&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('China', 'cn', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVU5PR2dKRFRpZ0FQAQ?ceid=CN:zh-Hans&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('India', 'in', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtaHBHZ0pKVGlnQVAB?ceid=IN:hi&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('German', 'de', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtUmxHZ0pFUlNnQVAB?ceid=DE:de&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Franch', 'fr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtWnlHZ0pHVWlnQVAB?ceid=FR:fr&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Japan', 'jp', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtcGhHZ0pLVUNnQVAB?ceid=JP:ja&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Brasil', 'br', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?ceid=BR:pt-419&oc=3&hl=pt-BR&gl=BR');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Russia', 'ru', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuSjFHZ0pTVlNnQVAB?ceid=RU:ru&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Korea', 'kr', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtdHZHZ0pMVWlnQVAB?ceid=KR:ko&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('United Kingdom', 'gb', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
    VALUES ('Taiwan', 'tw', 'https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?ceid=TW:zh-Hant&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
	VALUES ('Israel', 'il', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtbDNHZ0pKVENnQVAB?ceid=IL:he&oc=3');
INSERT INTO HEADLINE (country_name, country_code, url)
	VALUES ('Lebanon', 'lb', 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtRnlHZ0pNUWlnQVAB?ceid=LB:ar&oc=3');