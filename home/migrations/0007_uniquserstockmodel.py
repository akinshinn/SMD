# Generated by Django 4.2.3 on 2023-07-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_diarypostmodel_portfolio'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqUserStockModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tick', models.CharField(max_length=4)),
                ('industry', models.CharField(max_length=50)),
                ('user', models.IntegerField()),
            ],
        ),
    ]
