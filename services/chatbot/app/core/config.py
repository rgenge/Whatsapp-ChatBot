from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv
import os
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv("../.env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = ""
    API_V1_STR: str = ""
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    OPENAI_API_KEY: str = ""
    WHATSAPP_ACCESS_TOKEN: str =""
    WHATSAPP_VERIFY_TOKEN: str =""
    WHATSAPP_PHONE_NUMBER_ID: str =""

settings = Settings()
