from StockPortfolio import StockPortfolio


"""
Класс акции, в нем хранится имя, тик, отрасль, кол-во в портфеле
"""


class Stock:

    def __init__(self, name: str, amount: int, price: float, portfolio: StockPortfolio, tick: str = None, industry: str = None) -> None:
        _name = name
        _amount = amount
        _portfolio = portfolio
        _price = price
        _tick = tick if tick else None
        _industry = industry if industry else None

    def purchase(self, amountOfPurchase: int, price: float) -> None:
        if amountOfPurchase <= 0 or price <= 0:
            raise ValueError
        self._amount += amountOfPurchase

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> str:
        return self._price

    @property
    def tick(self) -> str:
        return self._tick

    @property
    def amount(self) -> int:
        return self._amount


def main():
    pass


if __name__ == '__main__':
    main()
