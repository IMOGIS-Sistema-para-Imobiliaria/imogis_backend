from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from os import getenv
from dotenv import load_dotenv
import os


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    load_dotenv()

    user = reset_password_token.user
    code = user.generate_reset_code()

    email_subject = "Redefinição de Senha - IMOGIS"

    text_content = f"""
    Olá, {user.first_name} {user.last_name}!

    Recebemos uma solicitação para redefinir sua senha. Utilize o código abaixo para completar o processo:

    Código de Redefinição: {code}

    Lembre-se: este código é válido por 30 minutos.

    Se você não fez esta solicitação, por favor, ignore este email.

    Atenciosamente,
    Equipe IMOGIS.
    """

    html_content = f"""
    <p>Olá, {user.first_name} {user.last_name}!</p>
    <p>Recebemos uma solicitação para redefinir sua senha. Utilize o código abaixo para completar o processo:</p>
    <p>Código de Redefinição: <strong>{code}</strong></p>
    <p>Lembre-se: este código é válido por 30 minutos.</p>
    <p>Se você não fez esta solicitação, por favor, ignore este email.</p>
    <p>Atenciosamente,<br>Equipe IMOGIS.</p>
    <p>
        <img src="cid:cartao_de_visita" alt="Cartão de Visita IMOGIS" style="width:200px;"/>
    </p>
    """

    email = EmailMultiAlternatives(
        email_subject, text_content, getenv("POSTGRES_PORT"), [user.email]
    )

    email.attach_alternative(html_content, "text/html")

    email.send()
