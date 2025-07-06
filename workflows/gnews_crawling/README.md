# Steps
1. extract gnews rrs
2. extract details by crawling each news
3. transform: type, translate into english
3. load to postgres


docker build -t harbor.rst0070.com/world-headlines/gnews-crawling:latest .