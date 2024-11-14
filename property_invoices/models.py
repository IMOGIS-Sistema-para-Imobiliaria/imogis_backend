import uuid
from django.db import models
from clients.models import Client
from real_estate.models import RealEstate


class ENUM_Months_Of_Year(models.TextChoices):
    JANEIRO = "Janeiro", "Janeiro"
    FEVEREIRO = "Fevereiro", "Fevereiro"
    MARCO = "Março", "Março"
    ABRIL = "Abril", "Abril"
    MAIO = "Maio", "Maio"
    JUNHO = "Junho", "Junho"
    JULHO = "Julho", "Julho"
    AGOSTO = "Agosto", "Agosto"
    SETEMBRO = "Setembro", "Setembro"
    OUTUBRO = "Outubro", "Outubro"
    NOVEMBRO = "Novembro", "Novembro"
    DEZEMBRO = "Dezembro", "Dezembro"


class ENUM_Status_Of_Invoice(models.TextChoices):
    PAGO = "Pago", "Pago"
    PENDENTE = "Pendente", "Pendente"
    ATRASADO = "Atrasado", "Atrasado"


class PropertyInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.CharField(
        max_length=9, choices=ENUM_Months_Of_Year.choices, null=False
    )
    due_date = models.PositiveIntegerField(null=False)
    rental_value = models.PositiveIntegerField(null=False)
    status_invoice = models.CharField(
        max_length=8,
        choices=ENUM_Status_Of_Invoice.choices,
        default=ENUM_Status_Of_Invoice.PENDENTE,
        null=False,
    )
    date_it_was_paid = models.DateTimeField(null=True, blank=True)
    observations = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="property_invoice_client",
    )
    real_estate = models.ForeignKey(
        RealEstate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="property_invoice_real_estate",
    )

    def __repr__(self):
        return f"Invoice {self.id} - {self.month} - {self.status_invoice}"
