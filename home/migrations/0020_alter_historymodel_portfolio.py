# Generated by Django 4.2.3 on 2023-08-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_stockportfoliomodel_comission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historymodel',
            name='portfolio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.stockportfoliomodel'),
        ),
    ]
