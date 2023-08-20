from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .operationsWithModels import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView

@login_required
def index(request):
    userID = getCurrentUser(request)
    data = {'title': "SMD",
            "titlePage": "Главная",
            "portfolioForm": StockPortfolioForm(), 
            "stockForm": StockForm(),
            "isAnyPortfolioCreated": StockPortfolioModel.objects.all().__len__() > 0,
            "userPortfolios": StockPortfolioModel.objects.filter(user = userID),
            "isError": False,
            "textError": []}

    if request.method == "POST":
        if data["isAnyPortfolioCreated"]:
            tick = request.POST.get("tick").upper()
            if not tick.isalpha():
                data["isError"] = True
                data["textError"] += ["TICK состоит только из латинских букв"]
            priceRUB = request.POST.get("priceRUB")
            target = request.POST.get("target")
            if priceRUB == target:
                data["isError"] = True
                data["textError"] += ["Цель должна отличаться от цены покупки"]
            
            stop = request.POST.get("stop")
            if priceRUB == stop:
                data["isError"] = True
                data["textError"] += ["Стоп приказ должен отличаться от цены покупки"]
            if stop == target:
                data["isError"] = True
                data["textError"] += ["Цель должна отличаться от стоп приказа"]
            reasonBuy = request.POST.get("reasonBuy")
            amount = request.POST.get("amount")
            industry = request.POST.get("industry")
            if industry == "":
                industry = "Без отрасли"
            dateBuying = request.POST.get("dateBuying")
            portfolio = request.POST.get("portfolio")
            portfolio = StockPortfolioModel.objects.get(user=userID, name = portfolio)
            if not isItPossibleToAddStockToPortfolio(userID, int(priceRUB), int(amount), portfolio):
                data["isError"] = True
                data["textError"] += [f"Вы не можете добавить данную акцию с такой ценой в портфель '{portfolio.name}', т.к. в нем не хватает свободных средств"]
            if data["isError"]:
                data["stockForm"] = StockForm(request.POST)
                return render(request, "home/index.html", context=data)
            cStock = StockModel(tick=tick, priceRUB = priceRUB, amount = amount, industry=industry, dateBuying = dateBuying, 
                                Portfolio = portfolio, user = userID, target = target, stop = stop, reasonBuy = reasonBuy)
            cStock.save()
            return redirect(f"/portfolios/show-portfolio/{portfolio.id}")
        else:
            name = request.POST.get("portfolioName")
            money = request.POST.get("portfolioMoney")
            comission = request.POST.get("portfolioComission")
            try:
                StockPortfolioModel.objects.get(name = name, user = userID)
                data["isError"] = True
                data["textError"] = "Портфель с таким названием уже существует"
            except:
                cPortfolio = StockPortfolioModel.objects.create(name = name, user = userID, money=money, comission = comission)
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
            "titlePage": "Зарегистрироваться",
            "isError": False,
            "textError": []}
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        email = form.data["email"]
        try:
            User.objects.get(email = email)
            data["isError"] = True
            data["textError"] += ["Пользователь с данной эл. почтой уже существует"]
            data["form"] = form
            return render(request, "home/sign-up.html", context=data)
        except ObjectDoesNotExist:
            pass
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
        if request.method == "POST":
            a = ["Сортировка по дате (сначала старые)", 
                 "Сортировка по дате (сначала новые)",
                 "Сортировка по тикеру (по алфавиту)",
                 "Сортировка по тикеру (по алфавиту в обратном порядке)",
                 "Сортировка по цене открытия (по возрастанию)",
                 "Сортировка по цене открытия (по убыванию)",
                 "Сортировка по цене закрытия (по возрастанию)",
                 "Сортировка по цене закрытия (по убыванию)",]
            
            dict = {}
            for i in range(len(a)):
                dict[a[i]] = i

            sort = request.POST.get("sort")

            isMonth = request.POST.get("month")

            isYear = request.POST.get("year")
            sort = dict[sort]
            if isMonth:
                period = "month"
            elif isYear:
                period = "year"
            else:
                period = None
            data["posts"] = getAllUserPosts(userID, sort, period)
            data["isMonth"] = isMonth
            data["isYear"] = isYear
            data["sort"] = sort
        else:
            data["posts"] = getAllUserPosts(userID, 1)
            data["sort"] = 1
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
        portfolioComission = request.POST.get("portfolioComission")
        try: 
            StockPortfolioModel.objects.get(name = portfolioName, user = userID)
            data["isError"] = True
            data["textError"] += ["Портфель с таким названием уже существует"]
        except:
            cPortfolio = StockPortfolioModel(name = portfolioName, user = userID, money = portfolioMoney, comission = portfolioComission)
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
            # try:
            #     priceRUB = float(priceRUB)
            #     if priceRUB < 0:
            #         raise KeyError
            #     stock.priceRUB = priceRUB
            # except KeyError:
            #     data["isError"] = True
            #     data["textError"] += ["Значение цены должно быть положительным"]
            # except:
            #     data["isError"] = True
            #     data["textError"] += ["В поле цены необходимо ввести число."]
            if isNum(priceRUB):
                priceRUB = isNum(priceRUB)
                stock.priceRUB = priceRUB
            else:
                data["isError"] = True
                data["textError"] += ["В поле цены покупки необходимо ввести число."]
            if priceRUB <= 0:
                data["isError"] = True
                data["textError"] += ["Цена покупки должна быть положительной"]

            target = request.POST.get('target').replace(",", ".")
            # try:
            #     target = float(target)
            #     if target < 0:
            #         raise KeyError
            #     stock.target = target
            # except KeyError:
            #     data["isError"] = True
            #     data["textError"] += ["Значение цели должно быть положительным"]
            # except:
            #     data["isError"] = True
            #     data["textError"] += ["В поле цели необходимо ввести число."]

            if isNum(target):
                target = isNum(target)
                stock.target = target
            else:
                data["isError"] = True
                data["textError"] += ["В поле цели необходимо ввести число."]
            if target <= 0:
                data["isError"] = True
                data["textError"] += ["Цель должна быть положительной"]

            stop = request.POST.get('stop').replace(",", ".")
            # try:
            #     stop = float(stop)
            #     if stop < 0:
            #         raise KeyError
            #     stock.stop = stop
            # except KeyError:
            #     data["isError"] = True
            #     data["textError"] += ["Значение стоп приказа должно быть положительным"]
            # except:
            #     data["isError"] = True
            #     data["textError"] += ["В поле стоп приказа необходимо ввести число."]  
            if isNum(stop):
                stop = isNum(stop)
                stock.stop = stop
            else:
                data["isError"] = True
                data["textError"] += ["В поле стоп-приказа  необходимо ввести число."]
            if stop <= 0:
                data["isError"] = True
                data["textError"] += ["Стоп-приказ должен быть положительным"]


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
                "textError": [],
                "industryPercent": getIndustryPortfolioPercentage(portfolio)}
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
            
            if isNum(portfolioMoney):
                portfolioMoney = float(portfolioMoney)
                if portfolioMoney < data["portfolioStats"]["ReservedMoney"] or portfolioMoney <= 0:
                    data["isError"] = True
                    data["textError"] += ["Сумма средств портфеля должна быть больше суммы вложенных денег"]
            else:
                data["isError"] = True
                data["textError"] += ["Средствами портфеля должно быть число"]

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
    data = {"title": "История",
            "titlePage": "История сделок",}
    userID = getCurrentUser(request)
    if request.method == "POST":
            a = ["Дата продажи (сначала недавние)", 
                 "Дата продажи (сначала старые)",
                 "Дата покупки (сначала недавние)",
                 "Дата покупки (сначала старые)",
                 "По портфелю",
                 "По итогу сделки (по возрастанию)",
                 "По итогу сделки (по убыванию)",
                 "По отрасли",]
            
            dict = {}
            for i in range(len(a)):
                dict[a[i]] = i

            sort = request.POST.get("sort")

            isMonth = request.POST.get("month")

            isYear = request.POST.get("year")
            sort = dict[sort]
            if isMonth:
                period = "month"
            elif isYear:
                period = "year"
            else:
                period = None
            data["isMonth"] = isMonth
            data["isYear"] = isYear
    else:
        sort = 0
        period = None
    data["sort"] = sort
    data["stocks"] = getAllSoldStocks(userID, sort, period)
    print(sort)
    
    return render(request, "home/history.html", context=data)

