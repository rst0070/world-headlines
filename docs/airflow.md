
## folder structure

### Version 1
For example, We can define the folder structure like below.  
```
- dags
    - dag1.py
- plugins
    - models
        - __init__.py
        - data_model.py
    - hooks
        - __init__.py
        - db_hook.py
    - __init__.py
- tests
    
```

__`./plugins`__  
It's good to place custom scripts inside the `./plugins` folder. The airflow will find all scripts inside it. 
From dag scripts, you don't need to specify the `plugins` as module, because the airflow will find it. 
However, you need to specify the `plugins` as module if you use the module inside `./plugins`
  
From `dags/dag1.py` you just need `from models.data_model import ...` for importing `data_model.py`. 
However, from `plugins/hooks/db_hook.py`, you need `from plugins.models.data_model import ...`.  

### Version 2
I tried version 1, but the problem was that the airflow doesn't reload scripts inside `plugins` folder.  so I tried another way.  
```
- dags
    - dag1.py
    - custom
        - hooks.py
        - operators.py
        - sensors.py
        - scripts.py
        - __init__.py
- tests
```
With testing, I checked that the airflow reloads scripts under `dags/custom` if some change is occurred.  

## config

### reloading....
https://stackoverflow.com/questions/51208550/airflow-how-to-reload-operators-and-plugins

### `airflow.cfg` file
__how to use the file with docker container?__  
you can set the file at local, and import that.  
```yaml
- volumes:
  - ./config/airflow.cfg:/opt/airflow/airflow.cfg
```  

## Plugins

### when plugins are reloaded?
https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html#when-are-plugins-re-loaded

## xcom between custom operators
example is below

__custom operator__  
```python
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MyStringListOperator(BaseOperator):

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(MyStringListOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        # Example list of strings
        string_list = ["apple", "banana", "cherry", "date"]
        # Return this list to store in XCom
        return string_list
```

__getting xcom value__  
```python
from airflow import DAG
from datetime import datetime
from my_custom_operators import MyStringListOperator  # Make sure to import the custom operator
from airflow.operators.python_operator import PythonOperator

def print_string_list(ti):
    string_list = ti.xcom_pull(task_ids='generate_strings')  # Pull XCom result
    for string in string_list:
        print(f"String: {string}")

with DAG(
    dag_id='example_custom_operator_dag',
    start_date=datetime(2023, 10, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task using the custom operator to generate the string list
    generate_strings = MyStringListOperator(
        task_id='generate_strings'
    )

    # Task using PythonOperator to print the string list from XCom
    print_strings = PythonOperator(
        task_id='print_strings',
        python_callable=print_string_list
    )

    # Set the task dependencies
    generate_strings >> print_strings
```

## [.airflowignore](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#airflowignore)

## Is it possible to create tasks inside task?
I tried to create task dynamically inside `execute` method of custom operator, but it didn't create task and it was like just executing method (it didnt appear to dag visualization).  
With this experience and *best practice* for airflow, creating task inside task is not a good idea.  
better to make task's code dependent on db not on other tasks.  
  
dynamically creating task inside task group can be alternative! (in terms of dynamical creating)

## where code initiating hook should be placed inside custom hook?
Best practice: Initialize the hook `poke` the first time the sensor "pokes," and then cache it in a local variable so that subsequent pokes use the same hook. This avoids the overhead of reconnecting multiple times while ensuring the hook is created only when needed.  
  

## Test
https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag

https://medium.com/wbaa/datas-inferno-7-circles-of-data-testing-hell-with-airflow-cef4adff58d8

https://medium.com/@montadhar/apache-airflow-testing-guide-7956a3f4bbf5#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjI4YTQyMWNhZmJlM2RkODg5MjcxZGY5MDBmNGJiZjE2ZGI1YzI0ZDQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDA2NjcyNTU5NDM5NzM1MTY2ODEiLCJlbWFpbCI6Imt3YjA3MTFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5iZiI6MTcyODAxODE4NCwibmFtZSI6IndvbmJpbiBLaW0iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSlA3QWVqQU9sYnJOSGo5ZkEyVjAxRDZxRXBUWkRLNTE2bEhLbHcwelFIY0hzXzJnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IndvbmJpbiIsImZhbWlseV9uYW1lIjoiS2ltIiwiaWF0IjoxNzI4MDE4NDg0LCJleHAiOjE3MjgwMjIwODQsImp0aSI6IjA3MDFmNWQ2YzBlOTU3MDZkZWM2M2E3OWU4YTVjYzRiZGUzM2NjZDgifQ.Nsjz8r25K2R1LmZd7WM8xq0ChLaXqkTWv2xfcUgugigC2b2kUwBq9ZwC3n7ZQb9mZOfPVUiwmK6cupYiExDBiQ6VCG5WTReiBZiNK6wEaA3uua8-yoXAhMekW8YYz_h7cGpyAmCZhSAACSCryEYIW3aVY-VhJdj2evaGVQDQOM8fzIrrdorlaUNlqlDm55AYh-W02dF3F0Pi1ZX6CTRYB9tBvK0Bzja8rcXDYVffZQjTk90yorZCiHGMztRh87mj8w1ybiwltva8nmOscfzqbndRlnfKa8r2OJMxQHBJaneoJHp6N8xVjA-01fknrPkB6xN85wO0BWpMg1Mlg5QPww

