import os
import smtplib
from email.message import EmailMessage
from typing import Dict

import jinja2
from fastapi.templating import Jinja2Templates

from core import settings
from core.fields import NotificationType
from core.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

templates = Jinja2Templates(directory="../templates/email")

templates_mapper = {
    NotificationType.new_user_invited: "invitation.html",
    NotificationType.friendly_reminder: "friendly_payment_reminder.html"
}

subjects = {
    NotificationType.new_user_invited: "You were invited.",
    NotificationType.friendly_reminder: "Payment reminder."
}


class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = EMAIL_FROM
        message['To'] = to
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if settings.EMAIL_USE_TLS:
            s.starttls()
        s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        s.send_message(message)
        s.quit()


async def send_notification(recipient: str, type: NotificationType, context: Dict):
    template = templates_mapper[type]

    path = os.path.join(settings.TEMPLATES_DIR, "email")
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    body = template.render(**context)

    subject = subjects[type]
    EmailService.send_email(
        to=recipient,
        subject=subject,
        body=body
    )
