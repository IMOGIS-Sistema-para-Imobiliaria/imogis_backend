# Generated by Django 5.1 on 2024-11-05 20:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('real_estate', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('month', models.CharField(choices=[('Janeiro', 'Janeiro'), ('Fevereiro', 'Fevereiro'), ('Março', 'Março'), ('Abril', 'Abril'), ('Maio', 'Maio'), ('Junho', 'Junho'), ('Julho', 'Julho'), ('Agosto', 'Agosto'), ('Setembro', 'Setembro'), ('Outubro', 'Outubro'), ('Novembro', 'Novembro'), ('Dezembro', 'Dezembro')], max_length=9)),
                ('due_date', models.PositiveIntegerField()),
                ('rental_value', models.PositiveIntegerField()),
                ('status_invoice', models.CharField(choices=[('Pago', 'Pago'), ('Pendente', 'Pendente'), ('Atrasado', 'Atrasado')], default='Pendente', max_length=8)),
                ('date_it_was_paid', models.DateTimeField(blank=True, null=True)),
                ('observations', models.CharField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_invoice_client', to='clients.client')),
                ('real_estate', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_invoice_real_estate', to='real_estate.realestate')),
            ],
        ),
    ]