## Unit Testing
*[How to unit test Airflow components locally without the need for a prodution system?](https://xebia.com/blog/testing-and-debugging-apache-airflow/?utm_source=GDD&utm_medium=redirect&utm_campaign=consolidation&utm_content=xebia.com-blog-testing-debugging-apache-airflow-)*  

### Setting ENV paths
To make pytest codes find my `plugins` codes, I added below code into `conftest.py`.  
```python
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../plugins')))
```
it reads scripts in `test/../plugins`.  

### Pytest Airflow fixtures & Helpers
__Goals__  
1. Use dummy DAG for test cases by `fixture`
    - `fixture` : object which can be passed to test functions as input arguments
    - Testing cannot be decoupled from running a DAG
        - because airflow jobs always run in the context of a DAG
        - so that, we will make temporary DAG only for the task    
2. Make convetion for running task by registering the process to [`pytest-helpers-namespace`](https://github.com/saltstack/pytest-helpers-namespace)  
    - asd
    - specific process is needed for registering task to the dummy DAG
    - install it by `pip install pytest-helpers-namespace`  
  

__test/conftest.py__  
```python
import datetime
import pytest
from airflow import DAG

pytest_plugins = ["helpers_namespace"]

@pytest.fixture
def test_dag():
    return DAG(
        "test_dag",
        default_args={'owner': 'airflow', 'start_date': datetime.datetime(2024, 10, 4)},
        schedule_interval=datetime.timedelta(days=1),
    )


@pytest.helpers.register
def run_task(task, dag):
    dag.clear()
    task.run(
        start_date=dag.default_args["start_date"],
        end_date=dag.default_args["start_date"],
    )
```

### Mocking Airflow
We can use `pytest-mock` package for mocking. 
Example code is below.
```python
from datetime import datetime

import pytest
from airflow.hooks.base_hook import BaseHook
from airflow.models import Connection
from airflow.operators.http_operator import SimpleHttpOperator

def test_simple_http_operator(test_dag, mocker):
    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(schema="https", host="api.sunrise-sunset.org"),
    )

    def _check_light(sunset_sunrise_response):
        results = sunset_sunrise_response.json()["results"]
        sunrise = datetime.strptime(results["sunrise"][:-6], "%Y-%m-%dT%H:%M:%S")
        sunset = datetime.strptime(results["sunset"][:-6], "%Y-%m-%dT%H:%M:%S")

        if sunrise  datetime.utcnow()  sunset:
            print("It is light!")
        else:
            print("It is dark!")

        return True

    is_it_light = SimpleHttpOperator(
        task_id="is_it_light",
        http_conn_id="random_name",
        endpoint="json",
        method="GET",
        data={"lat": "52.370216", "lng": "4.895168", "formatted": "0"},
        response_check=_check_light,
        dag=test_dag,
    )

    pytest.helpers.run_task(task=is_it_light, dag=test_dag)
```
__Feature of the code__  
- `mocker.path....` - it patches the parameterized object to new object in the application context.
    - in the above case, `BaseHook.get_connection` method is replaced as `return_value` parameter of the `mocker.patch.object`  

### Mocking external systems  
We can run docker container for mocking external system.  
For that, we need library `[pytest-docker-tools](https://pypi.org/project/pytest-docker-tools/)`.  
Below example `conftest.py` code runs SQL Server container and creates it's credentials fixture.  
```python
from collections import namedtuple
import pytest
from pytest_docker_tools import container, fetch

@pytest.fixture
def mssql_conn_str():
    return "mssql+pyodbc://sa:StrongPassword99!@localhost:1433/master?driver=ODBC+Driver+17+for+SQL+Server"
    
mssql_image = fetch(repository = 'mcr.microsoft.com/mssql/server:2022-latest')

mssql = container(
    image = "{mssql_image.id}",
    environment = {
        'MSSQL_PID':'developer',
        'ACCEPT_EULA':'Y',
        'MSSQL_SA_PASSWORD':'StrongPassword99!'
    },
    ports={'1433':'1433'},
    volumes={
        os.path.dirname(__file__):'/var/opt/mssql/scripts'
    },
    command= '/bin/bash -c "/opt/mssql-tools/bin/sqlcmd -S sqlserver -U sa -P StrongPassword99! -d master -i /var/opt/mssql/scripts/mssql_init.sql"'
)
```
I was trying to use docker container with the code above, but i got me bunch of errors of logging in. 
So im just gonna use external DB for this time. 
I hope i can find the way next time i try.  

## Running on windows
It needs wsl, and if some error happens, think about setting env val `AIRFLOW_HOME=~/airflow`.  

[doc](https://vivekjadhavr.medium.com/how-to-easily-install-apache-airflow-on-windows-6f041c9c80d2)