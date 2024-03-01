from multiusedFunctions import *
import currencies


# Расчёт НДС для юридического лица
def vat_artificial(vehicle):
    return ((price_to_rub(vehicle.price, vehicle.currency) +
             customs_fee(price_to_rub(vehicle.price, vehicle.currency)) +
             customs_excise_artificial(vehicle) +
             customs_duty_artificial(vehicle)) * 0.20)


# Акциз для юридического лица
def customs_excise_artificial(vehicle):
    if vehicle.engine_type == "euv":
        return customs_excise_euv(vehicle.power)
    elif vehicle.engine_type == "ice" or vehicle.engine_type == "hyb" or vehicle.engine_type == "dis":
        if vehicle.power <= 90:
            return 0
        elif vehicle.power <= 150:
            return 55 * vehicle.power
        elif vehicle.power <= 200:
            return 531 * vehicle.power
        elif vehicle.power <= 300:
            return 869 * vehicle.power
        elif vehicle.power <= 400:
            return 1482 * vehicle.power
        elif vehicle.power <= 500:
            return 1534 * vehicle.power
        elif vehicle.power < 500:
            return 1584 * vehicle.power
        else:
            return 0
    else:
        return 0


# Расчёт таможенной пошлины для возраста авто менее 3-х лет юр. лицо
def customs_duty_artificial3(vehicle):
    customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.15
    if vehicle.engine_capacity <= 3000:
        return customs_duty
    elif vehicle.engine_capacity > 3000:
        customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.125
        return customs_duty
    else:
        return 0


# Расчёт таможенной пошлины для возраста авто от 3-х до 7 лет юр. лицо
def customs_duty_artificial7(vehicle):
    customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.20
    if vehicle.engine_capacity <= 1000:
        customs_duty_minimum = vehicle.engine_capacity * 0.36 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity <= 1500:
        customs_duty_minimum = vehicle.engine_capacity * 0.4 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity <= 1800:
        customs_duty_minimum = vehicle.engine_capacity * 0.36 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity <= 3000:
        customs_duty_minimum = vehicle.engine_capacity * 0.44 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity > 3000:
        customs_duty_minimum = vehicle.engine_capacity * 0.8 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    else:
        return 0


# Расчёт таможенной пошлины для возраста авто от 7 лет юр. лицо
def customs_duty_artificial8(vehicle):
    if vehicle.engine_capacity <= 1000:
        return vehicle.engine_capacity * 1.4 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1500:
        return vehicle.engine_capacity * 1.5 * currencies.eur_rub
    elif vehicle.engine_capacity <= 1800:
        return vehicle.engine_capacity * 1.6 * currencies.eur_rub
    elif vehicle.engine_capacity <= 3000:
        return vehicle.engine_capacity * 2.2 * currencies.eur_rub
    elif vehicle.engine_capacity > 3000:
        return vehicle.engine_capacity * 3.2 * currencies.eur_rub
    else:
        return 0


# Расчёт таможенной пошлины для дизеля возраста авто менее 3-х лет юр. лицо
def customs_duty_artificial_dis3(vehicle):
    return price_to_rub(vehicle.price, vehicle.currency) * 0.15


# Расчёт таможенной пошлины для дизеля возраста авто от 3-х до 7 лет юр. лицо
def customs_duty_artificial_dis7(vehicle):
    customs_duty = price_to_rub(vehicle.price, vehicle.currency) * 0.20
    if vehicle.engine_capacity <= 1500:
        customs_duty_minimum = vehicle.engine_capacity * 0.32 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity <= 2500:
        customs_duty_minimum = vehicle.engine_capacity * 0.4 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    elif vehicle.engine_capacity > 2500:
        customs_duty_minimum = vehicle.engine_capacity * 0.8 * currencies.eur_rub
        return customs_duty_check(customs_duty, customs_duty_minimum)
    else:
        return 0


# Расчёт таможенной пошлины для дизеля возраста авто от 7 лет юр. лицо
def customs_duty_artificial_dis8(vehicle):
    if vehicle.engine_capacity <= 1500:
        return vehicle.engine_capacity * 1.5 * currencies.eur_rub
    elif vehicle.engine_capacity <= 2500:
        return vehicle.engine_capacity * 2.2 * currencies.eur_rub
    elif vehicle.engine_capacity > 2500:
        return vehicle.engine_capacity * 3.2 * currencies.eur_rub
    else:
        return 0


# Расчёт таможенной пошлины для юридических лиц
def customs_duty_artificial(vehicle):
    if vehicle.engine_type == "euv":
        return customs_duty_euv(price_to_rub(vehicle.price, vehicle.currency))
    elif vehicle.engine_type == "ice" or vehicle.engine_type == "hyb":
        if true_date(vehicle.year, vehicle.month) < 3:
            return customs_duty_artificial3(vehicle)
        elif true_date(vehicle.year, vehicle.month) < 7:
            return customs_duty_artificial7(vehicle)
        elif true_date(vehicle.year, vehicle.month) >= 7:
            return customs_duty_artificial8(vehicle)
        else:
            return 0
    elif vehicle.engine_type == "dis":
        if true_date(vehicle.year, vehicle.month) < 3:
            return customs_duty_artificial_dis3(vehicle)
        elif true_date(vehicle.year, vehicle.month) < 7:
            return customs_duty_artificial_dis7(vehicle)
        elif true_date(vehicle.year, vehicle.month) >= 7:
            return customs_duty_artificial_dis8(vehicle)
        else:
            return 0
    else:
        return 0


# Расчёт утилизационного сбора для авто до 3 лет юр. лицо
def customs_utiliaztion_artificial3(vehicle):
    rate = 20000
    if vehicle.engine_type == "euv":
        return rate * 1.63
    if vehicle.engine_capacity <= 1000:
        return rate * 4.06
    elif vehicle.engine_capacity <= 2000:
        return rate * 15.3
    elif vehicle.engine_capacity <= 3000:
        return rate * 42.24
    elif vehicle.engine_capacity <= 3500:
        return rate * 48.5
    elif vehicle.engine_capacity > 3500:
        return rate * 61.76
    else:
        return 0


# Расчёт утилизационного сбора для авто от 3 лет юр. лицо
def customs_utiliaztion_arificical4(vehicle):
    rate = 20000
    if vehicle.engine_type == "euv":
        return rate * 6.1
    if vehicle.engine_capacity <= 1000:
        return rate * 10.36
    elif vehicle.engine_capacity <= 2000:
        return rate * 26.44
    elif vehicle.engine_capacity <= 3000:
        return rate * 63.95
    elif vehicle.engine_capacity <= 3500:
        return rate * 74.25
    elif vehicle.engine_capacity > 3500:
        return rate * 81.19
    else:
        return 0


# Расчёт утилизационного сбора для юридических лиц
def customs_utilization_artificial(vehicle):
    if true_date(vehicle.year, vehicle.month) < 3:
        return customs_utiliaztion_artificial3(vehicle)
    elif true_date(vehicle.year, vehicle.month) >= 3:
        return customs_utiliaztion_arificical4(vehicle)
    else:
        return 0


# Расчёт всей таможни для юридических лиц
def customs_artificial(vehicle):
    return (price_to_rub(vehicle.price, vehicle.currency) +
            customs_fee(price_to_rub(vehicle.price, vehicle.currency)) +
            customs_excise_artificial(vehicle) +
            customs_duty_artificial(vehicle) +
            vat_artificial(vehicle) +
            customs_utilization_artificial(vehicle))
