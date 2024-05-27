# Мировой экспорте, доля страны (%)
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def generate_hex_color(i):
# Генерация случайных чисел для каждой из составляющих цвета
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Форматирование в строку в формате #RRGGBB
    return '#{r:02x}{g:02x}{b:02x}'.format(r=r, g=g, b=b)



def create_tab(tab_control):

                
                
    db_url = 'sqlite:///trade_map.db'
    engine = create_engine(db_url)
    sql_query = 'SELECT * FROM regions'
    df = pd.read_sql(sql_query, engine)
    df = df.dropna()

    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Экспорт по регионам РФ')
    tab_control.pack(expand=1, fill='both')
    
    label_h1 = ttk.Label(tab1, text="Экспорт по регионам РФ",  font=("Arial", 12, "bold"))
    label_h1.pack(side="top", pady=(10, 0))

    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax2 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    product_frame = ttk.Frame(tab1)
    product_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    product_label = ttk.Label(product_frame, text="Выберите регионы:")
    product_label.place(relx=0.5, rely=0.5, anchor="center")
    product_label.pack(side="top", pady=(10, 0), padx=0)

    product_list_box = tk.Listbox(product_frame, selectmode=tk.MULTIPLE)
    product_list_box.pack(side="top", fill=tk.BOTH, expand=True)
    
    factor_label = ttk.Label(product_frame, text="Выберите факторы:")
    factor_label.pack(side="top", pady=(10, 0))

    # Флаги
    
    flag_frame = ttk.Frame(product_frame)
    flag_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    checkboxes = []
        
    def on_checkbox_change(var):
        for checkbox in checkboxes:
            if checkbox != var:
                checkbox.set(False)
        update_graph(None)
    
    population_var = tk.BooleanVar()
    population_checkbox = ttk.Checkbutton(flag_frame, text="Население", variable=population_var, bootstyle="primary",command=lambda: on_checkbox_change(population_var))
    population_checkbox.pack(side="top", padx=5, pady=2, fill=tk.X)
    
    avg_t_june_var = tk.BooleanVar()
    avg_t_june_checkbox = ttk.Checkbutton(flag_frame, text="Средння температура июня", variable=avg_t_june_var, bootstyle="primary", command=lambda: on_checkbox_change(avg_t_june_var))
    avg_t_june_checkbox.pack(side="top", padx=5, pady=2, fill=tk.X)
    
    avg_t_january_var = tk.BooleanVar()
    avg_t_januart_checkbox = ttk.Checkbutton(flag_frame, text="Средння температура января", variable=avg_t_january_var, bootstyle="primary", command=lambda: on_checkbox_change(avg_t_january_var))
    avg_t_januart_checkbox.pack(side="top", padx=5, pady=2, fill=tk.X)
    
    square_var = tk.BooleanVar()
    square_checkbox = ttk.Checkbutton(flag_frame, text="Площадь", variable=square_var,  bootstyle="primary", command=lambda: on_checkbox_change(square_var))
    square_checkbox.pack(side="top", padx=5, pady=2, fill=tk.X)
    checkboxes = [population_var, avg_t_june_var, avg_t_january_var, square_var]
    

    
    cmap = plt.get_cmap('tab20') 
    count = df['region'].count()
    colors = [generate_hex_color(i) for i in range(count)]
    def normalize_value(values, new_min, new_max):
        values = [abs(x) for x in values]
        old_min = min(values)
        old_max = max(values)
        normalized_values = [(x - old_min) * (new_max - new_min) / (old_max - old_min) + new_min for x in values]
        return normalized_values

    
    def update_graph(event):
        ax2.clear()
        selected_products = [product_list_box.get(idx) for idx in product_list_box.curselection()]
        filtered_df = df[df['region'].isin(selected_products)]
        x = list(filtered_df['region'])
        y = list(filtered_df['cost'])

        bar_width = 0.35
        indices = np.arange(len(x))
        
        bar1 = ax2.barh(indices, y, bar_width, label='Цена, млн $')
        for i, (bar, val) in enumerate(zip(bar1, y)):
            ax2.text(bar.get_width(), bar.get_y() + bar.get_height()/3, f'{val:.2f} млн $', 
                    va='center', ha='left', fontsize=8)
            
        offset = bar_width
        factors = [population_var, avg_t_june_var, avg_t_january_var, square_var]
        labels = ['Население, тыс. чел.', 'Ср. температура в июне, °C', 'Ср. температура в январе, °C', 'Площадь, le1. км²']
        data_columns = ['population', 'avg_t_june', 'avg_t_january', 'square']
        label_bars = [' тыс. чел.', ' °C', ' °C', ' le1. км²']

        # Перебор факторов и создание столбцов
        for factor, label, data_column, label_bar in zip(factors, labels, data_columns, label_bars):            
            if factor.get():
                p = list(filtered_df[data_column])
                normalize_values = []
                if data_column == 'square':
                    normalize_values = [float(x) * 100 for x in p]
                    
                if data_column == 'avg_t_june':
                    normalize_values = normalize_value( p, 100, 8000 )
                    
                if data_column == 'avg_t_january':
                    normalize_values = normalize_value( p, 100, 8000 )
                    
                if data_column == 'population':
                    normalize_values = p
                    
                bar_create = ax2.barh(indices + offset, normalize_values, bar_width, label=label)
                for i, (bar, val) in enumerate(zip(bar_create, p)):
                    ax2.text(bar.get_width(), bar.get_y() + bar.get_height()/3, f'{val} {label_bar}', 
                            va='center', ha='left', fontsize=8)
                offset += bar_width  # Смещение для следующего столбца

        ax2.set(yticks=indices , yticklabels=x)
        ax2.legend()
        ax2.set_yticklabels(x, fontsize=10, ha='center')
        fig1.canvas.draw_idle()

    def on_tab_load(event):
        products = df['region']
        for product in products:
            product_list_box.insert(tk.END, product)
        product_list_box.selection_set(2)
        product_list_box.selection_set(4)
        product_list_box.selection_set(5)
        

        update_graph(None)
    


    on_tab_load(None)
    product_list_box.bind("<<ListboxSelect>>", update_graph)
    tab1.bind("<Visibility>", on_tab_load)

    return tab1