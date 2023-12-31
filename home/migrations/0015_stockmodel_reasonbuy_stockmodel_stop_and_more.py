# Generated by Django 4.2.3 on 2023-07-31 18:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_stockportfoliomodel_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockmodel',
            name='reasonBuy',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockmodel',
            name='stop',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stockmodel',
            name='target',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
