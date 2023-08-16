from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .operationsWithModels import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

@login_required
def index(request):
    userID = getCurrentUser(request)
    data = {'title': "SMD",
            "titlePage": "Главная",
            "portfolioForm": StockPortfolioForm(), "stockForm": StockForm(),
            "isAnyPortfolioCreated": StockPortfolioModel.objects.all().__len__() > 0,
            "userPortfolios": StockPortfolioModel.objects.filter(user = userID),
            "isError": False,
            "textError": []}

    if request.method == "POST":
        if data["isAnyPortfolioCreated"] and not request.POST.get('portfolioName'):
            tick = request.POST.get("tick").upper()
            if not tick.isalpha():
                data["isError"] = True
                data["textError"] += ["TICK состоит только из латинских букв"]
            priceRUB = request.POST.get("priceRUB")
            target = request.POST.get("target")
            stop = request.POST.get("stop")
            reasonBuy = request.POST.get("reasonBuy")
            amount = request.POST.get("amount")
            industry = request.POST.get("industry", "Без отрасли")
            dateBuying = request.POST.get("dateBuying")
            portfolio = request.POST.get("portfolio")
            portfolio = StockPortfolioModel.objects.get(user=userID, name = portfolio)
            if not isItPossibleToAddStockToPortfolio(userID, int(priceRUB), int(amount), portfolio):
                data["isError"] = True
                data["textError"] += [f"Вы не можете добавить данную акцию с такой ценой в портфель '{portfolio.name}', т.к. в нем не хватает свободных средств"]
            if data["isError"]:
                return render(request, "home/index.html", context=data)
            cStock = StockModel(tick=tick, priceRUB = priceRUB, amount = amount, industry=industry, dateBuying = dateBuying, 
                                Portfolio = portfolio, user = userID, target = target, stop = stop, reasonBuy = reasonBuy)
            cStock.save()
            return redirect(f"/portfolios/show-portfolio/{portfolio.id}")
        else:
            name = request.POST.get("portfolioName")
            money = request.POST.get("portfolioMoney")
            try:
                StockPortfolioModel.objects.get(name = name, user = userID)
                data["isError"] = True
                data["textError"] = "Портфель с таким названием уже существует"
            except:
                cPortfolio = StockPortfolioModel.objects.create(name = name, user = userID, money=money)
                data["isAnyPortfolioCreated"] = True
                return redirect(f"/portfolios/show-portfolio/{cPortfolio.id}")
    return render(request, 'home/index.html', context=data)

@login_required
def profile(request):
    user = request.user
    form = EditProfileForm()
    titlePage = user.username if not user.first_name else user.first_name
    data = {"title": user.username,
            "titlePage": f"Здравствуйте, {titlePage}",
            "portfolios": StockPortfolioModel.objects.filter(user = user.id),
            "stats": getStatsAllPortfolios(StockPortfolioModel.objects.filter(user = user.id)) if StockPortfolioModel.objects.filter(user = user.id) else None}
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.save()
        return redirect("/profile")
    else:         
        data["form"] = form
    return render(request, 'home/profile.html', context=data)

def about(request):
    data = {
        "title": "О проекте",
        "titlePage": "О проекте"
    }
    return render(request, 'home/about.html', context=data)

def logout_request(request):
    logout(request)
    return redirect("/login")

def login_request(request):
    data = {"title": "Войти",
            "titlePage": "Войти",}
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
    data["form"] = form
    return render(request, 'home/login.html', context=data)


def sign_up(request):
    data = {"title": "Зарегистрироваться",
            "titlePage": "Зарегистрироваться"}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("/")
    else: 
        form = UserRegistrationForm()
    data["form"] = form
    
    return render(request, "home/sign-up.html", context=data)

@login_required
def diary(request):
    userID = getCurrentUser(request)
    data = {'title': "Дневник",
            "titlePage": "Ваш Дневник",
            "isPosted": DiaryPostModel.objects.filter(user = userID).__len__() > 0}
    if data["isPosted"]:
        data["posts"] = getAllUserPosts(userID)
    return render(request, "home/diary.html", context=data)

@login_required
def portfolios(request):
    userID = getCurrentUser(request)
    portfolios = StockPortfolioModel.objects.filter(user = userID)
    stocks = getStocksFromUserPortfolios(userID)
    portfoliosAndStocks = []
    for portfolio in portfolios:
        portfoliosAndStocks += [[[portfolio.name, portfolio.id, portfolio.money], getPortfolioStats(portfolio), stocks[portfolio.id]]]
    data = {'title': "Портфели",
            "titlePage": "Ваши портфели",
            "portfolios": portfolios,
            "portfoliosAndStocks": portfoliosAndStocks,
            "portfolioForm": StockPortfolioForm,
            "isError": False,
            "textError": [],}
    if request.method == "POST":
        portfolioName = request.POST.get("portfolioName")
        portfolioMoney = request.POST.get("portfolioMoney")
        try: 
            StockPortfolioModel.objects.get(name = portfolioName, user = userID)
            data["isError"] = True
            data["textError"] += ["Портфель с таким названием уже существует"]
        except:
            cPortfolio = StockPortfolioModel(name = portfolioName, user = userID, money = portfolioMoney)
            cPortfolio.save()
            return redirect("/portfolios")
            
    return render(request, "home/portfolios.html", context=data)

