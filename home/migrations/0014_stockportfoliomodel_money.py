# Generated by Django 4.2.3 on 2023-07-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_stockmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockportfoliomodel',
            name='money',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]