# world-headlines
__world-headlines__ is a service, providing headline news from various countries. 
You can get to the web service [here: world-headlines.github.io](https://world-headlines.github.io).  
  
Especially this repository's code does automatic updating process for world-headlines service using apache aiflow. 

## Overview of the updating process
<img src="overview.png" width="600px"/>  

- Default scheduling term is a hour
- Google news provides rss news information with url starting like `news.google.com/rss`

## DB design


## Country codes
Entire world-headlines system uses country codes to distinguish country dependent information.  
[ISO_3166-1_alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) provides country identity as 2-characters. This service use this, but small letters.  


## TO DO
- set auto commit with sqlalchemy
    - with `autocommit=False`, deadlock happens.
    - I thought it is not needed because the SQL Server is autocommit default.
    - https://stackoverflow.com/questions/41900988/sql-server-pyodbc-and-deadlock-errors
- Figure out how to update db even some country's headline is not updated
    - with the system now, the whole update process need all gnews headlines are updated.
    - need to use `Trigger Rule`
- use tqdm for logging