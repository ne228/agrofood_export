import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import random


def get_country_code(country):
    db_url = 'sqlite:///trade_map.db'
    engine = create_engine(db_url)
    sql_query = f'SELECT * FROM country_cods WHERE country=\"{country}\"'
    df = pd.read_sql(sql_query, engine)
    df = df.dropna()
    print(df.head(5))
    if (len(df) == 0):
        return 0
    return df['code'][0]
