import datetime


class Stock:
    def __init__(self, id: int, tick: str,  priceRUB: float,  amount: int = 1, industry: str = None, dateBuying: datetime.date = datetime.date.today()):
        self._amount = amount
        self._priceRUB = priceRUB
        self._tick = tick
        self._industry = industry
        self._dateBuying = dateBuying
        self._id = id

    @property
    def priceRUB(self) -> int:
        return self._priceRUB
    @property
    def id(self) -> int:
        return self._id
    @property
    def tick(self) -> str:
        return self._tick

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def industry(self) -> str:
        return self._industry

    @property
    def dateBuying(self):
        return self._dateBuying

    def __str__(self):
        s = f"{self._tick}:\n \tЦена за 1 акцию = {self._priceRUB} руб\n \tКоличество = {self.amount}\n \tДата покупки: {self._dateBuying.isoformat()}\n"
        if self._industry:
            s += f"\tОтрасль: {self._industry} \n"
        return s


class StockPortfolio:
    def __init__(self, name ,stocks: list = []) -> None:
        self._stocks = stocks
        self._name = name
        self._sumStocksRub = self.getSumStocks()
        self._amountOfStocks = self.getAmount()

    def getAmount(self):
        amount = {}
        if self._stocks:
            for stock in self._stocks:
                amount[stock.tick] = stock.amount
        return amount

    def getSumStocks(self) -> float:
        res = 0
        if self.stocks:
            for stock in self.stocks:
                res += stock.priceRUB
        return res

    def purchaseStock(self, stock: Stock):
        if stock.amount <= 0 or stock.priceRUB <= 0:
            raise ValueError
        self._sumStocksRub = stock.amount * stock.priceRUB \
            if not self._sumStocksRub \
            else self._sumStocksRub + stock.amount * stock.priceRUB

        self._stocks += [stock]

        self._amountOfStocks[stock.tick] = stock.amount + self._amountOfStocks[stock.tick] \
            if stock.tick in self._amountOfStocks \
            else stock.amount

    def sellStock(self, stock: Stock):
        if stock.amount <= 0 or stock.amount > self.amount or stock.priceRUB <= 0:
            raise ValueError
        if not self._sumStocksRub:
            raise "There is no stock to sell"
        if stock not in self._stocks:
            raise "Portfolio doesn't contain this stock"
        self._sumStocksRub -= stock.amount * stock.priceRUB
        self._amountOfStocks[stock] -= stock.amount

    @property
    def stocks(self):
        return self._stocks
    @property
    def name(self):
        return self._name
    def name(self, value):
        self._name = value

    def setStocks(self, stocks):
        self._stocks = stocks

    def __str__(self):
        s = "В портфеле:\n"
        counter = 1
        for stock in self._stocks:
            s += f"({counter}) " + str(stock)
            counter += 1
        return s


def main():
    port = StockPortfolio()
    yndx = Stock("YNDX", 2224, port, industry="IT")
    print(yndx.dateBuying)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    port.purchaseStock(yndx)
    print(port)


if __name__ == '__main__':
    main()
