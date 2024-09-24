import time
import os
import pygit2
import sqlite3
from updater import load_configs, check_n_update
from config import Config

PATH_PRODUCT_REPO = os.path.join(os.getcwd(), "world-headlines.github.io")
STR_CLONE_PRODUCT_REPO = "https://world-headlines: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@github.com/world-headlines/world-headlines.github.io.git"

def pull_product_repo():
    """
    
    """
    print("pull_product_repo() is started ----------------------------------------------------")
    
    repo: pygit2.Repository = None
    if not os.path.isdir(PATH_PRODUCT_REPO):
        os.system(
        f"""mkdir {PATH_PRODUCT_REPO} && \
            git clone {STR_CLONE_PRODUCT_REPO} {PATH_PRODUCT_REPO}
        """)
    
    os.system(f"""cd {PATH_PRODUCT_REPO} && \
              git pull origin main              
              """)

    print("fetch_product_repo() is completed ----------------------------------------------------")
    
def set_db_conn():
    db_path = os.path.join(PATH_PRODUCT_REPO, 'world_headline.db')
    Config.db_connection = sqlite3.connect(db_path)
    
def update_product_repo():
    print("update_product_repo() is started ----------------------------------------------------")
    
    os.system(
        f"""cd {PATH_PRODUCT_REPO} && \
            git add . && \
            git commit -m "db updated" && \
            git push origin main
        """)
    
    print("update_product_repo() is completed ----------------------------------------------------")
    
def main():
    
    while True:
        pull_product_repo()
        set_db_conn()
        
        load_configs()
        check_n_update() 
        
        update_product_repo()
        
        print(f"sleep for...")
        time.sleep(60 * 60 * 1.0) 
    
    
if __name__ == "__main__":
    main()