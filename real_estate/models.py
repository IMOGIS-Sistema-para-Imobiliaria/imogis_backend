import uuid
from django.db import models
from clients.models import Client
from owners.models import Owner


class ENUM_Type_Of_Housing(models.TextChoices):
    ALUGUEL = "Aluguel", "Aluguel"
    VENDA = "Venda", "Venda"


class RealEstate(models.Model):
    class Meta:
        ordering = ["address"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_housing = models.CharField(
        max_length=7, choices=ENUM_Type_Of_Housing.choices, null=False
    )
    address = models.CharField(max_length=255, null=False)
    owner_name = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    about_the_property = models.CharField(max_length=255, null=False)
    rental_value = models.PositiveIntegerField(null=False)
    tenant_present = models.BooleanField(null=False)
    readjustment_date = models.DateTimeField(null=True, blank=True)
    client = models.OneToOneField(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="real_estate_client",
    )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="real_estate_owner",
    )

    def __repr__(self):
        return f"{self.type_of_housing} - {self.address[:20].strip()}..."