@login_required
def showStockPage(request, id):
    userID = getCurrentUser(request)
    stock = StockModel.objects.get(id = id)
    info = getStockInfo(stock)
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

@login_required
def editPost(request, id):
    userID = getCurrentUser(request)
    post = DiaryPostModel.objects.get(id = id)
    if userID == post.user:
        data = {"title": "Редактировать запись",
                "titlePage": "Редактировать запись",
                "form": DiaryPostForm,
                "post": post,
                "date": str(post.date),
                "textError": [],
                "isError": False}
        if request.method == "POST":
            priceOpen = request.POST.get("priceOpen".replace(",", "."))
            if isNum(priceOpen):
                priceOpen = isNum(priceOpen)
                post.priceOpen = priceOpen
            else:
                data["isError"] = True
                data["textError"] += ["В поле цены открытия необходимо ввести число."]
            if priceOpen <= 0:
                data["isError"] = True
                data["textError"] += ["Цена открытия должна быть положительной"]

            priceClose = request.POST.get("priceClose".replace(",", "."))
            if isNum(priceClose):
                priceClose = isNum(priceClose)
                post.priceClose = priceClose
            else:
                data["isError"] = True
                data["textError"] += ["В поле цены закрытия необходимо ввести число."]
            if priceClose <= 0:
                data["isError"] = True
                data["textError"] += ["Цена закрытия должна быть положительной"]
            
            priceMin = request.POST.get("priceMin".replace(",", "."))
            if isNum(priceMin):
                priceMin = isNum(priceMin)
                post.priceMin = priceMin
            else:
                data["isError"] = True
                data["textError"] += ["В поле минимальной цены необходимо ввести число."]
            if priceMin <= 0:
                data["isError"] = True
                data["textError"] += ["Минимальная цена должна быть положительной"]
            
            priceMax = request.POST.get("priceMax".replace(",", "."))
            if isNum(priceMax):
                priceMax = isNum(priceMax)
                post.priceMax = priceMax
            else:
                data["isError"] = True
                data["textError"] += ["В поле максимальной цены необходимо ввести число."]
            if priceMax <= 0:
                data["isError"] = True
                data["textError"] += ["Максимальной цена должна быть положительной"]
            
            
            if min(priceMin, priceClose, priceMax, priceOpen) != priceMin:
                data["isError"] = True
                data["textError"] += ["Минимальная цена должна быть меньше всех цен за день"]
            if max(priceMin, priceClose, priceMax, priceOpen) != priceMax:
                data["isError"] = True
                data["textError"] += ["Максимальная цена должна быть больше всех цен за день"]
           

            date = request.POST.get("date")
            try:
                date = map(int, date.split("-")) if "-" in date else map(int, date.split("."))[::-1]
                date = datetime.date(*date)
                post.date = date
            except:
                data["isError"] = True
                data["textError"] += ["Неправильный формат даты"]

            post.msg = request.POST.get("msg")
            if not data["isError"]:
                post.save()
                return redirect("/diary")

        return render(request, "home/edit-post.html", context=data)
    return redirect("/diary")

@login_required
def deletePost(request, id):
    post = DiaryPostModel.objects.get(id = id)
    userID = getCurrentUser(request)
    if post.user == userID:
        post.delete()
    return redirect("/diary")


