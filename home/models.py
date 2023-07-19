from django.db import models

# Create your models here.
class StockPortfolioModel(models.Model):
    name = models.CharField(max_length=50)

class StockModel(models.Model):
    tick = models.CharField(max_length=4)
    priceRUB = models.FloatField()
    amount = models.IntegerField()
    industry = models.CharField(max_length=50)
    dateBuying = models.DateField()
    Portfolio = models.ForeignKey(StockPortfolioModel, on_delete=models.CASCADE)
    