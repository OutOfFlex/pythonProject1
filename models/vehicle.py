# Модель данных для легковых авто
class Vehicle:
    def __init__(self, power, power_type, engine_capacity, year, month, price, currency, engine_type):
        self.power = power  # мощность
        self.power_type = power_type  # квт/ч или л.с. kw/hp
        self.engine_capacity = engine_capacity  # объм двигателя в кубических сантиметрах (1л = 1000см)
        self.year = year  # год производства
        self.month = month  # месяц производства
        self.price = price  # стоимость автомобиля
        self.currency = currency  # валюта - рубль в формате  ISO 4217 : rub, cny, eur, usd
        self.engine_type = engine_type  # euv - электродвигатель, ice - ДВС, dis - Дизель, hyb - гибрид
