from django.db import models
import uuid
from owners.models import Owner
from users.models import User
from django.core.validators import RegexValidator


class Client(models.Model):
    class Meta:
        ordering = ["fullname"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name="client_user",
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        blank=True,
        related_name="client_owner",
    )

    def __repr__(self) -> str:
        return f"Client object - {self.fullname}"
