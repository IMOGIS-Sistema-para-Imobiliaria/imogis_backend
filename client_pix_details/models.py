from django.db import models
from client_payment_method.models import ClientPaymentMethod


class ENUM_PIX_TYPE_CLIENT(models.TextChoices):
    CPF = "CPF", "CPF"
    CNPJ = "CNPJ", "CNPJ"
    TELEFONE = "Telefone", "Telefone"
    EMAIL = "Email", "Email"
    CHAVE_ALEATORIA = "Chave Aleatória", "Chave Aleatória"
    NAO_POSSUI_PIX = "Não Possui Pix", "Não Possui Pix"


class ClientPixDetails(models.Model):
    client_payment_method = models.ForeignKey(
        ClientPaymentMethod,
        related_name="pix_details",
        on_delete=models.CASCADE,
    )
    pix_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    pix_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=ENUM_PIX_TYPE_CLIENT.choices,
        default=ENUM_PIX_TYPE_CLIENT.NAO_POSSUI_PIX,
    )

    def __repr__(self) -> str:
        return f"{self.pix_type}: {self.pix_key}"
