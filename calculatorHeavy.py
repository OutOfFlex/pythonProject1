from multiusedFunctions import *
from models.heavy import *
import currencies

tn_ved_data = {
    8427101000: 0,
    8427109000: 0,
    8427209000: 0.05,
    8427201901: 0.05,
    8427201902: 0.05,
    8427201909: 0.05,
    8427201100: 0.05,
    8429511000: 0,
    8429519100: 0.05,
    8429519900: 0.05,
    8704101011: 0.03,
    8704101019: 0.03,
    8704101021: 0,
    8704101022: 0.05,
    8704101029: 0.05,
    8704101080: 0.05,
    8704109000: 0.05,
    8429200010: 0.03,
    8429200091: 0,
    8429200099: 0.03,
    8429110010: 0.05,
    8429110020: 0.05,
    8429110090: 0.05,
    8429190001: 0.05,
    8429190009: 0.05,
    8429521009: 0.05,
    8429521001: 0.05,
    8429529000: 0.05,
    8429590000: 0.05,
    8429401000: 0.05,
    8429403000: 0.075,
    8426410001: 0,
    8426410002: 0,
    8426410003: 0,
    8426410007: 0.05,
    8426490010: 0.05,
    8426490091: 0.07,
    8426490099: 0.05,
    8479100000: 0,
    8703101100: 0.05,
    8703101800: 0.05,
    8703121109: 0.05,
    8703311090: 0.15,
    8704900000: 0.15,
    8701100000: 0.10,
    8701919000: 0.10,
    8701911000: 0.05,
    8701915000: 0.10,
    8701929000: 0.10,
    8701921000: 0.10,
    8701925000: 0.10,
    8701939000: 0.10,
    8701931000: 0.10,
    8701935000: 0.10,
    8701941009: 0.10,
    8701945000: 0.10,
    8701949000: 0.10,
    8701951009: 0.10,
    8701955000: 0.10,
    8701959000: 0.10,
    8701211090: 0.13,
    8701219090: 0.13,
    8701221090: 0.13,
    8701229090: 0.13,
    8701231090: 0.13,
    8701239090: 0.13,
    8701241090: 0.13,
    8701249090: 0.13,
    8701291090: 0.13,
    8701299090: 0.13,
    8701300009: 0.075,
    8716109200: 0.10,
    8716109800: 0.10,
    8716200000: 0.05,
    8716310000: 0.125,
    8716391000: 0.125,
    8716395001: 0.10,
    8716395002: 0.09,
    8716395009: 0.10,
    8716398005: 0.10,
    8716398008: 0.10,
    8716400000: 0.10
}

# Расчёт пошлины
def customs_duty(heavy):
    # Проверяем, есть ли код в словаре tn_ved_data
    if heavy.tn_ved in tn_ved_data:
        return price_to_rub(heavy.price, heavy.currency) * tn_ved_data[heavy.tn_ved]
    else:
        print(f"Код ТН ВЭД {tn_ved_data[heavy.tn_ved]} не найден в словаре.")
        return 0

# Расчёт НДС
def customs_vat(heavy):
    return (price_to_rub(heavy.price, heavy.currency) + customs_duty(heavy)) * 0.2

def customs_utilization_heavy(heavy):
    if heavy.id_code == 'f':
        return utilization_f(heavy)
    elif heavy.id_code == 'r':
        return utilization_r(heavy)
    elif heavy.id_code == 'a':
        return utilization_a(heavy)
    elif heavy.id_code == 'b':
        return utilization_b(heavy)
    elif heavy.id_code == 'c':
        return utilization_c(heavy)
    elif heavy.id_code == 'e':
        return utilization_e(heavy)
    elif heavy.id_code == 'g':
        return utilization_g(heavy)
    elif heavy.id_code == 'g2':
        return utilization_g2(heavy)
    elif heavy.id_code == 'i':
        return utilization_i(heavy)
    elif heavy.id_code == 'm':
        return utilization_m(heavy)
    elif heavy.id_code == 'n':
        return utilization_n(heavy)
    elif heavy.id_code == 'k' or 'l':
        return utilization_kl(heavy)
    elif heavy.id_code == 'bus':
        return utilization_bus(heavy)
    else:
        return 0

