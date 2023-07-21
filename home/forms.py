from django import forms
from .StockPortfolio import Stock, StockPortfolio
import datetime

class StockForm(forms.Form):
    attrs = {"class": "form-control form-control-sm", 
             "aria-describedby": 'helpId'}
    
    tick = forms.CharField(max_length=4, min_length=4, label="TICK", required=True,
                           widget=forms.TextInput(attrs = attrs))
    priceRUB = forms.FloatField(min_value=1, required=True, label="Цена", 
                                widget=forms.NumberInput(attrs=attrs))
    attrs["value"] = 1
    amount = forms.IntegerField(min_value=1, label="Количество",
                                widget=forms.NumberInput(attrs=attrs))
    attrs.pop("value")
    industry = forms.CharField(required=False, label="Отрасль",
                               widget=forms.TextInput(attrs=attrs))
    attrs["value"] = datetime.date.today()
    dateBuying = forms.DateField(required=True, label="Дата покупки",
                                 widget=forms.DateInput(attrs=attrs))


class StockPortfolioForm(forms.Form):
    portfolioName = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control", 
                                                         'aria-describedby':"helpId",  
                                                         'placeholder':"Название вашего портфеля",
                                                         "id": "portfolioName"}))
