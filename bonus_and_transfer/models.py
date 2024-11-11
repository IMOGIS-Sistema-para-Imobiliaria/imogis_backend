from django.db import models
from clients.models import Client
from owners.models import Owner


class BonusAndTransfer(models.Model):
    sales_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    profit_transfer = models.DecimalField(max_digits=10, decimal_places=0)
    owner = models.ForeignKey(
        Owner, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
