# Generated by Django 5.1 on 2024-10-23 20:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientPaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sales_bonus', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profit_transfer', models.DecimalField(decimal_places=0, max_digits=10)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clients.client')),
            ],
        ),
    ]