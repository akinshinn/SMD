from django import forms
from .StockPortfolio import Stock, StockPortfolio

class StockForm(forms.Form):
    tick = forms.CharField(max_length=4, min_length=4, label="TICK", required=True)
    priceRUB = forms.FloatField(min_value=1, required=True, label="Цена")
    amount = forms.IntegerField(min_value=1, label="Количество")
    industry = forms.CharField(required=False, label="Отрасль")
    dateBuying = forms.DateField(required=True, label="Дата покупки")

class StockPortfolioForm(forms.Form):
    name = forms.CharField(label="Название портфеля", required=True)