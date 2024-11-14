from django.db import models
from uuid import uuid4
from users.models import User
from django.core.validators import RegexValidator


class ENUM_TYPE_OF_SALE(models.TextChoices):
    ALUGUEL = "Aluguel"
    VENDA = "Venda"


class Owner(models.Model):
    class Meta:
        ordering = ["fullname"]

    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
    )
    fullname = models.CharField(max_length=100, null=False)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="CPF must have exactly 11 digits.",
            ),
        ],
    )
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\d{14}$",
                message="CNPJ must have exactly 14 digits.",
            ),
        ],
    )
    telephone = models.CharField(max_length=15, null=False)
    address = models.CharField(max_length=255, null=False)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    type_of_sale = models.CharField(
        max_length=50,
        choices=ENUM_TYPE_OF_SALE.choices,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owner_user",
    )

    def __repr__(self) -> str:
        return self.fullname
