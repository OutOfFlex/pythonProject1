import pandas as pd

from calculatorLight import *
from calculatorPhysical import *
from models.vehicle import *
from models.heavy import *

from calculatorHeavy import *
import multiusedFunctions

df = pd.DataFrame()
hc = HeavyCalculator

# Импорт в датафрейм из экселя
def import_excel(filepath):
    global df
    df = pd.read_excel(filepath)


# Экспорт из датафрейма в эксель
def export_excel(file_path, add_logistics, before_logistics, after_logistics):
    last_index = df.iloc[:, 1].last_valid_index()
    if not add_logistics:
        before_logistics = 0
        after_logistics = 0
    for i in range(1, last_index + 1):
        if df.iat[i, 1] == 1:
            light_excel(i, before_logistics, after_logistics)
        elif df.iat[i, 1] == 2:
            heavy_excel(i, before_logistics, after_logistics)
        else:
            raise ValueError(f"Invalid value in the second column at index {i}")
        currency_excel(i)
    df.to_excel(file_path)


# Курс подсчёта
def currency_excel(i):
    if df.iat[i, 14] == "cny":
        df.iat[i, 15] = currencies.cny_rub
    elif df.iat[i, 14] == "eur":
        df.iat[i, 15] = currencies.eur_rub
    elif df.iat[i, 14] == "usd":
        df.iat[i, 15] = currencies.usd_rub
    elif df.iat[i, 14] == "yen":
        df.iat[i, 15] = currencies.yen_rub


# Расчёт для электромобиля
def euv_excel(row_excel, vehicle, before_logistics, after_logistics):
    global df
    df.iat[row_excel, 16] = price_to_rub(vehicle.price, vehicle.currency)
    multiusedFunctions.add_before_customs_expenses(vehicle, before_logistics)
    df.iat[row_excel, 17] = customs_excise_euv(vehicle.power)
    df.iat[row_excel, 18] = customs_fee(price_to_rub(vehicle.price, vehicle.currency))
    df.iat[row_excel, 19] = customs_duty_physical(vehicle)
    df.iat[row_excel, 20] = customs_utilization_physical(vehicle)
    df.iat[row_excel, 21] = vat_physical(vehicle)
    df.iat[row_excel, 22] = customs_physical(vehicle)
    df.iat[row_excel, 23] = customs_excise_euv(vehicle.power)
    df.iat[row_excel, 24] = customs_fee(price_to_rub(vehicle.price, vehicle.currency))
    df.iat[row_excel, 25] = customs_duty_artificial(vehicle)
    df.iat[row_excel, 26] = customs_utilization_artificial(vehicle)
    df.iat[row_excel, 27] = vat_artificial(vehicle)
    df.iat[row_excel, 28] = customs_artificial(vehicle) + after_logistics


# Расчёт легковых авто для юр.лиц
def artificial_excel(row_excel, vehicle, before_logistics, after_logistics):
    global df
    df.iat[row_excel, 16] = price_to_rub(vehicle.price, vehicle.currency)
    multiusedFunctions.add_before_customs_expenses(vehicle, before_logistics)
    df.iat[row_excel, 23] = customs_excise_artificial(vehicle)
    df.iat[row_excel, 24] = customs_fee(price_to_rub(vehicle.price, vehicle.currency))
    df.iat[row_excel, 25] = customs_duty_artificial(vehicle)
    df.iat[row_excel, 26] = customs_utilization_artificial(vehicle)
    df.iat[row_excel, 27] = vat_artificial(vehicle)
    df.iat[row_excel, 28] = customs_artificial(vehicle) + after_logistics


# Расчёт легковых авто для физических лиц
def physical_excel(row_excel, vehicle, before_logistics, after_logistics):
    global df
    df.iat[row_excel, 16] = price_to_rub(vehicle.price, vehicle.currency)
    multiusedFunctions.add_before_customs_expenses(vehicle, before_logistics)
    df.iat[row_excel, 18] = customs_fee(price_to_rub(vehicle.price, vehicle.currency))
    df.iat[row_excel, 19] = customs_duty_physical(vehicle)
    df.iat[row_excel, 20] = customs_utilization_physical(vehicle)
    df.iat[row_excel, 22] = customs_physical(vehicle) + after_logistics


# Расчёт для легковых авто
def light_excel(row_excel, before_logistics, after_logistics):
    global df
    vehicle = Vehicle(
        df.iat[row_excel, 7],
        df.iat[row_excel, 8],
        df.iat[row_excel, 10],
        df.iat[row_excel, 11],
        df.iat[row_excel, 12],
        df.iat[row_excel, 13],
        df.iat[row_excel, 14],
        df.iat[row_excel, 9]
    )
    multiusedFunctions.power_to_type(vehicle)
    if vehicle.engine_type == "euv":
        euv_excel(row_excel, vehicle, before_logistics, after_logistics)
    else:
        physical_excel(row_excel, vehicle, before_logistics, after_logistics)
    artificial_excel(row_excel, vehicle, before_logistics, after_logistics)


# Расчёт спец-техники
def heavy_excel(row_excel, before_logistics, after_logistics):
    global df
    heavy = Heavy(
        df.iat[row_excel, 7],
        df.iat[row_excel, 8],
        df.iat[row_excel, 10],
        df.iat[row_excel, 11],
        df.iat[row_excel, 12],
        df.iat[row_excel, 13],
        df.iat[row_excel, 14],
        df.iat[row_excel, 3],
        df.iat[row_excel, 2]
    )
    multiusedFunctions.add_before_customs_expenses(heavy, before_logistics)
    df.iat[row_excel, 16] = price_to_rub(heavy.price, heavy.currency)
    multiusedFunctions.add_before_customs_expenses(heavy, before_logistics)
    df.iat[row_excel, 25] = hc.customs_duty(heavy)
    df.iat[row_excel, 26] = hc.customs_utilization_heavy(heavy)
    df.iat[row_excel, 27] = hc.customs_vat(heavy)
    df.iat[row_excel, 28] = hc.customs_heavy(heavy) + after_logistics
    df.iat[row_excel, 29] = hc.customs_all_heavy(heavy) + after_logistics
