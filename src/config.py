from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv(find_dotenv(), override=True)


class Config(BaseSettings):
    POSTGRES_URL: PostgresDsn


config = Config()

__all__ = ["config"]
