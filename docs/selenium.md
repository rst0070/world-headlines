# Selenium

## geckodriver error
[stack overflow](https://stackoverflow.com/questions/46682841/selenium-common-exceptions-webdriverexception-message-geckodriver-executable).  
  
permission for executing something related to webdriver(geckodriver).  
But the problem is that if i specify the location of firefox driver, it makes unpretty dependency.  
so I just changed permission of `/home/airflow` because the geckodriver is inside it.  
I just added below line in `Dockerfile`
```Dockerfile
RUN chmod -R 777 /home/airflow
```