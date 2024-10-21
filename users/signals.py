from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from os import getenv
from dotenv import load_dotenv


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
    Equipe IMOGIS
    """

    image_url = "https://raw.githubusercontent.com/IMOGIS-Sistema-para-Imobiliaria/imogis_backend/refs/heads/main/media/IMOGIS.png"

    html_content = f"""
    <p style="font-size: 1rem; font-weight: 600;">
        Olá,<br>
        <strong style="font-size: 2rem;">
            {user.first_name} {user.last_name}
        </strong>
    </p>

    <p style="font-weight: 600; font-size: 0.8rem;">
        Recebemos uma solicitação para 
        <strong style="color: #1E3A8A; font-weight: bold;">redefinir sua senha</strong>. 
        Utilize o código abaixo para completar o processo:
    </p>

    <div style="margin-left: 15%; text-align: center; width: min-content;">
        <p style="font-weight: 600; font-size: 1rem; margin-top: 2rem;">
            Código de Redefinição:
        </p>

        <div style="margin: 20px 0;">
            <div style="display: inline-block; height: 80px; width: 288px; border: 2px solid #FCD34D; background-color: #1E40AF; border-radius: 0.375rem; line-height: 80px;">
                <p style="font-size: 24px; color: #FCD34D; margin: 0; font-weight: bold; text-align: center;">
                    {code}
                </p>
            </div>
        </div>

        <p style="font-weight: bold; color: #B91C1C; margin-bottom: 2rem;">
            Este código é válido por apenas 30 minutos!
        </p>
    </div>

    <p style="font-style: italic;">
        Se você não fez esta solicitação, por favor, ignore este email.
    </p>

    <p style="height: 18px; margin: 0; font-style: italic;">
        Atenciosamente,
    </p>

    <p style="font-size: 1rem; height: 18px; margin: 0; font-weight: 600;">
        Equipe <span style="color:#1e3a8a;font-weight: 800;">IMOGIS</span>.
    </p>

    <figure style="display: flex; margin: 0; padding: 0; width: min-content;">
        <img src="{image_url}" alt="Cartão de Visita IMOGIS" style="width: 300px; display: block; margin: 20px auto;" />
    </figure>
    """

    email = EmailMultiAlternatives(
        email_subject, text_content, getenv("POSTGRES_PORT"), [user.email]
    )

    email.attach_alternative(html_content, "text/html")

    email.send()
