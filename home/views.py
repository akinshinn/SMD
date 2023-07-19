from django.shortcuts import render
from .forms import StockForm
from .forms import StockPortfolioForm
from .StockPortfolio import StockPortfolio, Stock
from .models import StockPortfolioModel, StockModel
# Create your views here.

def deleteALL():
    StockPortfolioModel.objects.all().delete()
    StockModel.objects.all().delete()

    
def getStocksFromPortfolio(PortfolioID):
    result = []
    for stock in StockPortfolioModel.objects.filter(Portfolio_id = PortfolioID):
        cStock = Stock(stock.tick, stock.priceRUB,  stock.amount, stock.industry, stock.dateBuying)
        result += [cStock]
    return result


def index(request):
    data = {}
    deleteALL()
    if request.method == "POST":
        if request.POST.get('tick'):
            tick = request.POST.get("tick")
            priceRUB = request.POST.get("priceRUB")
            amount = request.POST.get("amount")
            industry = request.POST.get("industry", "NULL")
            dateBuying = request.POST.get("dateBuying")
            curStock = StockModel(tick = tick, priceRUB=priceRUB, amount = amount, industry=industry, dateBuying=dateBuying, \
                                  Portfolio = StockPortfolioModel.objects.last())
            curStock.save()
        else:
            name = request.POST.get("name")
            SP = StockPortfolioModel(name=name)
            SP.save()
            CSP = StockPortfolioModel.objects.get(name=name)
            data['namePortfolio'] = CSP.name
            data['formStock'] = StockForm()
    else:
        data['form'] = StockPortfolioForm()
    return render(request, 'home/index.html', context=data)


def profile(request):
    return render(request, 'home/profile.html')


def about(request):
    return render(request, 'home/about.html')
