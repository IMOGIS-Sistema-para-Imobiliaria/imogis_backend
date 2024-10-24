from django.db import models
from client_payment_method.models import ClientPaymentMethod


class ENUM_BANKS(models.TextChoices):
    BANCO_DO_BRASIL = "Banco do Brasil", "Banco do Brasil"
    BRADESCO = "Bradesco", "Bradesco"
    CAIXA_ECONOMICA_FEDERAL = (
        "Caixa Econômica Federal",
        "Caixa Econômica Federal",
    )
    ITAU = "Itaú", "Itaú"
    SANTANDER = "Santander", "Santander"
    BTG_PACTUAL = "BTG Pactual", "BTG Pactual"
    SAFRA = "Safra", "Safra"
    BANCO_INTER = "Banco Inter", "Banco Inter"
    NUBANK = "Nubank", "Nubank"
    C6_BANK = "C6 Bank", "C6 Bank"
    BANCO_PAN = "Banco Pan", "Banco Pan"
    BANRISUL = "Banrisul", "Banrisul"
    BANCO_VOTORANTIM = "Banco Votorantim", "Banco Votorantim"
    SICOOB = "Sicoob", "Sicoob"
    SICREDI = "Sicredi", "Sicredi"
    BANCO_ORIGINAL = "Banco Original", "Banco Original"
    MERCADO_PAGO = "Mercado Pago", "Mercado Pago"
    PAGSEGURO = "PagSeguro", "PagSeguro"
    BANCO_BMG = "Banco BMG", "Banco BMG"
    CREDISAN = "Credisan", "Credisan"
    BANCO_TOPAZ = "Banco Topázio", "Banco Topázio"
    ABC_BRASIL = "Banco ABC Brasil", "Banco ABC Brasil"
    BANCO_RIBEIRAO_PRETO = "Banco Ribeirão Preto", "Banco Ribeirão Preto"
    CITIBANK = "Citibank", "Citibank"
    JP_MORGAN = "JP Morgan", "JP Morgan"
    BANCO_MODAL = "Banco Modal", "Banco Modal"
    BANCO_PINE = "Banco Pine", "Banco Pine"
    BANCO_SOFISA = "Banco Sofisa", "Banco Sofisa"
    BANCO_MERCANTIL = "Banco Mercantil", "Banco Mercantil"
    BANCO_CETELEM = "Banco Cetelem", "Banco Cetelem"


class ENUM_ACCOUNT_TYPE(models.TextChoices):
    CONTA_CORRENTE = "Conta Corrente", "Conta Corrente"
    CONTA_POUPANCA = "Conta Poupança", "Conta Poupança"
    CONTA_SALARIO = "Conta Salário", "Conta Salário"
    CONTA_DIGITAL = "Conta Digital", "Conta Digital"
    CONTA_CONJUNTA = "Conta Conjunta", "Conta Conjunta"
    CONTA_PAGAMENTO = "Conta de Pagamento", "Conta de Pagamento"
    CONTA_INVESTIMENTO = "Conta de Investimento", "Conta de Investimento"
    CONTA_FACIL = "Conta Fácil", "Conta Fácil"


class ClientBankDetails(models.Model):
    bank = models.CharField(max_length=255, choices=ENUM_BANKS.choices)
    account = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    account_type = models.CharField(
        max_length=255,
        choices=ENUM_ACCOUNT_TYPE.choices,
    )
    client_payment_method = models.ForeignKey(
        ClientPaymentMethod,
        related_name="bank_details",
        on_delete=models.CASCADE,
    )

    def __repr__(self) -> str:
        return f"{self.bank} - {self.account} and {self.agency}"
