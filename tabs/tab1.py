import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sqlalchemy import create_engine, Table, MetaData, select
import pandas as pd
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import mplcursors


import export_ml_model


# Создаем вкладки
def create_tab(tab_control):        

    def get_value_table():
        # print(my_dict.get(tb_combobox.get()))
        return my_dict.get(tb_combobox.get())

    def get_country_data(table, database_path='trade_map.db'):
        # Подключение к базе данных SQLite
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        try:
            # Выполнение SQL запроса
            cursor.execute(f'SELECT DISTINCT country FROM {table}')
            
            # Извлечение результатов запроса
            countries = [row[0] for row in cursor.fetchall()]
            # print(countries)
            return countries
        finally:
            # Всегда закрываем соединение, чтобы избежать утечек ресурсов
            conn.close()

    def get_data_by_country(table, country, database_path='trade_map.db'):
        # Подключение к базе данных
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        try:
            # Выполнение SQL запроса с использованием параметров
            sql = f'SELECT * FROM {table} WHERE country = \"{country}\"'
            # print(sql)
            cursor.execute(sql)
            
            # Получение результатов запроса
            rows = cursor.fetchall()
            return rows
        finally:
            # Всегда закрываем соединение, чтобы избежать утечек ресурсов
            conn.close()

    # Обновление списка стран в зависимости от выбранной базы данных
    def update_country_list(event):
        country_list_box.delete(0, tk.END)   
        table = get_value_table()
        values = get_country_data(table)
        
        for value in values:
            country_list_box.insert(tk.END, value) 
            
        country_list_box.selection_set(0) 
        update_graph(None) 

              
    def on_tab_load(event):
        tb_combobox.current(0)
        update_country_list(None)
    
    def entry_changed(*args):
        update_graph(None)
        value = entry_var.get()
        if not value.isdigit() or int(value) < 1 or int(value) > 10:
            entry_var.set("3")
    
    def checkbox_changed():
        update_graph(None)
    
    def get_predict():
        return predict.get()
    
    def get_predict_count():
        try:
            my_integer = int(entry.get())
            if (my_integer > 10):
                return 10
            return my_integer
        except ValueError:
            return 3
          
    
    
    def update_graph(event):    
        ax1.clear()  
        selected_table = get_value_table()
        selected_countries = [country_list_box.get(idx) for idx in country_list_box.curselection()]     
               
        for country in selected_countries:
            data = get_data_by_country(selected_table, country)
            x = []
            y = []
            for i in data:
                x.append(i[1])
                y.append(i[2])          
            
           
            if get_predict():
                for i in range(get_predict_count()):
                    x_add = x[len(x) - 1 ] + 1
                    
                    predict = export_ml_model.predict_output(x_add, country)
                    x.append(x_add)
                    y.append(predict)
            # Построение графиков
            rounded_x = [str(round(val, 1)) for val in x]
            # ax1.set_xticklabels(rounded_x)
            ax1.plot(rounded_x, y, label=data[0][0])  # Первый график
            
            
        # Установка меток и легенды
        ax1.set_xlabel('Год')
        ax1.set_ylabel('тыс. $')
        ax1.legend(loc='best')

        ax1.figure.subplots_adjust(left=0.2) 

        canvas1.draw()
    
  
  
    my_dict = {"Экспорт": "export_all"}
    
    tab1 = tk.Frame(tab_control)
        
    label_h1 = ttk.Label(tab1, text="Цена экспорта РФ",  font=("Arial", 12, "bold"))
    label_h1.pack(side="top", pady=(10, 0))

    tab_control.add(tab1, text='Экспорт')
    tab_control.pack(expand=1, fill='both')
    
    frame_top = tk.Frame(tab1)
    frame_top.pack(side="right")

    frame_left = tk.Frame(frame_top)
    frame_left.pack(side="top")
    # Создаем выпадающий список для выбора базы данных
    db_label = ttk.Label(frame_left, text="Экспорт", anchor="center")
    db_label.pack(side="top")
    tb_combobox = ttk.Combobox(frame_left)
    tb_combobox['values'] = list(my_dict.keys())
    tb_combobox.pack(side="top")


    frame_right = tk.Frame(frame_top)
    frame_right.pack(side="top")
    # Создаем выпадающий список для выбора страны
    country_label = ttk.Label(frame_right, text="Выберите страну", anchor="center")
    country_label.pack(side="top", padx=(0, 0))
    window_width = tab1.winfo_width()
    country_list_box = tk.Listbox(frame_right, selectmode=tk.MULTIPLE, width=50)
    country_list_box.config(height=10)
    country_list_box.pack(side="top")
    
    predict_label_frame = ttk.Labelframe(frame_right, text="Предсказать изменение АПК", bootstyle="info")
    predict_label_frame.pack(side="top", pady=(20, 5), padx=20,  fill="both", expand=True)
    
    predict = tk.BooleanVar()
    predict.set(False)
    checkbox = ttk.Checkbutton(predict_label_frame, text="Предсказывать значение", variable=predict, bootstyle="success-round-toggle", command=checkbox_changed)
    checkbox.pack(side="top",  pady=(5,0), padx=20)


    count_predict_label = ttk.Label(predict_label_frame, text="Количество лет для предсказания", anchor="center")    
    count_predict_label.pack(side="top", pady=(20, 0), padx=20)
    count_predict = tk.StringVar()
    entry = ttk.Entry(predict_label_frame, textvariable=count_predict, bootstyle="success")
    entry.pack(side="top", pady=(5,20), padx=20)
    entry.bind("<<Modified>>", entry_changed)

    # Создаем график
    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax1 = fig1.add_subplot(111)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


   
   
    tb_combobox.bind("<<ComboboxSelected>>", update_country_list)
    tb_combobox.current(0)
    country_list_box.bind("<<ListboxSelect>>", update_graph)
    update_country_list(None)
    tb_combobox.bind("<Visibility>", on_tab_load)
    return tab1