@login_required
def addPost(request):
    userID = getCurrentUser(request)
    userUniqStocks = set(sorted([stock.tick for stock in StockModel.objects.filter(user = userID)]))
    data = {'title': "Добавить запись",
            "titlePage": "Добавить запись",
            'form': DiaryPostForm(), 
            "userUniqStocks": userUniqStocks,
            "isPostCreated": False,
            "textMsg": "",
            "isError": "",
            "textError": []}
    if request.method == "POST":
        stockTick = request.POST.get("uniqStocks")
        priceOpen = float(request.POST.get("priceOpen"))
        priceClose = float(request.POST.get("priceClose"))
        priceMax = float(request.POST.get("priceMax", "NULL"))
        priceMin = float(request.POST.get("priceMin", "NULL"))
        date = request.POST.get("date")
        post = request.POST.get("post")
        
        cPost = DiaryPostModel(stockTick = stockTick, priceOpen=priceOpen, priceClose=priceClose, priceMax=priceMax, priceMin = priceMin,
                       date = date, msg=post, user = userID)
        data["isPostCreated"] = True
        data["textMsg"] = stockTick
        if priceMin != "NULL":
            if min(priceMin, priceClose, priceMax, priceOpen) != priceMin:
                data["isError"] = True
                data["textError"] += ["Минимальная цена должна быть меньше всех цен за день"]
        if priceMax != "NULL":
            if max(priceMin, priceClose, priceMax, priceOpen) != priceMax:
                data["isError"] = True
                data["textError"] += ["Максимальная цена должна быть больше всех цен за день"]
        if not data["isError"]:
            cPost.save()
    return render(request, "home/add-post.html", context=data)

@login_required
def editStockPage(request, id):
    userID = getCurrentUser(request)
    stock = StockModel.objects.get(id = id)

    data = {"stock": stock,
            "title": "Редактировать акцию",
            "titlePage": "Редактировать акцию",
            "form": EditStockForm(request.POST),
            "userPortfolios": StockPortfolioModel.objects.filter(user = userID),
            "isError": False,
            "textError": [],
            "date" : str(stock.dateBuying)}
    if stock.user == userID:
        if request.method == "POST":
            stock.tick = request.POST.get("tick").upper()

            priceRUB = request.POST.get('priceRUB').replace(",", ".")
            try:
                priceRUB = float(priceRUB)
                if priceRUB < 0:
                    raise KeyError
                stock.priceRUB = priceRUB
            except KeyError:
                data["isError"] = True
                data["textError"] += ["Значение цены должно быть положительным"]
            except:
                data["isError"] = True
                data["textError"] += ["В поле цены необходимо ввести число."]

            target = request.POST.get('target').replace(",", ".")
            try:
                target = float(target)
                if target < 0:
                    raise KeyError
                stock.target = target
            except KeyError:
                data["isError"] = True
                data["textError"] += ["Значение цели должно быть положительным"]
            except:
                data["isError"] = True
                data["textError"] += ["В поле цели необходимо ввести число."]

            stop = request.POST.get('stop').replace(",", ".")
            try:
                stop = float(stop)
                if stop < 0:
                    raise KeyError
                stock.stop = stop
            except KeyError:
                data["isError"] = True
                data["textError"] += ["Значение стоп приказа должно быть положительным"]
            except:
                data["isError"] = True
                data["textError"] += ["В поле стоп приказа необходимо ввести число."]  

            amount = request.POST.get("amount")
            if int(amount) == float(amount):
                stock.amount = int(amount)
            else:
                data["isError"] = True
                data["textError"] += ["Значение количества акций должно быть натуральным"]
            
            stock.industry = request.POST.get("industry")
            dateBuying = request.POST.get("dateBuying")
            try:
                dateBuying = map(int, dateBuying.split("-")) if "-" in dateBuying else map(int, dateBuying.split("."))[::-1]
                dateBuying = datetime.date(*dateBuying)
                stock.dateBuying = dateBuying
            except:
                data["isError"] = True
                data["textError"] += ["Неправильный формат даты"]
            portfolio = request.POST.get("portfolio")
            portfolio = StockPortfolioModel.objects.get(user = userID, name = portfolio)
            stock.Portfolio = portfolio
            if not isItPossibleToAddStockToPortfolio(userID, stock.priceRUB, stock.amount, portfolio):
                data["isError"] = True
                data["textError"] += ["Невозможно добавить в портфель данную акцию, т.к. в нем не хватает свободных средств"]
            if data["isError"]:
                return render(request, "home/edit-stock.html", context=data)
            stock.reasonBuy = request.POST.get("reasonBuy")
            stock.save()
            return redirect("/portfolios")     
    else:
        return redirect("/portfolios")       
        
    return render(request, "home/edit-stock.html", context=data)

