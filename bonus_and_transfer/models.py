from django.db import models
from clients.models import Client
from owners.models import Owner
import uuid


class BonusAndTransfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    profit_transfer = models.DecimalField(max_digits=10, decimal_places=0)
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="bonus_and_transfer_owner",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="bonus_and_transfer_client",
    )
