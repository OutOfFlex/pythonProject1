import requests
import xml.etree.ElementTree as ET


def get_currency_exchange_rates():
    # Запрос курсов валют с ЦБ РФ
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content
        # Парсим XML и извлекаем курсы валют
        currency_rates = {}
        root = ET.fromstring(content)
        for valute in root.findall('.//Valute'):
            currency_id = valute.find('CharCode').text.lower()
            rate = float(valute.find('VunitRate').text.replace(',', '.'))
            currency_rates[currency_id] = rate
        return currency_rates
    else:
        print("Failed to retrieve currency exchange rates.")
        return {}


eur_rub = 98.50
cny_rub = 12.34
yen_rub = 0.591
usd_rub = 92.25


# Обновить валюты в приложении
def update_currencies():
    global cny_rub
    global usd_rub
    global eur_rub
    global yen_rub
    # Обновление валют
    currency_rates = get_currency_exchange_rates()

    cny_rub = currency_rates.get('cny', 12.34)
    usd_rub = currency_rates.get('usd', 92.25)
    eur_rub = currency_rates.get('eur', 98.50)
    yen_rub = currency_rates.get('jpy', 0.591)
