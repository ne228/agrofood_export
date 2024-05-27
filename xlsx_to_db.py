import pandas as pd
from sqlalchemy import create_engine

# Чтение данных из файла Excel
file_path = 'trade_map\\export_all.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# Подключение к базе данных SQLite (или замените на вашу базу данных)
# Например, для SQLite:
database_url = 'sqlite:///trade_map.db'

# Для других баз данных, например, PostgreSQL:
# database_url = 'postgresql://username:password@localhost/trade_map'

engine = create_engine(database_url)

# Запись данных в таблицу import_all
df.to_sql('export_all', engine, if_exists='replace', index=False)

print("Данные успешно импортированы в базу данных")