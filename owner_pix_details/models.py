from django.db import models
from owner_payment_method.models import OwnerPaymentMethod


class ENUM_PIX_TYPE_OWNER(models.TextChoices):
    CPF = "CPF", "CPF"
    CNPJ = "CNPJ", "CNPJ"
    TELEFONE = "Telefone", "Telefone"
    EMAIL = "Email", "Email"
    CHAVE_ALEATORIA = "Chave Aleatória", "Chave Aleatória"
    NAO_POSSUI_PIX = "Não Possui Pix", "Não Possui Pix"


class OwnerPixDetails(models.Model):
    owner_payment_method = models.ForeignKey(
        OwnerPaymentMethod,
        related_name="pix_details",
        on_delete=models.CASCADE,
    )
    pix_key = models.CharField(max_length=255)
    pix_type = models.CharField(max_length=50)

    def __repr__(self) -> str:
        return f"{self.pix_type}: {self.pix_key}"
