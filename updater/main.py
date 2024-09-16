import time
from config import Config
from services import is_gnews_updated, update_db


def check_n_update():
    
    for country in Config.country_names:
        print(country)
        if is_gnews_updated(country):
            update_db(country)


def main():

    while True:
        
        check_n_update()
        time.sleep(60 * 60 * 1.0)        
    
if __name__ == "__main__":
    
    main()