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


class DiaryPostForm(forms.Form):
    attrs = {"class": "form-control form-control-xs", 
             "aria-describedby": 'helpId'}
    priceOpen = forms.FloatField(min_value=1, required=True, label="Цена открытия", 
                                 widget=forms.NumberInput(attrs = attrs))
    priceClose = forms.FloatField(min_value=1, required=True, label="Цена закрытия",
                                 widget=forms.NumberInput(attrs = attrs))
    priceMin = forms.FloatField(min_value=1, label="Минимальная цена", required=False,
                                 widget=forms.NumberInput(attrs = attrs))
    priceMax = forms.FloatField(min_value=1, label="Максимальная цена", required=False,
                                 widget=forms.NumberInput(attrs = attrs))
    attrs["value"] = datetime.date.today()
    date = forms.DateField(required=True, label="Дата",help_text="Формат: YYYY-MM-DD",
                                 widget=forms.DateInput(attrs=attrs))
    attrs.pop("value")
    attrs["class"] = "form-control form-control-xs"
    attrs["rows"] = 4
    post = forms.CharField(max_length=1000, required=True, label="Текст записи",
                            widget=forms.Textarea(attrs=attrs))
    

class EditStockForm(forms.Form):
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