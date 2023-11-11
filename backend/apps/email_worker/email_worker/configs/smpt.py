from aiosmtplib import SMTP

from email_worker.configs.settings import get_settings

settings = get_settings()


def get_smtp_server() -> SMTP:
    return SMTP(hostname=settings.smtp_host, port=settings.smtp_port)
