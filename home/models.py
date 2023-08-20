from django.db import models

# Create your models here.
class StockPortfolioModel(models.Model):
    name = models.CharField(max_length=50)
    user = models.IntegerField()
    money = models.FloatField()
    comission = models.FloatField()

class StockModel(models.Model):
    tick = models.CharField(max_length=4)
    priceRUB = models.FloatField()
    amount = models.IntegerField()
    industry = models.CharField(max_length=50, null=True)
    dateBuying = models.DateField()
    Portfolio = models.ForeignKey(StockPortfolioModel, on_delete=models.CASCADE)
    user = models.IntegerField()
    reasonBuy = models.TextField()
    target = models.FloatField()
    stop = models.FloatField()


class DiaryPostModel(models.Model):
    stockTick = models.CharField(max_length=4)
    priceOpen = models.FloatField()
    priceClose = models.FloatField()
    priceMax = models.FloatField(null=True)
    priceMin = models.FloatField(null=True)
    msg = models.TextField()
    date = models.DateField()
    user = models.IntegerField()

class HistoryModel(models.Model):
    tick = models.CharField(max_length=4)
    priceBuy = models.FloatField()
    priceSell = models.FloatField()
    reasonSell = models.TextField()
    reasonBuy = models.TextField()
    dateBuy = models.DateField()
    dateSell = models.DateField()
    industry = models.CharField(max_length=50)
    portfolio = models.ForeignKey(StockPortfolioModel, on_delete=models.CASCADE)
    amountSell = models.IntegerField()
    user = models.IntegerField()
