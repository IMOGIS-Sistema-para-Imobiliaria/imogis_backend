from django.db import models
import uuid
from users.models import User
from django.core.validators import RegexValidator


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=100)
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

    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    owner_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="clients"
    )
    real_estate_id = models.UUIDField(blank=True, null=True, default=None)
    contract_id = models.UUIDField(blank=True, null=True, default=None)

    def __repr__(self) -> str:
        return f"Client object - {self.fullname}"
