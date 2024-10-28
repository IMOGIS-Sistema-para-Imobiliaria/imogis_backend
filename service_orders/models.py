import uuid
from django.db import models

from owners.models import Owner


class ENUM_Service_Category(models.TextChoices):
    MANUTENCAO = "Manutenção", "Manutenção"
    REFORMA = "Reforma", "Reforma"
    PINTURA = "Pintura", "Pintura"
    ELÉTRICA = "Elétrica", "Elétrica"
    HIDRÁULICA = "Hidráulica", "Hidráulica"
    LIMPEZA = "Limpeza", "Limpeza"
    JARDINAGEM = "Jardinagem", "Jardinagem"
    SEGURANCA = "Segurança", "Segurança"
    CLIMATIZACAO = "Climatização", "Climatização"
    OUTRO = "Outro", "Outro"


class ENUM_Payment_Status(models.TextChoices):
    PAGO = "Pago", "Pago"
    PENDENTE = "Pendente", "Pendente"
    ATRASADO = "Atrasado", "Atrasado"


class ServiceOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_category = models.CharField(
        max_length=13,
        choices=ENUM_Service_Category.choices,
        default=ENUM_Service_Category.OUTRO,
        null=False,
    )
    service_provided = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=8,
        choices=ENUM_Payment_Status.choices,
        default=ENUM_Payment_Status.PENDENTE,
        null=False,
    )
    date_paid = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_orders",
    )

    def __repr__(self):
        return f"Order {self.id} - {self.service_provided[:20]}"
