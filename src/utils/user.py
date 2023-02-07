import os
import ipdb
import smtplib
import ssl
from flask_jwt_extended import create_access_token, create_refresh_token

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from src.adapters.user import User


def make_login_response(identity: User) -> dict:
    acess_token = create_access_token(identity=identity.id)

    refresh_token = create_refresh_token(identity=identity.id)
    return {'token': acess_token, 'refresh_token': refresh_token}


def send_email(receiver_email: str, link_with_token: str):

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = os.environ.get('DEFAULT_FROM_EMAIL')
    message["To"] = receiver_email

    # # Create the plain-text and HTML version of your message
    text = f"""\
      Recebemos uma solicitação de alteração de senha para {receiver_email}.
      Cliqueaquipara redefinir sua senha.
      Caso o link acima não funcione, copie e cole o seguinte link na barra de endereço do seu navegador:
      {link_with_token}\n\n
      Obrigado,
      Suporte da Firma.
      """

    with open('src/utils/template_reset_password.html') as file:
        html = file.read()

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    ipdb.set_trace()
    attach_file_to_email(
        message, 'src/email_templates/images_template_reset_password/animated_header.gif',
        {'Content-ID': '<animated_header>'}
    )

    # Create secure connection with server and send email
    ctx = ssl.create_default_context()
    ipdb.set_trace()
    with smtplib.SMTP_SSL(str(os.environ.get('EMAIL_HOST')), os.environ.get('EMAIL_PORT'), context=ctx) as server:
        server.login(message["From"], os.environ.get('EMAIL_HOST_PASSWORD'))
        server.sendmail(
            message["From"], receiver_email, message.as_string()
        )


def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        # ipdb.set_trace()
        file_attachment = MIMEApplication(f.read())

    # Add header/name to the attachments
    # ipdb.set_trace()
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # ipdb.set_trace()
    # Set up the input extra_headers for img
    # Default is None: since for regular file attachments, it's not needed
    # When given a value: the following code will run
    # Used to set the cid for image
    if extra_headers is not None:
        ipdb.set_trace()
        for name, value in extra_headers.items():
            ipdb.set_trace()
            file_attachment.add_header(name, value)
    # Attach the file to the message
    ipdb.set_trace()
    email_message.attach(file_attachment)
