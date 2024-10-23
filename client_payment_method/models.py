from django.db import models
import uuid
from clients.models import Client


class ClientPaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    profit_transfer = models.DecimalField(max_digits=10, decimal_places=0)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Payment Method {self.id} for Client {self.client.id}"
