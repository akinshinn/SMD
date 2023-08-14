from django import forms
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
    target = forms.FloatField(min_value=1, required=True, label="Цель", 
                                widget=forms.NumberInput(attrs=attrs))
    stop = forms.FloatField(min_value=1, required=True, label="Стоп приказ", 
                                widget=forms.NumberInput(attrs=attrs))
    attrs["class"] = "form-control form-control-xs"
    attrs["rows"] = 4
    reasonBuy = forms.CharField(max_length=1000, required=True, label="Текст записи",
                            widget=forms.Textarea(attrs=attrs))


class StockPortfolioForm(forms.Form):
    attrs = {"class":"form-control form-control", 'aria-describedby':"helpId"}
    attrs["placeholder"] = "Название вашего портфеля"
    attrs["id"] = "portfolioName"
    portfolioName = forms.CharField(widget=forms.TextInput(attrs=attrs))
    attrs['placeholder'] = "Средства портфеля в рублях"
    attrs["id"] = "portfolioMoney"
    portfolioMoney = forms.FloatField(min_value=1, widget=forms.NumberInput(attrs=attrs))


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
    

class SellStockForm(forms.Form):
    attrs = {"class": "form-control form-control-sm", 
             "aria-describedby": 'helpId'}
    priceSell = forms.FloatField(min_value=1, required=True, label="Цена продажи",
                                 widget=forms.NumberInput(attrs=attrs))
    attrs["value"] = 1
    amountSell = forms.IntegerField(min_value=1, label="Количество",
                                    widget=forms.NumberInput(attrs=attrs))
    attrs["class"] = "form-control form-control-xs"
    attrs["rows"] = 4
    reasonSell = forms.CharField(max_length=1000, required=True, label="Причина продажи",
                                 widget=forms.Textarea(attrs=attrs))
    

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm"}))

    class Meta:
        # attrs = {"class": "form-control form-control-sm"}
        model = User
        fields = ('username', 'email')
        widgets = {
            "username": forms.TextInput(
                                        attrs={"class": "form-control form-control-sm"}, 
                                        ),
            "email": forms.TextInput(
                                     attrs={"class": "form-control form-control-sm"}, 
                                     )
        }
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control form-control-sm"}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "email": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "first_name": forms.TextInput(attrs={"class": "form-control form-control-sm"})
        }