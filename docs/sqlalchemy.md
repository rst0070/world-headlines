# `sqlalchemy`

## absolute path vs real path for connection
[stack overflow](https://stackoverflow.com/questions/18208492/sqlalchemy-exc-operationalerror-operationalerror-unable-to-open-database-file).  
__Example__  
- absolute path : `sqlite:////absolute/path/to/file.db`
- real path : `sqlite:///relative/path/to/file.db`

## `Null` data from DB
If sqlalchemy gets null data, what the python data type would be?  
The answer is `None` type.  

## `pyobdc` cannot find `libodbc.so.2`

[github](https://github.com/mkleehammer/pyodbc/issues/1133#issuecomment-1869123055).  
- when I tried to use `pyodbc` for sqlalchemy (with wsl terminal)
- got error like `libodbc.so.2: cannot open shared object file: No such file or directory`
- The issue solved with below commands
```sh
sudo apt remove libodbc2
sudo apt install libodbc2
```

## Run sql file
```python
from sqlalchemy import create_engine
from sqlalchemy import text
# or from sqlalchemy.sql import text

engine = create_engine('mysql://{USR}:{PWD}@localhost:3306/db', echo=True)

with engine.connect() as con:
    with open("src/models/query.sql") as file:
        query = text(file.read())
        con.execute(query)
```

## Running sql file
you can use something like below.
```python
from sqlalchemy import create_engine, text

...
engine = create_engine("....")
with open(os.path.join(os.path.dirname(__file__), 'mssql_set_up.sql'), 'r') as file:
    with engine.begin() as conn:
        query = text(file.read())
```

## Create DB : `sqlalchemy-utils`
I couldn't use `CREATE DATABASE` statement inside sql file for running that.  
But you can use `sqlalchemy-utils` library to solve that.  
```python
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("postgresql://localhost/mydb")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))
```