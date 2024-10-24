import uuid
from django.db import models


class ENUM_Type_Of_Contract(models.TextChoices):
    ALUGUEL = "Aluguel", ("Aluguel")
    VENDA = "Venda", ("Venda")
    NAO_INFORMADO = "Não Informado", ("Não Informado")


class ENUM_Status_Of_Contract(models.TextChoices):
    ATIVO = "Ativo", ("Ativo")
    INATIVO = "Inativo", ("Inativo")
    PENDENTE = "Pendente", ("Pendente")


class Contract(models.Model):
    class Meta:
        ordering = ["contract_belongs_to"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract_belongs_to = models.CharField(
        max_length=100, null=False, blank=False
    )
    type_of_contract = models.CharField(
        max_length=13,
        choices=ENUM_Type_Of_Contract.choices,
        default=ENUM_Type_Of_Contract.NAO_INFORMADO,
        null=False,
    )
    status = models.CharField(
        max_length=8,
        choices=ENUM_Status_Of_Contract.choices,
        default=ENUM_Status_Of_Contract.PENDENTE,
        null=False,
    )
    contract_duration = models.PositiveIntegerField(null=False)
    start_of_contract = models.DateTimeField(null=False)
    end_of_contract = models.DateTimeField(null=False)
    rental_value = models.PositiveIntegerField(null=False)
    due_date = models.PositiveIntegerField(null=False)
    client_id = models.UUIDField(null=True, blank=True, default=None)
    owner_id = models.UUIDField(null=True, blank=True, default=None)
    real_estate_id = models.UUIDField(null=True, blank=True, default=None)

    def __repr__(self) -> str:
        return f"{self.contract_belongs_to} - {self.type_of_contract}"
