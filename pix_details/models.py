from django.db import models
from clients.models import Client
from owners.models import Owner
import uuid


class ENUM_PIX_TYPE_CLIENT(models.TextChoices):
    CPF = "CPF", "CPF"
    CNPJ = "CNPJ", "CNPJ"
    TELEFONE = "Telefone", "Telefone"
    EMAIL = "Email", "Email"
    CHAVE_ALEATORIA = "Chave Aleatória", "Chave Aleatória"
    NAO_POSSUI_PIX = "Não Possui Pix", "Não Possui Pix"


class PixDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pix_key = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    pix_type = models.CharField(
        max_length=15,
        choices=ENUM_PIX_TYPE_CLIENT.choices,
        default=ENUM_PIX_TYPE_CLIENT.NAO_POSSUI_PIX,
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="pix_details_owner",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="pix_details_client",
    )

    def __repr__(self) -> str:
        return f"{self.pix_type}: {self.pix_key}"
