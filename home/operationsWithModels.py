from .models import *
from .StockPortfolio import *


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
    portfolio = StockPortfolioModel.objects.get(id = PortfolioID)
    for stock in StockModel.objects.filter(Portfolio = portfolio):
        cStock = Stock(stock.tick, stock.priceRUB,  stock.amount, stock.industry, stock.dateBuying)
        result += [cStock]
    return result


def getStocksFromUserPortfolios(UserID = 1):
    result = {}
    portfolios = getUserPortfolios(UserID)
    for portfolioName, portfolioID in portfolios:
        result[portfolioID] = getStocksFromPortfolio(portfolioID)
    return result


def getUniqueUserStockTicks(UserID = 1):
    result = list(UniqUserStockModel.objects.filter(user = UserID).values_list("tick", flat=True))
    result.sort()
    return result


def getAllUserPosts(UserID = 1):
    posts = DiaryPostModel.objects.filter(user = UserID)
    return posts