@login_required
def deleteStockPage(request, id):
    userID = getCurrentUser(request)
    cStock = StockModel.objects.get(id=id)
    if cStock.user == userID:
        cStock.delete()

    return redirect("/portfolios")

@login_required
def deletePortfolioPage(request, id):
    userID = getCurrentUser(request)
    cPortfolio = StockPortfolioModel.objects.get(id = id)
    if cPortfolio.user == userID:
        cPortfolio.delete()
    return redirect("/portfolios")

@login_required
def showPortfolioPage(request, id):
    userID = getCurrentUser(request)
    portfolio = StockPortfolioModel.objects.get(id = id)
    stocks = StockModel.objects.filter(Portfolio = portfolio)
    if userID == portfolio.user:
        data = {"portfolio": portfolio,
                "title": portfolio.name,
                "titlePage": portfolio.name,
                "portfolioStats": getPortfolioStats(portfolio),
                "portfolio": portfolio,
                "stocks": stocks,
                "portfolioForm": StockPortfolioForm,
                "isError": False,
                "textError": []}
        if request.method == "POST":
            portfolioName = request.POST.get("portfolioName")
            try:
                portfolioGet = StockPortfolioModel.objects.get(name=portfolioName)
                if portfolioGet.id != portfolio.id:
                    data["isError"] = True
                    data["textError"] += ["Портфель с таким названием уже существует"]
            except ObjectDoesNotExist:
                portfolio.name = portfolioName
            portfolioMoney = request.POST.get("portfolioMoney").replace(",", ".")
            try:
                portfolioMoney = float(portfolioMoney)
            except:
                data["isError"] = True
                data["textError"] += ["Средствами портфеля должно быть только положительное число"]
            if portfolioMoney < data["portfolioStats"]["ReservedMoney"] or portfolioMoney <= 0:
                data["isError"] = True
                data["textError"] += ["Сумма средств портфеля должна быть больше суммы вложенных денег"]
            if not data["isError"]:
                portfolio.money = portfolioMoney
                portfolio.name = portfolioName
                portfolio.save()
                return redirect(f"/portfolios/show-portfolio/{portfolio.id}")

        return render(request, "home/show-portfolio.html", context=data)
    else:
        return redirect("/")

@login_required
def historyPage(request):
    userID = getCurrentUser(request)
    stocks = HistoryModel.objects.filter(user = userID).order_by("-dateSell")
    stocks = [[stock, getSoldStockInfo(stock)] for stock in stocks]
    data = {"title": "История",
            "titlePage": "История сделок",
            "stocks": stocks}
    return render(request, "home/history.html", context=data)

@login_required
def showStockPage(request, id):
    userID = getCurrentUser(request)
    stock = StockModel.objects.get(id = id)
    info = getStockInfo(stock, 0.003)
    data = {"title": stock.tick,
            "titlePage": stock.tick,
            "stockInfo": info,
            "stock": stock,
            "sellForm": SellStockForm,
            "isError": False,
            "textError": []}
    if request.method == "POST":
        priceSell = float(request.POST.get("priceSell"))
        amountSell = int(request.POST.get("amountSell"))
        
        if amountSell > stock.amount:
            data["isError"] = True
            data["textError"] += ["Количество продажи должно быть меньше количества текущей акции"]
        
        reasonSell = request.POST.get("reasonSell")
        if data["isError"]:
            return render(request, "home/show-stock.html", context=data)

        cHistoryStock = HistoryModel(tick = stock.tick, priceBuy = stock.priceRUB, 
                                    priceSell = priceSell, reasonSell = reasonSell,
                                    reasonBuy = stock.reasonBuy, dateBuy = stock.dateBuying,
                                    dateSell = datetime.date.today(), industry = stock.industry,
                                    portfolio = stock.Portfolio, amountSell = amountSell,
                                    user = userID)
        cHistoryStock.save()
        info = getSoldStockInfo(cHistoryStock)
        stock.Portfolio.money += info["finalTotal"]
        stock.Portfolio.save()
        if amountSell < stock.amount:
            stock.amount -= amountSell
            stock.save()
            
        else:
            return redirect(f"/delete/{stock.id}")
        return redirect(f"/show-stock/{stock.id}")
    return render(request, "home/show-stock.html", context=data)

@login_required
def deleteSoldStock(request, id):
    userID = getCurrentUser(request)
    stock = HistoryModel.objects.get(id = id)
    if stock.user == userID:
        stock.delete()
    return redirect("/history")

@login_required
def change_password(request):
    userID = getCurrentUser(request)
    user = User.objects.get(id = userID)

    data = {"title": "Сменить пароль",
            "titlePage": "Сменить пароль",
            "errors": [],
            "success": ""}
    if request.method == "POST":
        oldPassword = request.POST.get("oldPassword")
        if user.check_password(oldPassword):
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            print(password1)
            if password1 == password2 and password1:
                user.set_password(password1)
                user.save()
                data["success"] = ["Пароль успешно изменён!"]
            else:
                data["errors"] += ["Новый пароль не совпадает с подтверждением"]
        else:
            data["errors"] += ["Введеный пароль не совпадает с текущим"]
    return render(request, "home/change-password.html", context=data)


