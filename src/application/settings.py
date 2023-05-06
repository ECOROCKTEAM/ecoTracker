import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    class Config:
        env_file = ".env"


class SettingsDev(Settings):
    class Config:
        env_file = "dev.env"


class SettingsTest(Settings):
    class Config:
        env_file = "test.env"


config = dict(dev=SettingsDev, test=SettingsTest)
settings: Settings = config[os.environ.get("APP_ENV", "dev").lower()]()  # type: ignore
