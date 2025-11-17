import smtplib
from . import celery
from email.message import EmailMessage
import logging
import os


@celery.task
def send_email(
    body: str,
    to_email: str,
    from_email: str,
    subject: str = "Lorehub Notification",
    smtp_password: str = "smtp.gmail.com",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
):
    try:
        smtp_password = os.getenv("SMTP_PASSWORD")
        if not smtp_password:
            raise ValueError("SMTP_PASSWORD is not set in environment variables.")

        # Create email message
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(body)

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, smtp_password)
            server.send_message(msg)

        logging.info(f"Email sent to {to_email}")

    except Exception as e:
        logging.error(f"Failed to send email to {to_email}: {str(e)}")
        # Optionally: raise or return False to retry later
