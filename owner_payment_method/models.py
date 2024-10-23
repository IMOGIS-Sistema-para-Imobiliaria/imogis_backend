from django.db import models
import uuid

from owners.models import Owner


class OwnerPaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    profit_transfer = models.DecimalField(max_digits=10, decimal_places=0)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f"Payment Method {self.id} for Owner {self.owner.id}"
