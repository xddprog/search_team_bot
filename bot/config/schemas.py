from dataclasses import dataclass


@dataclass
class BotConfig:
    BOT_TOKEN: str


@dataclass
class DatabaseConfig:
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
