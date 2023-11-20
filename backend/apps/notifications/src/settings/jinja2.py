from pathlib import Path

from pydantic_settings import SettingsConfigDict

from src.settings.base import BaseAppSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Jinja2Settings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="jinja2_")

    template_folder: Path = BASE_DIR / "templates"
