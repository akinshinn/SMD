from django.db import models

# Create your models here.
class StockPortfolioModel(models.Model):
    name = models.CharField(max_length=50)
    user = models.IntegerField()

class StockModel(models.Model):
    tick = models.CharField(max_length=4)
    priceRUB = models.FloatField()
    amount = models.IntegerField()
    industry = models.CharField(max_length=50)
    dateBuying = models.DateField()
    Portfolio = models.ForeignKey(StockPortfolioModel, on_delete=models.CASCADE)
    
class UniqUserStockModel(models.Model):
    tick = models.CharField(max_length=4)
    industry = models.CharField(max_length=50)
    user = models.IntegerField()

class DiaryPostModel(models.Model):
    Stock = models.ForeignKey(UniqUserStockModel, on_delete=models.DO_NOTHING)
    priceOpen = models.FloatField()
    priceClose = models.FloatField()
    priceMax = models.FloatField(null=True)
    priceMin = models.FloatField(null=True)
    msg = models.TextField()
    date = models.DateField()
    user = models.IntegerField()

