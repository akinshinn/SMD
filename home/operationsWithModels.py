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


def getAllUserPosts(UserID, sort, period = None):
    # 0 - сначала старые, 1 - новые, 2 - алфавит, 3 - обратный алфавит
    # 4- по возр цены откр, 5 - по убыв цены откр, 6 - по возр цены закр,
    # 7 - по убыв цены закр
    if sort == 0:
        posts = DiaryPostModel.objects.filter(user = UserID)
    elif sort == 1:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("-date")
    elif sort == 2:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("stockTick")
    elif sort == 3:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("-stockTick")
    elif sort == 4:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("priceOpen")
    elif sort == 5:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("-priceOpen")
    elif sort == 6:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("priceClose")
    else:
        posts = DiaryPostModel.objects.filter(user = UserID).order_by("-priceClose")
    if period:
        today = datetime.date.today()
        filtered_posts = []
        if period == "month":
            for post in posts:
                post_date = post.date
                if post_date.month == today.month and post_date.year == today.year:
                    filtered_posts += [post]
        else:
            for post in posts:
                post_date = post.date
                if post_date.year == today.year:
                    filtered_posts += [post]
        return filtered_posts
    return posts

def getAllSoldStocks(UserID, sort = 1, period = None):
    # 0 - дата продажи недавние, 1 - дата продажи старые
    # 2 - дата покупки недавние, 3 - дата покупки старые, 
    # 4 - портфель, 5 - итог сделаки возр, 6 - итог сделки убыв
    # 7 - отрасль
    stocks = HistoryModel.objects.filter(user = UserID)
    if sort == 0:
        stocks = stocks.order_by("-dateSell")
    elif sort == 1:
        stocks = stocks.order_by("dateSell")
    elif sort == 2:
        stocks = stocks.order_by("-dateBuy")
    elif sort == 3:
        stocks = stocks.order_by("dateBuy")
    elif sort == 4:
        stocks = stocks.order_by("portfolio")
    elif sort == 5:
        filtered = []
        tmp = []
        for stock in stocks:
            info = getSoldStockInfo(stock)
            total = info["finalTotal"]
            tmp += [total]
        tmp.sort()
        for stock in stocks:
            cTotal = getSoldStockInfo(stock)["finalTotal"]
            for total in tmp:
                if total == cTotal:
                    filtered += [stock]
                    tmp.remove(total)
        stocks = filtered  
    elif sort == 6:
        filtered = []
        tmp = []
        for stock in stocks:
            info = getSoldStockInfo(stock)
            total = info["finalTotal"]
            tmp += [total]
        tmp = sorted(tmp, reverse=True)
        print(tmp)
        for stock in stocks:
            cTotal = getSoldStockInfo(stock)["finalTotal"]
            for total in tmp:
                if total == cTotal:
                    filtered += [stock]
                    tmp.remove(total)
        stocks = filtered 
    else:
        stocks = stocks.order_by("industry")
    result = []
    if period == "month":
        for stock in stocks:
            date_stock = stock.dateSell
            today = datetime.date.today()
            if date_stock.year == today.year and date_stock.month == today.month:
                result += [[stock, getSoldStockInfo(stock)]]
    elif period == "year":
        for stock in stocks:
            date_stock = stock.dateSell
            today = datetime.date.today()
            if date_stock.year == today.year:
                result += [[stock, getSoldStockInfo(stock)]]
    else:
        for stock in stocks:
            result += [[stock, getSoldStockInfo(stock)]]
    return result


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


def getStockInfo(stock):
    commission = stock.Portfolio.comission / 100
    risk = stock.stop - stock.priceRUB
    profit = stock.target - stock.priceRUB
    print(risk, profit)
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


def getSoldStockInfo(stock):
    commission = stock.portfolio.comission / 100
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


def isNum(number:str):
    # num - str
    number = number.replace(",", ".")
    try:
        number = float(number)
    except:
        return False
    return number
    

def getIndustryPortfolioPercentage(portfolio):
    industryPercent = {}
    stocks = StockModel.objects.filter(Portfolio = portfolio)
    for stock in stocks:
        info = getStockInfo(stock)
        if stock.industry not in industryPercent:
            industryPercent[stock.industry] = info["portfolioPercent"]
        else:
            industryPercent[stock.industry] += info["portfolioPercent"]
    
    return industryPercent