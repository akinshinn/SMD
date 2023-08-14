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


def getStocksFromUserPortfolios(UserID):
    result = {}
    portfolios = StockPortfolioModel.objects.filter(user = UserID)
    for portfolio in portfolios:
        result[portfolio.id] = StockModel.objects.filter(Portfolio = portfolio)
    return result


def getAllUserPosts(UserID):
    posts = DiaryPostModel.objects.filter(user = UserID)
    return posts


def getCurrentUser(request):
    return request.user.id


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
    total = 0 
    totalMonth = 0
    totalYear = 0
    today = datetime.date.today()
    stocks = HistoryModel.objects.filter(portfolio = portfolio)
    for stock in stocks:
        info = getSoldStockInfo(stock)
        total += info["finalTotal"]
        totalMonth += info["finalTotal"] if (stock.dateSell.year == today.year and stock.dateSell.month == today.month) else 0
        totalYear += info["finalTotal"] if stock.dateSell.year == today.year else 0 
    maxLossesMonth = totalMonth
    stocks = StockModel.objects.filter(Portfolio = portfolio)
    for stock in stocks:
        info = getStockInfo(stock)
        maxLossesMonth += info["maxLoss"]
    result = {"freeMoney": freeMoney,
              "percentFreeMoney": freeMoney / portfolio.money * 100,
              "ReservedMoney": reservedMoney,
              "percentReservedMoney": reservedMoney / portfolio.money * 100,
              "twoPercent": portfolio.money * 0.02,
              "sixPercent": portfolio.money * 0.06,
              "total": total,
              "totalMonth": totalMonth,
              "totalYear": totalYear,
              "totalMonthPercent": totalMonth / portfolio.money * 100,
              "totalYearPercent": totalYear / portfolio.money * 100,
              "totalPercent": total / portfolio.money * 100,
              "maxLossesMonth": maxLossesMonth}
    return result


def getStockInfo(stock, commission = 0.003):
    risk = stock.stop - stock.priceRUB
    profit = stock.target - stock.priceRUB
    commissionMax = stock.target * stock.amount * commission
    commissionMin = stock.stop * stock.amount * commission
    result = {"profitPercent": profit / stock.priceRUB * 100,
              "risksPercent" : risk / stock.priceRUB * 100, 
              "slippage":   stock.priceRUB * stock.amount * commission,
              "commissionMin": commissionMin,
              "commissionMax": commissionMax, 
              "risk": risk,
              "profit": profit,
              "portfolioPercent": stock.amount * stock.priceRUB / stock.Portfolio.money * 100,
              "maxLoss": -commissionMin + risk*stock.amount,
              "maxProfit": -commissionMax + profit*stock.amount,
              "riskToProfit": abs(risk/profit)}
    return result


def getSoldStockInfo(stock, commission = 0.003):
    total = stock.priceSell - stock.priceBuy
    totalPerStock = total - stock.priceSell * commission  - stock.priceBuy * commission
    finalTotal = totalPerStock * stock.amountSell
    result = {"total": total,
              "totalPerStock": totalPerStock,
              "finalTotal": finalTotal,}
    return result


def getStatsAllPortfolios(portfolios):
    sumPortfolios = 0
    diffMonthPortfolio = 0
    diffYearPortfolio = 0 

    for portfolio in portfolios:
        stats = getPortfolioStats(portfolio)
        sumPortfolios += portfolio.money
        diffMonthPortfolio += stats["totalMonth"]
        diffYearPortfolio += stats["totalYear"]
    result = {"totalMonthPortfolio": diffMonthPortfolio,
              "totalYearPortfolio": diffYearPortfolio,
              "totalMonthPercent": diffMonthPortfolio / sumPortfolios * 100,
              "totalYearPercent": diffYearPortfolio / sumPortfolios * 100,
              "sumPortfolios": sumPortfolios}
    return result