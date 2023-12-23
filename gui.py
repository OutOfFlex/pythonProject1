import multiusedFunctions
from calculatorHeavy import *
from calculatorLight import *
from calculatorPhysical import *
from currencies import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from excelFiles import import_excel, export_excel
import pandas as pd


class CustomsCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Таможенный калькулятор")

        # Создаем переменные для хранения вводимых данных
        self.power_var = tk.IntVar()
        self.engine_capacity_var = tk.IntVar()
        self.year_var = tk.IntVar()
        self.month_var = tk.IntVar()
        self.price_var = tk.IntVar()
        self.currency_var = tk.StringVar()
        self.engine_type_var = tk.StringVar()
        self.power_type_var = tk.StringVar()
        self.currency_symbols = {"rub": "₽", "cny": "¥", "eur": "€", "usd": "$", "yen": "Y"}
        self.engine_type_symbols = {"ice": "Бензин", "hyb": "Гибрид", "euv": "Электромотор", "dis": "Дизель"}
        self.power_type_symbols = {"hp": "Л.с.", "kw": "Квт.ч"}

        ttk.Button(root, text="Импорт из Excel", command=self.import_from_excel).grid(row=0, column=1, pady=10)
        ttk.Button(root, text="Экспорт в Excel", command=self.export_to_excel).grid(row=0, column=2, pady=10)

        # Строка для обновления валют и получения актуального курса
        ttk.Button(root, text="Обновить валюты", command=self.update_currencies).grid(row=1, column=0, padx=10, pady=5,
                                                                                      sticky="w")
        self.currency_label = ttk.Label(root,
                                        text=f"CNY={cny_rub:.2f} USD={usd_rub:.2f} EUR={eur_rub:.2f} YEN={yen_rub:.3f}")
        self.currency_label.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="w")

        # Создаем метки и текстовые поля для ввода данных
        ttk.Label(root, text="Мощность л.с.:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ttk.Entry(root, textvariable=self.power_var, width=8).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(root, text="Объем двигателя (см³):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        ttk.Entry(root, textvariable=self.engine_capacity_var, width=8).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(root, text="Произведён(год, месяц):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(root, textvariable=self.year_var, width=8).grid(row=4, column=1, padx=5, pady=5)
        ttk.Entry(root, textvariable=self.month_var, width=4).grid(row=4, column=2, padx=5, pady=5, sticky="w")

        ttk.Label(root, text="Стоимость автомобиля:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(root, textvariable=self.price_var, width=8).grid(row=6, column=1, padx=5, pady=5)

        # Создаем Combobox для выбора валюты
        self.currency_combobox = ttk.Combobox(root, textvariable=self.currency_var, state="readonly")
        self.currency_combobox.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.currency_combobox.configure(width=2)

        self.currencies = list(self.currency_symbols.values())

        # Добавляем элементы в выпадающий список Combobox с символами валют
        self.currency_combobox["values"] = self.currencies
        self.currency_combobox.current(self.currencies.index("₽"))  # значение по умолчанию

        # Создаем Combobox для выбора типа мощности
        self.power_type_combobox = ttk.Combobox(root, textvariable=self.power_type_var, state="readonly")
        self.power_type_combobox.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.power_type_combobox.configure(width=5)

        power_types = list(self.power_type_symbols.values())

        # Добавляем элементы в выпадающий список Combobox с типами мощности
        self.power_type_combobox["values"] = power_types
        self.power_type_combobox.current(power_types.index("Л.с."))  # значение по умолчанию

        # Создаем Combobox для выбора типа двигателя
        self.engine_type_combobox = ttk.Combobox(root, textvariable=self.engine_type_var, state="readonly")
        self.engine_type_combobox.grid(row=3, column=2, columnspan=2, padx=8, pady=5, sticky="w")
        self.engine_type_combobox.configure(width=12)

        engine_types = list(self.engine_type_symbols.values())

        # Добавляем элементы в выпадающий список Combobox с типами двигателей
        self.engine_type_combobox["values"] = engine_types
        self.engine_type_combobox.current(engine_types.index("Бензин"))  # значение по умолчанию

        # Создаем кнопку для расчета
        ttk.Button(root, text="Рассчитать", command=self.calculate_customs).grid(row=9, column=1, columnspan=2, pady=10)

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(title="Выберите файл Excel", filetypes=[("Excel files", "*.xlsx")])

        if file_path:
            try:
                # Чтение данных из Excel
                df = pd.read_excel(file_path)

                # Получение данных из DataFrame
                data = {
                    'power': df.at[0, 'Мощность л.с.'],
                    'engine_capacity': df.at[0, 'Объем двигателя (см³)'],
                    'year': df.at[0, 'Произведён(год, месяц)'].year,
                    'month': df.at[0, 'Произведён(год, месяц)'].month,
                    'price': df.at[0, 'Стоимость автомобиля'],
                    'currency': df.at[0, 'Валюта'],
                    'power_type': df.at[0, 'Тип мощности'],
                    'engine_type': df.at[0, 'Тип двигателя'],
                }

                # Присваиваем значения переменным класса
                self.power_var.set(data['power'])
                self.engine_capacity_var.set(data['engine_capacity'])
                self.year_var.set(data['year'])
                self.month_var.set(data['month'])
                self.price_var.set(data['price'])
                currency_index = self.currencies.index(data['currency'])
                self.currency_combobox.current(currency_index)
                power_type_index = self.power_types.index(data['power_type'])
                self.power_type_combobox.current(power_type_index)
                engine_type_index = self.engine_types.index(data['engine_type'])
                self.engine_type_combobox.current(engine_type_index)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при импорте: {str(e)}")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if file_path:
            try:
                # Создание DataFrame из значений переменных класса
                data = {
                    'power': self.power_var.get(),
                    'engine_capacity': self.engine_capacity_var.get(),
                    'year': self.year_var.get(),
                    'month': self.month_var.get(),
                    'price': self.price_var.get(),
                    'currency': self.currencies[self.currency_combobox.current()],
                    'power_type': self.power_types[self.power_type_combobox.current()],
                    'engine_type': self.engine_types[self.engine_type_combobox.current()],
                }

                df = pd.DataFrame([data])

                # Запись DataFrame в Excel
                df.to_excel(file_path, index=False)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при экспорте: {str(e)}")

    def import_excel(file_path):
        try:
            # Чтение данных из Excel
            df = pd.read_excel(file_path)

            # Получение данных из DataFrame
            return {
                'power': df.at[0, 'power'],
                'engine_capacity': df.at[0, 'engine_capacity'],
                'year': df.at[0, 'year'],
                'month': df.at[0, 'month'],
                'price': df.at[0, 'price'],
                'currency': df.at[0, 'currency'],
                'power_type': df.at[0, 'power_type'],
                'engine_type': df.at[0, 'engine_type'],
            }

        except Exception as e:
            raise ValueError(f"Ошибка при импорте: {str(e)}")

    def export_excel(file_path, data):
        try:
            # Создание DataFrame из словаря
            df = pd.DataFrame([data])

            # Расчеты
            df['Таможенный сбор'] = df['price'] * 0.1
            # Другие расчеты...

            # Запись DataFrame в Excel
            df.to_excel(file_path, index=False)

        except Exception as e:
            raise ValueError(f"Ошибка при экспорте: {str(e)}")
    @staticmethod
    def get_currencies():
        # Обновление валют
        currency_rates = get_currency_exchange_rates()
        currencies.update_currencies()

        currencies.cny_rub = currency_rates.get('cny', 12.34)
        currencies.usd_rub = currency_rates.get('usd', 92.25)
        currencies.eur_rub = currency_rates.get('eur', 98.50)
        currencies.yen_rub = currency_rates.get('jpy', 0.591)

    def update_currencies(self):
        self.get_currencies()
        currencies_text = f"CNY={currencies.cny_rub:.2f} USD={currencies.usd_rub:.2f} EUR={currencies.eur_rub:.2f} YEN={currencies.yen_rub:.3f}"
        self.currency_label.config(text=currencies_text)

    def calculate_customs(self):
        # Получаем выбранное значение валюты и типа двигателя
        selected_currency_index = self.currency_combobox.current()
        selected_currency = list(self.currency_symbols.keys())[selected_currency_index]

        selected_engine_type_index = self.engine_type_combobox.current()
        selected_engine_type = list(self.engine_type_symbols.keys())[selected_engine_type_index]

        selected_power_type_index = self.power_type_combobox.current()
        selected_power_type = list(self.power_type_symbols.keys())[selected_power_type_index]

        # Создаем объект heavy с введенными данными
        vehicle = Vehicle(
            self.power_var.get(),
            selected_power_type,
            self.engine_capacity_var.get(),
            self.year_var.get(),
            self.month_var.get(),
            self.price_var.get(),
            selected_currency,
            selected_engine_type
        )

        multiusedFunctions.power_to_type(vehicle)
        # Вызываем функцию для расчета и выводим результат в новом окне
        result_window = tk.Toplevel(self.root)
        result_window.title("Результат расчета")
        result_window.resizable(width=False, height=False)

        if vehicle.engine_type == "euv":
            ttk.Label(result_window, text="Таможенные платежи для электромобиля (физ.лицо):").grid(row=1, column=0,
                                                                                                   columnspan=2, pady=5)
            ttk.Label(result_window, text=f"Цена авто: {int(price_to_rub(vehicle.price, vehicle.currency)):,}").grid(
                row=2, column=0, columnspan=2,
                pady=5)
            ttk.Label(result_window,
                      text=f"Таможенный сбор: {int(customs_fee(price_to_rub(vehicle.price, vehicle.currency))):,}").grid(
                row=3, column=0,
                columnspan=2, pady=5)
            ttk.Label(result_window, text=f"Акциз: {int(customs_excise_physical(vehicle)):,}").grid(row=4, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=5)
            ttk.Label(result_window, text=f"Пошлина: {int(customs_duty_physical(vehicle)):,}").grid(row=5, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=5)
            ttk.Label(result_window, text=f"Утильсбор: {int(customs_utilization_physical(vehicle)):,}").grid(row=6,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             pady=5)
            ttk.Label(result_window, text=f"НДС: {int(vat_physical(vehicle)):,}").grid(row=7, column=0, columnspan=2,
                                                                                       pady=5)
            ttk.Label(result_window, text=f"Суммарно: {int(customs_physical(vehicle)):,}").grid(row=8, column=0,
                                                                                                columnspan=2,
                                                                                                pady=5)
        else:
            ttk.Label(result_window, text="Таможенные платежи для автомобиля (физ.лицо):").grid(row=1, column=0,
                                                                                                columnspan=2, pady=5)
            ttk.Label(result_window, text=f"Цена авто: {int(price_to_rub(vehicle.price, vehicle.currency)):,}").grid(
                row=2, column=0, columnspan=2,
                pady=5)
            ttk.Label(result_window,
                      text=f"Таможенный сбор: {int(customs_fee(price_to_rub(vehicle.price, vehicle.currency))):,}").grid(
                row=3, column=0,
                columnspan=2, pady=5)
            ttk.Label(result_window, text=f"Пошлина: {int(customs_duty_physical(vehicle)):,}").grid(row=4, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=5)
            ttk.Label(result_window, text=f"Утильсбор: {int(customs_utilization_physical(vehicle)):,}").grid(row=5,
                                                                                                             column=0,
                                                                                                             columnspan=2,
                                                                                                             pady=5)
            ttk.Label(result_window, text=f"Суммарно: {int(customs_physical(vehicle)):,}").grid(row=6, column=0,
                                                                                                columnspan=2,
                                                                                                pady=5)

        ttk.Label(result_window, text="Таможенные платежи для автомобиля (юр.лицо):").grid(row=1, column=2,
                                                                                           columnspan=2, pady=5)
        ttk.Label(result_window, text=f"Цена авто: {int(price_to_rub(vehicle.price, vehicle.currency)):,}").grid(row=2,
                                                                                                                 column=2,
                                                                                                                 columnspan=2,
                                                                                                                 pady=5)
        ttk.Label(result_window,
                  text=f"Таможенный сбор: {int(customs_fee(price_to_rub(vehicle.price, vehicle.currency))):,}").grid(
            row=3, column=2,
            columnspan=2, pady=5)
        ttk.Label(result_window, text=f"Пошлина: {int(customs_duty_artificial(vehicle)):,}").grid(row=4, column=2,
                                                                                                  columnspan=2, pady=5)
        ttk.Label(result_window, text=f"Утильсбор: {int(customs_utilization_artificial(vehicle)):,}").grid(row=5,
                                                                                                           column=2,
                                                                                                           columnspan=2,
                                                                                                           pady=5)
        ttk.Label(result_window, text=f"Акциз: {int(customs_excise_artificial(vehicle)):,}").grid(row=6, column=2,
                                                                                                  columnspan=2, pady=5)
        ttk.Label(result_window, text=f"НДС: {int(vat_artificial(vehicle)):,}").grid(row=7, column=2, columnspan=2,
                                                                                     pady=5)
        ttk.Label(result_window, text=f"Суммарно: {int(customs_artificial(vehicle)):,}").grid(row=8, column=2,
                                                                                              columnspan=2,
                                                                                              pady=5)