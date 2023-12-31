# Generated by Django 4.2.3 on 2023-07-27 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_diarypostmodel_pricemax_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tick', models.CharField(max_length=4)),
                ('priceBuy', models.FloatField()),
                ('priceSell', models.FloatField()),
                ('reasonSell', models.TextField()),
                ('reasonBuy', models.TextField()),
                ('dateBuy', models.DateField()),
                ('dateSell', models.DateField()),
                ('industry', models.CharField(max_length=50)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.stockportfoliomodel')),
            ],
        ),
    ]
