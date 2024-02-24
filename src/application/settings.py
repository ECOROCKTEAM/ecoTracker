import os

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    CONFIGURE_JSON_PATH: str = ""

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

    @validator("CONFIGURE_JSON_PATH")
    def conf_json_path_exist(cls, v: str) -> str:
        if not os.path.exists(v):
            raise Exception(f"Please create file {v} for setup app!")
        return v


class SettingsDev(Settings):
    CONFIGURE_JSON_PATH: str = "develop.json"

    class Config:
        env_file = "dev.env"


class SettingsTest(Settings):
    CONFIGURE_JSON_PATH: str = "test.json"

    class Config:
        env_file = "test.env"


class SettingsProd(Settings):
    CONFIGURE_JSON_PATH: str = "prod.json"

    class Config:
        env_file = "prod.env"


config = dict(dev=SettingsDev, test=SettingsTest, prod=SettingsProd)
settings: Settings = config[os.environ.get("APP_ENV", "dev").lower()]()  # type: ignore
