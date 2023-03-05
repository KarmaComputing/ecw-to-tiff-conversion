import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(email=None, filename=None):
    port = os.getenv("PORT")
    sender_email = os.getenv("SENDER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    password = os.getenv("PASSWORD")
    receiver_email = email
    domain = os.getenv("DOMAIN")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your MAP conversion is ready"
    message["From"] = sender_email
    message["To"] = receiver_email
    body = f"""\
    <html>
        <body>
            <p> Please use this link to </p>
            <a href="http://{domain}/payment/{filename}"> download file </a>
        </body>
    </html>
    """
    print(f"Sending email to {email} with body:")
    print(body)
    part1 = MIMEText(body, "html")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("email sent")


def send_email_to_admin(email=None, filename=None):
    port = os.getenv("PORT")
    sender_email = os.getenv("SENDER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    password = os.getenv("PASSWORD")
    receiver_email = os.getenv("receiver_email_1")
    domain = os.getenv("DOMAIN")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your MAP conversion is ready"
    message["From"] = sender_email
    message["To"] = receiver_email
    link = f"""\
    <html>
        <body>
            <p> Please use this link to </p>
            <a href="http://{domain}/download/{filename}"> download file </a>
        </body>
    </html>
    """
    part1 = MIMEText(link, "html")
    message.attach(part1)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string(),
        )
    print("email sent")


def send_notification_upload_email():
    try:
        port = os.getenv("PORT")
        sender_email = os.getenv("SENDER_EMAIL")
        smtp_server = os.getenv("SMTP_SERVER")
        password = os.getenv("PASSWORD")
        receiver_email = os.getenv("receiver_email_1")
        message = MIMEMultipart("alternative")
        message["Subject"] = "A new map has been uploaded"
        message["From"] = sender_email
        message["To"] = receiver_email
        link = """\
        <html>
            <body>
                <p> A newmap has been uploaded!! </p>
            </body>
        </html>
        """
        part1 = MIMEText(link, "html")
        message.attach(part1)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(
                sender_email,
                receiver_email,
                message.as_string(),
            )
        print("email sent")
    except Exception as e:
        print(f"Error sending send_notification_upload_email: {e}")
