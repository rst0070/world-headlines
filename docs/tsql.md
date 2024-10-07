## date & time types
official document says "Avoid using datetime for new work. Instead, use the time, date, datetime2, and datetimeoffset data types. These types align with the SQL Standard, and are more portable. time, datetime2 and datetimeoffset provide more seconds precision."  

## GRANT to user
```sql
GRANT INSERT,SELECT,UPDATE,DELETE ON OBJECT::dbo.TEST_TABLE TO wh_updater;
```

## `GO` statement
[stack overflow](https://stackoverflow.com/questions/2299249/what-is-the-use-of-go-in-sql-server-management-studio-transact-sql)  

## MSSQL ODBC
To use mssql odbc, check [this](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15&tabs=ubuntu18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline).  
Need to install odbc.  

## `text`
It is depreciated. so use another type. the `text` type even cannot be compared with `=` operator.  
