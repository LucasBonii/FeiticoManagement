# Generated by Django 5.0.6 on 2024-06-01 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0012_alter_venda_finalizada_alter_venda_funcionario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='itenspedido',
            name='preco_parcial',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
