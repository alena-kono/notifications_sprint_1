from functools import lru_cache

from jinja2 import Environment, FileSystemLoader

from src.settings.app import get_app_settings


settings = get_app_settings()


_loader = FileSystemLoader(settings.jinja2.template_folder)
_env = Environment(loader=_loader)


@lru_cache()
def get_template(template_name: str):
    return _env.get_template(template_name)
