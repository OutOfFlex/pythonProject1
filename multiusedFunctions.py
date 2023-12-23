import datetime
import currencies


currentTime = datetime.datetime.now()

# Расчёт таможенного сбора
def customs_fee(price):
    if price <= 200000:
        return 775
    elif price <= 450000:
        return 1550
    elif price <= 1200000:
        return 3100
    elif price <= 2700000:
        return 8530
    elif price <= 4200000:
        return 12000
    elif price <= 5500000:
        return 15500
    elif price <= 7000000:
        return 20000
    elif price <= 8000000:
        return 23000
    elif price <= 9000000:
        return 25000
    elif price <= 10000000:
        return 27000
    elif price > 10000000:
        return 30000
    else:
        return 0

# Проверка минимума пошлины
def customs_duty_check(customs_duty, customs_duty_minimum):
    if customs_duty < customs_duty_minimum:
        return customs_duty_minimum
    else:
        return customs_duty

# Акциз для электродвигателя
def customs_excise_euv(power):
    if power <= 90:
        return 0
    elif power <= 200:
        return 531 * power
    elif power <= 300:
        return 869 * power
    elif power <= 400:
        return 1482 * power
    elif power <= 500:
        return 1534 * power
    elif power < 500:
        return 1584 * power
    else:
        return 0

# Расчёт таможенной пошлины для электромобиля
def customs_duty_euv(price):
    return price * 0.15

# Костыльный расчёт ПОЛНЫХ лет с месяца производства
def check_manufactured_date(year, month):
    output_year = currentTime.year - year
    if month == 13:
        month = 5
    if currentTime.month < month:
        return output_year - 1
    else:
        return output_year

# Перевод цены в рубли
def price_to_rub(price, currency):
    if currency == "cny":
        return price * currencies.cny_rub
    elif currency == "usd":
        return price * currencies.usd_rub
    elif currency == "eur":
        return price * currencies.eur_rub
    elif currency == "yen":
        return price * currencies.yen_rub
    elif currency == "rub":
        return price
    else:
        return 0

# Перевод квт/ч в л.с.
def power_to_type(vehicle):
    if vehicle.power_type == "kw":
        vehicle.power *= 1.36
        vehicle.power_type = "hp"