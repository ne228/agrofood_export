import joblib
import pandas as pd
import get_country_code

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

import joblib

# Загрузка модели
pipeline = joblib.load('models\\export_polynomial_regression_model.pkl')


def predict_output(year, country):
    country_code = get_country_code.get_country_code(country)
    input_data = pd.DataFrame({'year': [year], 'country_code': [country_code]})
    predicted_output = pipeline.predict(input_data)
    
    return predicted_output[0]



