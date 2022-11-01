# Generated by Django 4.1.2 on 2022-11-01 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0012_bank_balancecurrent_bank_lastupdated_category_invest_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='fromBank',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.bank'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fromCat',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fromCat', to='budget.category'),
        ),
    ]