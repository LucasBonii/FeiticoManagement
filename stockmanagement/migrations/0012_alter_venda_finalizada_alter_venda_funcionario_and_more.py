# Generated by Django 5.0.6 on 2024-06-01 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0011_alter_venda_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='finalizada',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='venda',
            name='funcionario',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='stockmanagement.funcionario'),
        ),
        migrations.AlterField(
            model_name='venda',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]