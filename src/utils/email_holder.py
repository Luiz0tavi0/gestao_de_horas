from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from datetime import timedelta
import ipdb
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_template_email(template, to, subj, **kwargs):
    """Sends an email using a template."""
    env = Environment(
        loader=PackageLoader('src', 'email_templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(template)
    ipdb.set_trace()
    send_email(to, subj, template.render(**kwargs))


def send_email(receiver_email: str, link_with_token: str):
    sender_email = "doneganskyylar@gmail.com"

    password = r"W7d`RYx;Ty2=wM48!Fv*?NPe@)U#rk-z~9aAp^tZHfb+"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = sender_email
    message["To"] = receiver_email

    # # Create the plain-text and HTML version of your message
    # text = f"""\
    #   Recebemos uma solicitação de alteração de senha para {receiver_email}.
    #   Cliqueaquipara redefinir sua senha.
    #   Caso o link acima não funcione, copie e cole o seguinte link na barra de endereço do seu navegador:
    #   {link_with_token}\n\n
    #   Obrigado,
    #   Suporte da Firma.
    #   """

    with open('src/utils/template_reset_password.html') as file:
        html = file.read()

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)
    ipdb.set_trace()
    attach_file_to_email(message, 'src/utils/images/animated_header.gif',
                         {'Content-ID': '<animated_header>'})

    # Create secure connection with server and send email
    receiver_email = 'luiz_loon@yahoo.com.br'
    ctx = ssl.create_default_context()
    ipdb.set_trace()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
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
