from email.message import EmailMessage

from aiosmtplib import SMTP, SMTPException
from faststream import Depends
from loguru import logger

from email_worker.configs.smpt import get_smtp_server
from email_worker.email_senders.interface import IEmailSender


# async context manager?
class EmailSender(IEmailSender):
    def __init__(self, smpt_client: SMTP) -> None:
        self.smpt_client = smpt_client

    async def send(self, email_message: EmailMessage) -> None:
        from_email = email_message["From"]
        to_emails = email_message["To"].split(",")
        message = email_message.as_string()

        try:
            async with self.smpt_client as smpt_client:
                await smpt_client.sendmail(from_email, to_emails, message)

        except SMTPException as exc:
            reason = f"{type(exc).__name__}: {exc}"
            logger.error(f"Could send the email. {reason}")

        else:
            logger.debug("The email has been successfully delivered!")

        finally:
            smpt_client.close()


def get_email_sender(
    smpt_client: SMTP = Depends(get_smtp_server),
) -> EmailSender:
    return EmailSender(smpt_client)
