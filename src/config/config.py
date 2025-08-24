from dataclasses import dataclass

from environs import Env


@dataclass
class DataBaseConfig:
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_name: str


@dataclass
class App:
    host: str
    port: int


@dataclass
class Config:
    app: App
    db: DataBaseConfig


def load_config(path: str = None) -> str:
    env = Env()
    env.read_env()
    
    return Config(
        db=DataBaseConfig(
            database_user=env("DB_USER"),
            database_password=env("DB_PASSWORD"),
            database_host=env("DB_HOST"),
            database_port=env("DB_PORT"),
            database_name=env("DB_NAME"),
        ),
        app=App(host=env("HOST"), port=int(env("PORT")))
    )
