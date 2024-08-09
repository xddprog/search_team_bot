from environs import Env

from config.schemas import BotConfig, DatabaseConfig


def get_bot_config() -> BotConfig:
    env = Env()
    env.read_env()

    return BotConfig(
        BOT_TOKEN=env.str('BOT_TOKEN')
    )


def get_database_config() -> DatabaseConfig:
    env = Env()
    env.read_env()

    return DatabaseConfig(
        db_host=env.str('DB_HOST'),
        db_pass=env.str('DB_PASS'),
        db_user=env.str('DB_USER'),
        db_name=env.str('DB_NAME'),
        db_port=env.str('DB_PORT')
    )


def load_geoapify_token() -> str:
    env = Env()
    env.read_env()
    return env("GEOAPIFY_KEY")
