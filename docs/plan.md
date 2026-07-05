# Upgrade plan of world-headlines - 08/06/25

## Current state

Now world-headlines service provides news articles from several countries. 
It uses google news rss feed to get urls to original news articles, and crawls each news article.
Additionally translate and extract keywords (into eng) leveraging LLM.
  
## What new features we want?

The current service only provides existing news articles, but we guess generative ai era requires us to generate new information leveraging source data.  
  
In our case, just like our moto: providing various perspectives, we can generate analysis about common topic with different perspectives around world. For example, "about trump tariff, japan news papers say blah blah while us news papers sya blah blah."  
  
## But the problem is the way to do it

- To find common topic
    - maybe we can explore algorithms like frequent item set
    - but the topic should be scattered on different countries not only one country
- To cluster articles
    - use common topic
    - need to consider how to make sure variousness between articles
    - need to consider metric for expressing importance between articles
- To leverage existing knowledge
    - now our system retrieves new information by scheduled crawling
    - not only the fresh information, but it is good to leverage existing knowledge from past news articles
    - maybe need to consider knowledge base system