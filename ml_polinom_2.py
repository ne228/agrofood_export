import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import joblib
import os

# Ваши данные
X = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
y = [8.1, 12, 17.3, 16.8, 19.1, 17, 17.8, 21.6, 25.8, 25.6, 30.6, 37.1, 41.6]

# Преобразование строк в список чисел с плавающей точкой
X_float = np.array(list(map(float, X))).reshape(-1, 1)
y_float = np.array(y)

# Создание модели полиномиальной регрессии
degree = 2  # Степень полинома
poly_features = PolynomialFeatures(degree=degree)
X_poly = poly_features.fit_transform(X_float)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_poly, y_float)

# Предсказание на всех данных
years_to_predict = np.array([float(year) for year in range(2010, 2029)]).reshape(-1, 1)
X_poly_predict = poly_features.transform(years_to_predict)
predictions = model.predict(X_poly_predict)

# Визуализация фактических и предсказанных значений на всех годах
plt.scatter(years_to_predict, predictions, color='red', label='Predicted values')
plt.scatter(X_float, y_float, color='blue', label='Actual values')
plt.xlabel('Year')
plt.ylabel('y')
plt.legend()
plt.title('Actual vs Predicted Values (2010-2028)')
plt.show()

# Убедитесь, что директория существует
os.makedirs('models', exist_ok=True)

# Сохранение модели и объектов в файл
joblib.dump(model, 'models/export_totao_polynomial_regression_model.pkl')
joblib.dump(poly_features, 'models/poly_features.pkl')
np.save('models/years_to_predict.npy', years_to_predict)
np.save('models/predictions.npy', predictions)
