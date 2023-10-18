import smtplib
from email.message import EmailMessage
from typing import Dict

from fastapi.templating import Jinja2Templates

from core.fields import NotificationType
from core.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_FROM

templates = Jinja2Templates(directory="templates/email")

templates_mapper = {
    NotificationType.new_operator_invited: "invitation.html",
}

subjects = {
    NotificationType.new_operator_invited: "You were invited.",
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
        s.send_message(message)
        s.quit()


def send_notification(recipient: str, type: NotificationType, context: Dict):
    template = templates.TemplateResponse(templates_mapper[type], context)
    subject = subjects[type]
    EmailService.send_email(to=recipient,
                            subject=subject,
                            body=context["password"])
