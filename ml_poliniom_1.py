import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Загрузка данных из Excel
data = pd.read_excel('trade_map\\export_dataset_copy.xlsx')

# Извлечение признаков и целевой переменной
X = data[['year', 'country_code']]
y = data['y']

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание пайплайна с полиномиальными признаками и линейной регрессией
degree = 2  # Степень полинома, можно попробовать разные значения
pipeline = Pipeline([
    ('poly_features', PolynomialFeatures(degree=degree)),
    ('regressor', LinearRegression())
])

# Обучение модели
pipeline.fit(X_train, y_train)

# Предсказание на тестовых данных
y_pred = pipeline.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (MSE): {mse}')
print(f'R^2 Score: {r2}')



# Сохранение модели
joblib.dump(pipeline, 'export_polynomial_regression_model.pkl')

# Загрузка модели
pipeline_loaded = joblib.load('export_polynomial_regression_model.pkl')