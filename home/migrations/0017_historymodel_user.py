# Generated by Django 4.2.3 on 2023-08-02 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_historymodel_amountsell_alter_stockmodel_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='historymodel',
            name='user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]