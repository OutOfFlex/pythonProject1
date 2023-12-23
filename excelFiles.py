import pandas as pd

def import_excel(file_path):
    try:
        # Чтение данных из Excel
        df = pd.read_excel(file_path, header = 2)

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
        for i in range(2,df["Your_Column"].last_valid_index()):
            if df.iat[i, 1] == 1:
                light_excel(df)
            elif df.iat[i, 1] == 2:
                heavy_excel(df)
            else:
                raise ValueError(f"Ошибка при экспорте: {str(Exception)}")
        # Запись DataFrame в Excel
        df.to_excel(file_path, index=False)

    except Exception as e:
        raise ValueError(f"Ошибка при экспорте: {str(e)}")

def heavy_excel(df):
    try:
        raise NotImplementedError
    except Exception as e:
        raise ValueError(f"Ошибка при экспорте: {str(e)}")

def light_excel(df):
    try:
        raise NotImplementedError
    except Exception as e:
        raise ValueError(f"Ошибка при экспорте: {str(e)}")