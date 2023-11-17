from functools import lru_cache

from jinja2 import Environment, FileSystemLoader

from email_worker.configs.settings import get_settings

settings = get_settings()


_loader = FileSystemLoader(settings.template_folder)
_env = Environment(loader=_loader)


@lru_cache()
def get_template(template_name: str):
    return _env.get_template(template_name)
