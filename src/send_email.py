# src/send_email.py
from __future__ import annotations

import logging
from typing import Sequence

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from . import config


def send_newsletter(
    recipients: Sequence[str],
    subject: str,
    html_body: str,
    text_body: str,
) -> None:
    """
    Send the newsletter email to the given recipients via SendGrid.
    """
    if not config.SENDGRID_API_KEY:
        raise RuntimeError("SENDGRID_API_KEY is not set in environment/config")

    if not recipients:
        logging.warning("No recipients configured; skipping email send.")
        return

    message = Mail(
        from_email=config.FROM_EMAIL,
        to_emails=list(recipients),
        subject=subject,
        html_content=html_body,
        plain_text_content=text_body,
        is_multiple=True,
    )

    try:
        sg = SendGridAPIClient(config.SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info("SendGrid response status: %s", response.status_code)
        if response.status_code != 202:
            logging.warning("Unexpected SendGrid status code: %s", response.status_code)
    except Exception as exc:
        logging.exception("Error sending newsletter via SendGrid: %s", exc)
        raise