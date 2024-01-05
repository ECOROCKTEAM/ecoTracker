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

    FIREBASE_SECRET_PATH: str
    FIREBASE_APP_NAME: str

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


class SettingsProd(Settings):
    class Config:
        env_file = "prod.env"


config = dict(dev=SettingsDev, test=SettingsTest, prod=SettingsProd)
settings: Settings = config[os.environ.get("APP_ENV", "dev").lower()]()  # type: ignore
