import os
import smtplib
import ssl

from dotenv import load_dotenv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def read_template(filename) -> Template:
    """
    Read template mail file
    :param filename: the HTML filename to read
    :return: Template file
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()

    return Template(template_file_content)


def setup_smtp_server() -> smtplib.SMTP_SSL:
    """
    Creates a secure SMTP server with login credentials
    :return: SMTP Server
    """

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Set up SMTP server
    server = smtplib.SMTP_SSL(host=os.getenv("HOST"), port=os.getenv("PORT"), context=context)
    server.login(os.getenv("FROM_ADDRESS"), os.getenv("PASSWORD"))

    return server


def send_message_via_smtp(to_address, message) -> None:
    """
    Send mail to the SMTP server
    :param to_address:
    :param message: The message to send
    :return: None
    """
    with setup_smtp_server() as server:
        from_address = os.getenv("FROM_ADDRESS")
        server.sendmail(from_address, to_address, message.as_string())
        print("The mail has been send to the SMTP server.")


def setup_mime_multipart(to_address, subject) -> MIMEMultipart:
    """
    Setup the MIME (Multipurpose Internet Mail Extensions) multipart
    :param to_address: The address to send to
    :param subject: The subject of the mail
    :return: MIMEMultipart
    """

    # Load .env file
    load_dotenv()

    message = MIMEMultipart()

    message["From"] = os.getenv("FROM_ADDRESS")
    message["To"] = to_address
    message["Subject"] = subject

    return message


def send_welcome_mail(to_address, username):
    # Setup MIME Multipart
    message = setup_mime_multipart(to_address, "Welcome to Dwetter")

    # Read HTML template
    template = read_template("templates/welcome.html")

    # Substitute variables in HTML
    mime_text = MIMEText(template.substitute(USERNAME=username), "html")
    message.attach(mime_text)

    send_message_via_smtp(to_address, message)


def send_verification_mail(to_address, username):
    # Setup MIME Multipart
    message = setup_mime_multipart(to_address, "Verify your email")

    # Read HTML template
    template = read_template("templates/verification.html")

    # Substitute variables in HTML
    mime_text = MIMEText(template.substitute(USERNAME=username), "html")
    message.attach(mime_text)

    send_message_via_smtp(to_address, message)
