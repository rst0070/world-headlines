# Headline RSS

Things to know.
- url cannot be unique in NEWS_ARTICLES table. (sometimes the actual url of an article is copied over news companies)
- translation costs a lot. so try to translate from user's browser
- you cannot get original url of news article by just using request api.
    - you need to use browser crawling. so that, to get url used in this app, browser crawling is neccesary
    - it means that you cannot determine which article to crawl before crawl it

## Google News 
  
__Google News rss feeds__  
check `updater/db_init.sql`  

__News images__  
If follow the news site, you can find main image by `head > meta(property="og:image")`

## To do 
1. design and code webapp
2. using jenkins to automate commit process to publish

## Webapp

https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts

### Note

__`app` router__  
The app router is new feature of version 13 of Next.js.  
so that im gonna try that.  

  
__Dynamic Routes: how to with app router?__  
[Document](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes). 
With `app` router, dynamic segment of folder name is provided.  

__ssr with dynamic routes__  
[Document](https://nextjs.org/docs/app/building-your-application/routing/dynamic-routes#generating-static-params). 

__Globally Accessible Variables__  
[Example](https://medium.com/@squashfold/creating-globally-accessible-variables-and-configuration-files-in-next-js-83811d9edc7e). 
  
__Image src__  
with src attribute in a `<Image>` tag, you need to the src information on the `next.config.mjs`.  
[Document](https://nextjs.org/docs/messages/next-image-unconfigured-host)