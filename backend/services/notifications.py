import os
import smtplib
from email.message import EmailMessage
from typing import Dict

import jinja2
from fastapi.templating import Jinja2Templates
from loguru import logger

from core import settings
from core.database import get_contextual_session
from core.fields import NotificationType
from core.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from services.drivers import build_drivers_query, is_driver_debtor
from services.statements import generate_statement_for_driver
from services.transactions import find_drivers_transactions
from utils import paginate
from views.drivers import UpdateDriverView
from views.notifications import PaymentReminderView

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


async def send_reminder_to_debtors(callback=None, view: UpdateDriverView | None = None):
    page = 1
    size = 10
    notifications = []

    async with get_contextual_session() as session:
        while True:
            items, pagination = await paginate(
                session,
                lambda: build_drivers_query(""),
                page,
                size
            )
            for driver in [item[0] for item in items]:
                is_debtor, month, year = await is_driver_debtor(session, driver)

                if is_debtor:
                    if callback and view:  # we can block driver here
                        await callback(session, driver.garage_id, driver.id, view)
                        await session.commit()

                    transactions = await find_drivers_transactions(
                        session,
                        driver,
                        month,
                        year
                    )
                    statement = await generate_statement_for_driver(
                        session,
                        driver.garage,
                        driver,
                        transactions,
                        month,
                        year
                    )
                    context = PaymentReminderView(
                        month=month,
                        year=year,
                        total_cost=statement.total_cost,
                        total_kw=statement.total_kw
                    )

                    logger.info(f"{driver} is a debtor (context={context})")

                    notifications.append(
                        (driver.email, NotificationType.friendly_reminder, context.dict())
                    )

            if pagination.last_page == page:
                break
            page += 1

    for notification in notifications:
        await send_notification(*notification)
