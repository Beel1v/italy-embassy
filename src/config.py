import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_project_path() -> Path:
    path = Path(find_dotenv()).parent
    return path


def get_tg_token() -> str:
    return os.environ["TG_TOKEN"]


def get_tg_subscribed_users() -> list[int]:
    return [int(s) for s in os.environ["TG_SUBSCRIBED_USERS"].split(",") if len(s) > 0]


def get_prenotami_user() -> str:
    return os.environ["PRENOTAMI_USER"]


def get_prenotami_password() -> str:
    return os.environ["PRENOTAMI_PASSWORD"]
