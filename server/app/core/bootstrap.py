import os
from dotenv import load_dotenv as dotenv_load


def load_environment():
    env_file = os.getenv("ENV_FILE", ".env")
    dotenv_load(env_file)