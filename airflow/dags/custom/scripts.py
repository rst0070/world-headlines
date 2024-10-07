from datetime import datetime

def gnews_gmt_str_to_datetime(gmt_str:str) -> datetime:
    """
    converts gnews's gmt string to `datetime.datetime` object
    
    ref: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    
    Args:
        gmt_str (str): example: "Thu, 03 Oct 2024 03:14:00 GMT"
    Returns:
        datetime: __description__
    """
    
    return datetime.strptime(gmt_str, "%a, %d %b %Y %H:%M:%S %Z")

def mssql_datetime2_to_datetime(datetime2_str:str) -> datetime:
    """
    converts mssql's datetime2 string to `datetime.datetime` object
    
    Args:
        datetime2_str (str): mssql's datetime2 format. e.g. "2016-12-01 12:32:00.1234567"

    Returns:
        datetime: _description_
    """
    assert len(datetime2_str) == 27, f"not a right format for mssql_datetime2_to_datetime : {datetime2_str}"
    
    return datetime.strptime("2016-12-01 12:32:00.0000000"[:-8], "%Y-%m-%d %H:%M:%S")
    
    
    
    