from multiusedFunctions import *


class HeavyCalculator:

    @staticmethod
    def customs_duty(heavy):
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

        if heavy.tn_ved in tn_ved_data:
            return heavy.price * tn_ved_data[heavy.tn_ved]
        else:
            raise ValueError(f"Значение tn_ved_data не обнаружено")

    @staticmethod
    def customs_vat(heavy):
        return ((heavy.price +
                 HeavyCalculator.customs_duty(heavy)) *
                0.2)

    @staticmethod
    def customs_utilization_heavy(heavy):
        utilization_functions = {
            'f': HeavyCalculator.utilization_f,
            'r': HeavyCalculator.utilization_r,
            'a': HeavyCalculator.utilization_a,
            'b': HeavyCalculator.utilization_b,
            'c': HeavyCalculator.utilization_c,
            'e': HeavyCalculator.utilization_e,
            'g': HeavyCalculator.utilization_g,
            'g2': HeavyCalculator.utilization_g2,
            'i': HeavyCalculator.utilization_i,
            'm': HeavyCalculator.utilization_m,
            'n': HeavyCalculator.utilization_n,
            'k': HeavyCalculator.utilization_kl,
            'l': HeavyCalculator.utilization_kl,
            'bus': HeavyCalculator.utilization_bus
        }

        if heavy.id_code in utilization_functions:
            return utilization_functions[heavy.id_code](heavy)
        else:
            raise ValueError(f"Значение heavy.id_code не находится в списке id кодов {HeavyCalculator.
                             customs_utilization_heavy.__name__}")

    @staticmethod
    def utilization_f(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 50:
            return rate * (1 if true_date < 3 else 6)
        elif heavy.power < 100:
            return rate * (4.2 if true_date < 3 else 10)
        elif heavy.power < 200:
            return rate * (6.2 if true_date < 3 else 17)
        elif heavy.power < 250:
            return rate * (4.5 if true_date < 3 else 20)
        elif heavy.power < 300:
            return rate * (12.09 if true_date < 3 else 30)
        elif heavy.power < 400:
            return rate * (14.13 if true_date < 3 else 35)
        elif heavy.power >= 400:
            return rate * (26.09 if true_date < 3 else 70)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_f.__name__}")

    # Расчёт утильсбора категории R
    @staticmethod
    def utilization_r(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 200:
            return rate * (22.4 if true_date < 3 else 35)
        elif heavy.power < 650:
            return rate * (34.78 if true_date < 3 else 51.12)
        elif heavy.power < 1750:
            return rate * (41.3 if true_date < 3 else 52.8)
        elif heavy.power >= 1750:
            return rate * (61.1 if true_date < 3 else 66)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_r.__name__}")

    # Расчёт утильсбора категории A
    @staticmethod
    def utilization_a(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 100:
            return rate * (3.2 if true_date < 3 else 8.5)
        elif heavy.power < 140:
            return rate * (11.74 if true_date < 3 else 30.75)
        elif heavy.power < 200:
            return rate * (12.37 if true_date < 3 else 33.39)
        elif heavy.power >= 200:
            return rate * (16.81 if true_date < 3 else 49.8)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_a.__name__}")

    # Расчёт утильсбора категории B
    @staticmethod
    def utilization_b(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 100:
            return rate * (4 if true_date < 3 else 12)
        elif heavy.power < 200:
            return rate * (12.17 if true_date < 3 else 35)
        elif heavy.power < 300:
            return rate * (14.49 if true_date < 3 else 55)
        elif heavy.power < 400:
            return rate * (16.81 if true_date < 3 else 70)
        elif heavy.power >= 200:
            return rate * (15 if true_date < 3 else 100)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_b.__name__}")

    # Расчёт утильсбора категории C
    @staticmethod
    def utilization_c(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 170:
            return rate * (4 if true_date < 3 else 17)
        elif heavy.power < 250:
            return rate * (6 if true_date < 3 else 25)
        elif heavy.power >= 250:
            return rate * (8 if true_date < 3 else 40.5)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_c.__name__}")

    # Расчёт утильсбора категории E
    @staticmethod
    def utilization_e(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 40:
            return rate * (4.62 if true_date < 3 else 9.86)
        elif heavy.power < 80:
            return rate * (5.8 if true_date < 3 else 12)
        elif heavy.power >= 80:
            return rate * (6.96 if true_date < 3 else 15)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_e.__name__}")

    # Расчёт утильсбора категории G1-3
    @staticmethod
    def utilization_g(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 170:
            return rate * (11.5 if true_date < 3 else 44.3)
        elif heavy.power < 250:
            return rate * (22.7 if true_date < 3 else 95.5)
        elif heavy.power >= 250:
            return rate * (30.3 if true_date < 3 else 238.1)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_g.__name__}")

    # Расчёт утильсбора категории 4-7
    @staticmethod
    def utilization_g2(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 130:
            return rate * (10 if true_date < 3 else 30)
        elif heavy.power < 200:
            return rate * (16 if true_date < 3 else 50)
        elif heavy.power < 300:
            return rate * (21 if true_date < 3 else 70)
        elif heavy.power >= 300:
            return rate * (25 if true_date < 3 else 100)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_g2.__name__}")

    # Расчёт утильсбора категории I
    @staticmethod
    def utilization_i(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 100:
            return rate * (2.8 if true_date < 3 else 10.9)
        elif heavy.power < 220:
            return rate * (4.1 if true_date < 3 else 16.5)
        elif heavy.power >= 220:
            return rate * (4.7 if true_date < 3 else 19.3)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_i.__name__}")

    # Расчёт утильсбора категории M
    @staticmethod
    def utilization_m(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power <= 30:
            return rate * (0.4 if true_date < 3 else 1.8)
        elif heavy.power < 60:
            return rate * (1.01 if true_date < 3 else 2.9)
        elif heavy.power < 90:
            return rate * (3.13 if true_date < 3 else 14.49)
        elif heavy.power < 130:
            return rate * (7.25 if true_date < 3 else 17.39)
        elif heavy.power < 180:
            return rate * (10.14 if true_date < 3 else 23.19)
        elif heavy.power < 220:
            return rate * (11.59 if true_date < 3 else 26.67)
        elif heavy.power < 280:
            return rate * (13.19 if true_date < 3 else 31.59)
        elif heavy.power < 340:
            return rate * (20.87 if true_date < 3 else 43.48)
        elif heavy.power < 380:
            return rate * (6.7 if true_date < 3 else 25)
        elif heavy.power >= 380:
            return rate * (9 if true_date < 3 else 40)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_m.__name__}")

    # Расчёт утильсбора категории N
    @staticmethod
    def utilization_n(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.power < 100:
            return rate * (1.5 if true_date < 3 else 7)
        elif heavy.power < 200:
            return rate * (2.5 if true_date < 3 else 10)
        elif heavy.power >= 200:
            return rate * (9 if true_date < 3 else 28)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_n.__name__}")

    # Расчет утильсбора категории K и L
    @staticmethod
    def utilization_kl(heavy):
        rate = 172500
        true_date = customs_duty_check(heavy.year, heavy.month)

        if 0 < heavy.engine_capacity < 300:
            return rate * (0.4 if true_date < 3 else 0.7)
        elif heavy.engine_capacity >= 300:
            return rate * (0.7 if true_date < 3 else 1.3)
        else:
            raise ValueError(f"Значение heavy.power не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_kl.__name__}")

    # Расчет утильсбора категории Автобусов
    @staticmethod
    def utilization_bus(heavy):
        rate = 15000
        true_date = customs_duty_check(heavy.year, heavy.month)

        if heavy.engine_capacity == 0:
            return rate * (10 if true_date < 3 else 10.09)
        elif heavy.engine_capacity < 2500:
            return rate * (3.14 if true_date < 3 else 3.18)
        elif heavy.engine_capacity < 5000:
            return rate * (11.05 if true_date < 3 else 16.73)
        elif heavy.engine_capacity < 10000:
            return rate * (12.34 if true_date < 3 else 15.84)
        elif heavy.engine_capacity >= 10000:
            return rate * (14.27 if true_date < 3 else 22.46)
        else:
            raise ValueError(f"Значение heavy.engine_capacity не может быть меньше 0 в функции {HeavyCalculator.
                             utilization_bus.__name__}")

    @staticmethod
    def customs_all_heavy(heavy):
        return (HeavyCalculator.customs_heavy(heavy) +
                HeavyCalculator.customs_utilization_heavy(heavy))

    @staticmethod
    def customs_heavy(heavy):
        return (heavy.price +
                HeavyCalculator.customs_duty(heavy) +
                HeavyCalculator.customs_vat(heavy))
