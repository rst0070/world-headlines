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

## Python unit testing with `pytest`
I felt that not using test could faster the coding process, but if the needs and some data structure is changed, using automated testing could faster the coding process.  
  
__Categories of Testing__  
- UI test/ End-To-End test
- Integration Test
- unit test
  
unit test just needs part of code. so that, it tests segment of code. and it looks like `pytest` library is popular one rather than official `unittest` library. 

### Get Started

__Run test__  
In a directory, if you run `pytest`, then it automatically detects python file starting with `test_`, and run that python script regarding its a test code.   
- pytest regards 
    - python file starting with `test_` as test code
    - function starting with `test_` as unit test
    - class starting with `Test` as a group of unit tests
- other methods are [here](https://docs.pytest.org/en/stable/how-to/usage.html#usage)


__Group of Unit test__  
Every unit test (function) has unique instance of the class so functions inside test class are isolated.  
for example, `test_two` of the code below will fail.  
```python
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
```
  
### Fixtures
In testing, a fixture provides a defined, reliable and consistent context for the tests. This could include environment (for example a database configured with known parameters) or content (such as a dataset).  
Example below.
```python
from __future__ import annotations

import pytest


@pytest.fixture
def order():
    return []


@pytest.fixture
def outer(order, inner):
    order.append("outer")


class TestOne:
    @pytest.fixture
    def inner(self, order):
        order.append("one")

    def test_order(self, order, outer):
        assert order == ["one", "outer"]


class TestTwo:
    @pytest.fixture
    def inner(self, order):
        order.append("two")

    def test_order(self, order, outer):
        assert order == ["two", "outer"]
```
