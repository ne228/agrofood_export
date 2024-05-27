import numpy as np
import matplotlib.pyplot as plt
import joblib

# Загрузка модели и объектов
model = joblib.load('models/export_totao_polynomial_regression_model.pkl')
poly_features = joblib.load('models/poly_features.pkl')

def perdict(year):
    """
    Предсказывает значение для одного года с использованием загруженной модели полиномиальной регрессии.

    Parameters:
    year (int): Год для предсказания

    Returns:
    float: Предсказанное значение
    """
    year_array = np.array([[float(year)]])  # Преобразование года в массив 2D
    year_poly = poly_features.transform(year_array)  # Преобразование с полиномиальными признаками
    prediction = model.predict(year_poly)  # Предсказание с использованием модели
    return prediction[0]
 
