from dotenv import load_dotenv
import os


def load_env():
    if os.getenv("ENV") == "local":
        load_dotenv()
