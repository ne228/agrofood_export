import pandas as pd

# Данные
x = ["Зерновые", "Масложировая продукция", 
     "Рыба и морепродукты", "Продукция пищевой и перерабатывающей промышленности",
     "Прочая продукция АПК", "Мясная и молочная продукция"]
y =  [32, 22, 14, 13, 15, 4]

# Создаем DataFrame
df = pd.DataFrame({'Продукция': x, 'Значения': y})

# Сохраняем в файл Excel
df.to_excel('trade_map\\tab3.xlsx', index=False)
