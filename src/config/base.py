from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.dirs import BASE_DIR


class BaseApplicationConfig(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )
