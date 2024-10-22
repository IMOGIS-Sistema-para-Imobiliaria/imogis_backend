from django.db import models
from owner_payment_method.models import OwnerPaymentMethod


class OwnerBankDetails(models.Model):
    bank = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    owner_payment_method = models.ForeignKey(
        OwnerPaymentMethod,
        related_name="bank_details",
        on_delete=models.CASCADE,
    )

    def __repr__(self) -> str:
        return f"{self.bank} - {self.account}"
