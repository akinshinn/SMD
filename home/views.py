from django.shortcuts import render
from .forms import StockForm
from .forms import StockPortfolioForm
from .models import StockPortfolioModel, StockModel
from .operationsWithModels import *


def index(request):
    userID = 1
    data = {"portfolioForm": StockPortfolioForm(), "stockForm": StockForm(),
            "isAnyPortfolioCreated": StockPortfolioModel.objects.all().__len__() > 0,
            "userPortfolios": getUserPortfolios(userID),
            "isError": False,
            "textError": ""}

    if request.method == "POST":
        if data["isAnyPortfolioCreated"] and not request.POST.get('portfolioName'):
            tick = request.POST.get("tick").upper()
            if not tick.isalpha():
                data["isError"] = True
                data["textError"] = "TICK состоит только из латинских букв"
                return render(request, 'home/index.html', context=data)
            priceRUB = request.POST.get("priceRUB")
            amount = request.POST.get("amount")
            industry = request.POST.get("indusrty", "Без отрасли")
            dateBuying = request.POST.get("dateBuying")
            portfolio = request.POST.get("portfolio")
            cStock = StockModel(tick=tick, priceRUB = priceRUB, amount = amount, industry=industry, dateBuying = dateBuying, 
                                Portfolio = StockPortfolioModel.objects.get(user=userID, name = portfolio))
            cStock.save()
        else:
            name = request.POST.get("portfolioName")
            try:
                StockPortfolioModel.objects.get(name = name, user = userID)
                data["isError"] = True
                data["textError"] = "Портфель с таким названием уже существует"
            except:
                cPortfolio = StockPortfolioModel(name = name, user = userID)
                cPortfolio.save()
                data["isAnyPortfolioCreated"] = True
    return render(request, 'home/index.html', context=data)


def profile(request):
    return render(request, 'home/profile.html')

def about(request):
    return render(request, 'home/about.html')

def login(request):
    return render(request, 'home/login.html')

def sign_up(request):
    data = {}
    if request.method == "POST":
        name = request.POST.get("floatingInputName")
        email = request.POST.get("floatingInput")
        passw1 = request.POST.get("floatingPassword")
        passw2 = request.POST.get("confirmPassword")
        print(name, email, passw1, passw2)

    return render(request, "home/sign-up.html", context=data)

def diary(request):
    return render(request, "home/diary.html")

def portfolios(request):
    userID = 1
    portfolioAndStocks= []
    for p in getUserPortfolios(userID):
        portfolioAndStocks += [[p[0], getStocksFromPortfolio(p[1])]]
    data = {"portfolios": portfolioAndStocks}

    return render(request, "home/portfolios.html", context=data)

