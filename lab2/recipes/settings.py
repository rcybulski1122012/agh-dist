from pydantic_core import Url
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FOOD_API_KEY: str
    FOOD_API_URL: Url
    DEEPL_API_KEY: str
    DEEPL_API_URL: Url
    TARGET_LANGUAGE: str = "pl"


settings = Settings()
