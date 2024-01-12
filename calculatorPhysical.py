import currencies
from models.vehicle import *
from multiusedFunctions import *

# Акциз для физичекского лица
def customs_excise_physical(vehicle):
    if vehicle.engine_type == "euv":
        return customs_excise_euv(vehicle.power)
    else:
        return 0

# Расчёт таможенной пошлины для возраста авто менее 3-х лет физ. лицо
def customs_duty_physical3(vehicle):
    customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.48
    if price_to_rub(vehicle.price, vehicle.currency) < 8500 * currencies.eur_rub:
        customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.54
        customs_duty_minimum = vehicle.engine_capacity * 2.5 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif price_to_rub(vehicle.price, vehicle.currency) <= 16700 * currencies.eur_rub:
        customs_duty_minimum = vehicle.engine_capacity * 3.5 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif price_to_rub(vehicle.price, vehicle.currency) <= 42300 * currencies.eur_rub:
        customs_duty_minimum = vehicle.engine_capacity * 5.5 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif price_to_rub(vehicle.price, vehicle.currency) <= 84500 * currencies.eur_rub:
        customs_duty_minimum = vehicle.engine_capacity * 7.5 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif price_to_rub(vehicle.price, vehicle.currency) <= 169000 * currencies.eur_rub:
        customs_duty_minimum = vehicle.engine_capacity * 15 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif price_to_rub(vehicle.price, vehicle.currency) > 169000 * currencies.eur_rub:
        customs_duty_minimum = vehicle.engine_capacity * 20 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    else:
        return 0


# Расчёт таможенной пошлины для возраста авто от 3-х лет до 5 лет физ. лицо
def customs_duty_physical5(vehicle):
    if vehicle.engine_capacity <= 1000:
        return vehicle.engine_capacity * 1.5 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1500:
        return vehicle.engine_capacity * 1.7 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1800:
        return vehicle.engine_capacity * 2.5 * currencies.eur_rub
    elif vehicle.engine_capacity <= 2300:
        return vehicle.engine_capacity * 2.7 * currencies.eur_rub
    elif vehicle.engine_capacity <= 3000:
        return vehicle.engine_capacity * 3 * currencies.eur_rub
    elif vehicle.engine_capacity > 3000:
        return vehicle.engine_capacity * 3.6 * currencies.eur_rub
    else:
        return 0


# Расчёт таможенной пошлины для возраста авто от 5-х лет физ. лицо
def customs_duty_physical6(vehicle):
    if vehicle.engine_capacity <= 1000:
        return vehicle.engine_capacity * 3 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1500:
        return vehicle.engine_capacity * 3.2 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1800:
        return vehicle.engine_capacity * 3.5 * currencies.eur_rub
    elif vehicle.engine_capacity <= 2300:
        return vehicle.engine_capacity * 4.8 * currencies.eur_rub
    elif vehicle.engine_capacity <= 3000:
        return vehicle.engine_capacity * 5 * currencies.eur_rub
    elif vehicle.engine_capacity > 3000:
        return vehicle.engine_capacity * 5.7 * currencies.eur_rub
    else:
        return 0


# Расчёт таможенной пошлины для физических лиц
def customs_duty_physical(vehicle):
    if vehicle.engine_type == "euv":
        return customs_duty_euv(price_to_rub(vehicle.price, vehicle.currency))
    elif vehicle.engine_type == "ice" or vehicle.engine_type == "hyb" or vehicle.engine_type == "dis":
        if check_manufactured_date(vehicle.year, vehicle.month) < 3:
            return customs_duty_physical3(vehicle)
        elif check_manufactured_date(vehicle.year, vehicle.month) < 5:
            return customs_duty_physical5(vehicle)
        elif check_manufactured_date(vehicle.year, vehicle.month) >= 5:
            return customs_duty_physical6(vehicle)
        else:
            return 0
    else:
        return 0


# Расчёт утилизационного сбора для авто до 3 лет физ. лицо для Л.П.
def customs_utiliaztion_physical3(vehicle):
    rate = 20000
    if vehicle.engine_type == "euv":
        return rate * 0.17
    if vehicle.engine_capacity <= 3000:
        return rate * 0.17
    elif vehicle.engine_capacity <= 3500:
        return rate * 48.5
    elif vehicle.engine_capacity > 3500:
        return rate * 61.76
    else:
        return 0


# Расчёт утилизационного сбора для авто от 3 лет физ. лицо для Л.П.
def customs_utiliaztion_physical4(vehicle):
    rate = 20000
    if vehicle.engine_type == "euv":
        return rate * 0.17
    if vehicle.engine_capacity <= 3500:
        return rate * 0.26
    elif vehicle.engine_capacity > 3500:
        return rate * 81.91
    else:
        return 0


# Расчёт утилизационного сбора для физических лиц
def customs_utilization_physical(vehicle):
    if check_manufactured_date(vehicle.year, vehicle.month) < 3:
        return customs_utiliaztion_physical3(vehicle)
    elif check_manufactured_date(vehicle.year, vehicle.month) >= 3:
        return customs_utiliaztion_physical4(vehicle)
    else:
        return 0


# Расчёт НДС для физичекского лица
def vat_physical(vehicle):
    if vehicle.engine_type == "euv":
        return ((price_to_rub(vehicle.price, vehicle.currency) +
                 customs_fee(price_to_rub(vehicle.price, vehicle.currency)) +
                 customs_excise_physical(vehicle) +
                 customs_duty_physical(vehicle)) * 0.20)
    else:
        return 0

# Расчёт всей таможни для физических лиц
def customs_physical(vehicle):
    return (price_to_rub(vehicle.price, vehicle.currency) +
            customs_fee(price_to_rub(vehicle.price, vehicle.currency)) +
            customs_excise_physical(vehicle) +
            customs_duty_physical(vehicle) +
            vat_physical(vehicle) +
            customs_utilization_physical(vehicle))