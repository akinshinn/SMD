from .models import *
from .StockPortfolio import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

def deleteAllFromModel(model):
    model.objects.all().delete()


def deleteAll():
    models = [StockPortfolioModel, StockModel]
    for model in models:
        deleteAllFromModel(model)


def getUserPortfolios(UserID):
    portfolios = StockPortfolioModel.objects.filter(user = UserID)
    portfoliosList = [[portfolio.name, portfolio.id] for portfolio in portfolios]
    return portfoliosList


def getStocksFromPortfolio(PortfolioID):
    result = []
    portfolio = StockPortfolioModel.objects.get(id = PortfolioID)
    for stock in StockModel.objects.filter(Portfolio = portfolio):
        cStock = Stock(stock.id, stock.tick, stock.priceRUB,  stock.amount, stock.industry, stock.dateBuying)
        result += [cStock]
    return result


def getStocksFromUserPortfolios(UserID):
    result = {}
    portfolios = getUserPortfolios(UserID)
    for portfolioName, portfolioID in portfolios:
        result[portfolioID] = getStocksFromPortfolio(portfolioID)
    return result


def getUniqueUserStockTicks(UserID):
    result = list(UniqUserStockModel.objects.filter(user = UserID).values_list("tick", flat=True))
    result.sort()
    return result


def getAllUserPosts(UserID):
    posts = DiaryPostModel.objects.filter(user = UserID)
    return posts


def getCurrentUser():
    return 1


def addUniqStock(stockTick, UserID):
    UniqUserStockModel.objects.get_or_create(tick = stockTick, user = UserID)


def delUniqStock(stockTick, UserID): 
    try:
        StockModel.objects.get(tick = stockTick, user = UserID)
    except ObjectDoesNotExist:
        UniqUserStockModel.objects.get(tick = stockTick, user = UserID).delete()


def getReservedMoneyPortfolio(userID, portfolio):
    stocks = StockModel.objects.filter(user = userID, Portfolio = portfolio)
    sumPortfolio = 0
    for stock in stocks:
        sumPortfolio += stock.priceRUB * stock.amount
    return sumPortfolio


def isItPossibleToAddStockToPortfolio(userID, cStockSum, cAmount, portfolio):
    sumStocksInPortfolio = getReservedMoneyPortfolio(userID, portfolio)
    return cStockSum * cAmount <= portfolio.money - sumStocksInPortfolio


def getPortfolioStats(portfolio):
    reservedMoney = getReservedMoneyPortfolio(portfolio.user, portfolio)
    freeMoney = portfolio.money - reservedMoney
    
    result = {"freeMoney": freeMoney,
              "percentFreeMoney": freeMoney / portfolio.money * 100,
              "ReservedMoney": reservedMoney,
              "percentReservedMoney": reservedMoney / portfolio.money * 100}
    return result


def deleteStock(id):
    cStock = StockModel.objects.get(id=id)
    cTick = cStock.tick
    cUser = cStock.user
    cStock.delete()
    delUniqStock(cTick, cUser)