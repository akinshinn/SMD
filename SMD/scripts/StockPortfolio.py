from Stock import Stock


class StockPortfolio:
    def __init__(self, stocks: list = None) -> None:
        _stocks = stocks if stocks else None
        _sumStocksRub = 0

    @property
    def stocks(self):
        return self._stocks

    def setStocks(self, stocks):
        self._stocks = stocks


def main():
    pass


if __name__ == '__main__':
    main()