def utilization_f(heavy):
    rate = 20000
    if heavy.power < 50:
        return rate * (1 if check_manufactured_date(heavy.year, heavy.month) < 3 else 6)
    elif heavy.power < 100:
        return rate * (4.2 if check_manufactured_date(heavy.year, heavy.month) < 3 else 10)
    elif heavy.power < 200:
        return rate * (6.2 if check_manufactured_date(heavy.year, heavy.month) < 3 else 17)
    elif heavy.power < 250:
        return rate * (4.5 if check_manufactured_date(heavy.year, heavy.month) < 3 else 20)
    elif heavy.power < 300:
        return rate * (12.09 if check_manufactured_date(heavy.year, heavy.month) < 3 else 30)
    elif heavy.power < 400:
        return rate * (14.13 if check_manufactured_date(heavy.year, heavy.month) < 3 else 35)
    elif heavy.power >= 400:
        return rate * (26.09 if check_manufactured_date(heavy.year, heavy.month) < 3 else 70)
    else:
        return 0

def utilization_r(heavy):
    rate = 20000
    if heavy.power < 200:
        return rate * (22.4 if check_manufactured_date(heavy.year, heavy.month) < 3 else 35)
    elif heavy.power < 650:
        return rate * (34.78 if check_manufactured_date(heavy.year, heavy.month) < 3 else 51.12)
    elif heavy.power < 1750:
        return rate * (41.3 if check_manufactured_date(heavy.year, heavy.month) < 3 else 52.8)
    elif heavy.power >= 1750:
        return rate * (61.1 if check_manufactured_date(heavy.year, heavy.month) < 3 else 66)
    else:
        return 0

def utilization_a(heavy):
    rate = 20000
    if heavy.power < 100:
        return rate * (3.2 if check_manufactured_date(heavy.year, heavy.month) < 3 else 8.5)
    elif heavy.power < 140:
        return rate * (11.74 if check_manufactured_date(heavy.year, heavy.month) < 3 else 30.75)
    elif heavy.power < 200:
        return rate * (12.37 if check_manufactured_date(heavy.year, heavy.month) < 3 else 33.39)
    elif heavy.power >= 200:
        return rate * (16.81 if check_manufactured_date(heavy.year, heavy.month) < 3 else 49.8)
    else:
        return 0

def utilization_b(heavy):
    rate = 20000
    if heavy.power < 100:
        return rate * (4 if check_manufactured_date(heavy.year, heavy.month) < 3 else 12)
    elif heavy.power < 200:
        return rate * (12.17 if check_manufactured_date(heavy.year, heavy.month) < 3 else 35)
    elif heavy.power < 300:
        return rate * (14.49 if check_manufactured_date(heavy.year, heavy.month) < 3 else 55)
    elif heavy.power < 400:
        return rate * (16.81 if check_manufactured_date(heavy.year, heavy.month) < 3 else 70)
    elif heavy.power >= 200:
        return rate * (15 if check_manufactured_date(heavy.year, heavy.month) < 3 else 100)
    else:
        return 0

def utilization_c(heavy):
    rate = 20000
    if heavy.power < 170:
        return rate * (4 if check_manufactured_date(heavy.year, heavy.month) < 3 else 17)
    elif heavy.power < 250:
        return rate * (6 if check_manufactured_date(heavy.year, heavy.month) < 3 else 25)
    elif heavy.power >= 250:
        return rate * (8 if check_manufactured_date(heavy.year, heavy.month) < 3 else 40.5)
    else:
        return 0

def utilization_e(heavy):
    rate = 20000
    if heavy.power < 40:
        return rate * (4.62 if check_manufactured_date(heavy.year, heavy.month) < 3 else 9.86)
    elif heavy.power < 80:
        return rate * (5.8 if check_manufactured_date(heavy.year, heavy.month) < 3 else 12)
    elif heavy.power >= 80:
        return rate * (6.96 if check_manufactured_date(heavy.year, heavy.month) < 3 else 15)
    else:
        return 0

def utilization_g(heavy):
    rate = 20000
    if heavy.power < 170:
        return rate * (11.5 if check_manufactured_date(heavy.year, heavy.month) < 3 else 44.3)
    elif heavy.power < 250:
        return rate * (22.7 if check_manufactured_date(heavy.year, heavy.month) < 3 else 95.5)
    elif heavy.power >= 250:
        return rate * (30.3 if check_manufactured_date(heavy.year, heavy.month) < 3 else 238.1)
    else:
        return 0

