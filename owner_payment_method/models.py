from django.db import models
import uuid


class OwnerPaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_bonus = models.IntegerField(null=False)
    profit_transfer = models.IntegerField(default=0)
    owner_id = models.OneToOneField(
        "owner.Owner",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __repr__(self) -> str:
        return f"Payment Method {self.id} for Owner {self.owner}"
