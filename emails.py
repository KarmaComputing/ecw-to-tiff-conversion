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
    to_addr = [os.getenv("receiver_email_1"), os.getenv("receiver_email_2")]
    BCC = ", ".join(to_addr)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your MAP conversion is ready"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Bcc"] = BCC
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
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("email sent")


def send_notification_upload_email():
    port = os.getenv("PORT")
    sender_email = os.getenv("SENDER_EMAIL")
    smtp_server = os.getenv("SMTP_SERVER")
    password = os.getenv("PASSWORD")
    to_addr = [os.getenv("receiver_email_1"), os.getenv("receiver_email_2")]
    receiver_email = ", ".join(to_addr)
    message = MIMEMultipart("alternative")
    message["Subject"] = "A new map has been uploaded"
    message["From"] = sender_email
    message["To"] = receiver_email
    link = f"""\
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
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("email sent")