def utilization_g2(heavy):
    rate = 20000
    if heavy.power < 130:
        return rate * (10 if check_manufactured_date(heavy.year, heavy.month) < 3 else 30)
    elif heavy.power < 200:
        return rate * (16 if check_manufactured_date(heavy.year, heavy.month) < 3 else 50)
    elif heavy.power < 300:
        return rate * (21 if check_manufactured_date(heavy.year, heavy.month) < 3 else 70)
    elif heavy.power >= 300:
        return rate * (25 if check_manufactured_date(heavy.year, heavy.month) < 3 else 100)
    else:
        return 0

def utilization_i(heavy):
    rate = 20000
    if heavy.power < 100:
        return rate * (2.8 if check_manufactured_date(heavy.year, heavy.month) < 3 else 10.9)
    elif heavy.power < 220:
        return rate * (4.1 if check_manufactured_date(heavy.year, heavy.month) < 3 else 16.5)
    elif heavy.power >= 220:
        return rate * (4.7 if check_manufactured_date(heavy.year, heavy.month) < 3 else 19.3)
    else:
        return 0

def utilization_m(heavy):
    rate = 20000
    if heavy.power <= 30:
        return rate * (0.4 if check_manufactured_date(heavy.year, heavy.month) < 3 else 1.8)
    elif heavy.power < 60:
        return rate * (1.01 if check_manufactured_date(heavy.year, heavy.month) < 3 else 2.9)
    elif heavy.power < 90:
        return rate * (3.13 if check_manufactured_date(heavy.year, heavy.month) < 3 else 14.49)
    elif heavy.power < 130:
        return rate * (7.25 if check_manufactured_date(heavy.year, heavy.month) < 3 else 17.39)
    elif heavy.power < 180:
        return rate * (10.14 if check_manufactured_date(heavy.year, heavy.month) < 3 else 23.19)
    elif heavy.power < 220:
        return rate * (11.59 if check_manufactured_date(heavy.year, heavy.month) < 3 else 26.67)
    elif heavy.power < 280:
        return rate * (13.19 if check_manufactured_date(heavy.year, heavy.month) < 3 else 31.59)
    elif heavy.power < 340:
        return rate * (20.87 if check_manufactured_date(heavy.year, heavy.month) < 3 else 43.48)
    elif heavy.power < 380:
        return rate * (6.7 if check_manufactured_date(heavy.year, heavy.month) < 3 else 25)
    elif heavy.power >= 380:
        return rate * (9 if check_manufactured_date(heavy.year, heavy.month) < 3 else 40)
    else:
        return 0

def utilization_n(heavy):
    rate = 20000
    if heavy.power < 100:
        return rate * (1.5 if check_manufactured_date(heavy.year, heavy.month) < 3 else 7)
    elif heavy.power < 200:
        return rate * (2.5 if check_manufactured_date(heavy.year, heavy.month) < 3 else 10)
    elif heavy.power >= 200:
        return rate * (9 if check_manufactured_date(heavy.year, heavy.month) < 3 else 28)
    else:
        return 0

def utilization_kl(heavy):
    rate = 2000
    if heavy.engine_capacity < 300:
        return rate * (0.4 if check_manufactured_date(heavy.year, heavy.month) < 3 else 0.7)
    elif heavy.engine_capacity >= 300:
        return rate * (0.7 if check_manufactured_date(heavy.year, heavy.month) < 3 else 1.3)
    else:
        return 0

def utilization_bus(heavy):
    rate = 2000
    if heavy.engine_capacity == 0:
        return rate * (10 if check_manufactured_date(heavy.year, heavy.month) < 3 else 10.09)
    elif heavy.engine_capacity < 2500:
        return rate * (3.14 if check_manufactured_date(heavy.year, heavy.month) < 3 else 3.18)
    elif heavy.engine_capacity < 5000:
        return rate * (11.05 if check_manufactured_date(heavy.year, heavy.month) < 3 else 16.73)
    elif heavy.engine_capacity < 10000:
        return rate * (12.34 if check_manufactured_date(heavy.year, heavy.month) < 3 else 15.84)
    elif heavy.engine_capacity >= 10000:
        return rate * (14.27 if check_manufactured_date(heavy.year, heavy.month) < 3 else 22.46)
    else:
        return 0

def customs_heavy(heavy):
    return (price_to_rub(heavy.price, heavy.currency) +
            customs_utilization_heavy(heavy) +
            customs_duty(heavy) +
            customs_vat(heavy))