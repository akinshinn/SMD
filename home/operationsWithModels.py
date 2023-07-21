from .models import StockModel, StockPortfolioModel
from .StockPortfolio import StockPortfolio, Stock


def deleteAllFromModel(model):
    model.objects.all().delete()


def deleteAll():
    models = [StockPortfolioModel, StockModel]
    for model in models:
        deleteAllFromModel(model)


def getUserPortfolios(UserID = 1):
    portfolios = StockPortfolioModel.objects.filter(user = UserID)
    portfoliosList = [[portfolio.name, portfolio.id] for portfolio in portfolios]
    return portfoliosList


def getStocksFromPortfolio(PortfolioID):
    result = []
    for stock in StockPortfolioModel.objects.filter(Portfolio_id = PortfolioID):
        cStock = Stock(stock.tick, stock.priceRUB,  stock.amount, stock.industry, stock.dateBuying)
        result += [cStock]
    return result

