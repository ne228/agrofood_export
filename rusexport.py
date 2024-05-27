import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sqlalchemy import create_engine, Table, MetaData, select
import pandas as pd
# from ttkbootstrap import Style
import sqlite3
import mplcursors

my_dict = {"Весь импорт": "import_all", 
           "Весь экспорт": "export_all"}
  
# Создаем основное окно приложения
root = tk.Tk()
root.title("Агропродовольственный экспорт России")
root.minsize(1000, root.winfo_height())

# Создаем вкладки
tab_control = ttk.Notebook(root)
tab1 = tk.Frame(tab_control)

frame_top = tk.Frame(tab1)
frame_top.pack(side="top")

tab_control.add(tab1, text='Trade Map')
tab_control.pack(expand=1, fill='both')

# Создаем график
fig1 = Figure(figsize=(5, 4), dpi=100)
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
canvas1.draw()
canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

# Данные для столбчатой диаграммы
x = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
y =  [8.1, 12, 17.3, 16.8, 19.1, 17, 17.8, 21.6, 25.8, 25.6, 30.6, 37.1, 41.6]

# Построение столбчатой диаграммы
ax1.bar(x, y, label="Экспорт продукции АПК 2010 – 2022 гг. (млрд $)", color='skyblue')

# Добавляем заголовок и метки осей
ax1.set_title('Экспорт продукции АПК 2010 – 2022 гг. (млрд $)')
ax1.set_xlabel('Год')
ax1.set_ylabel('Экспорт (млрд $)')

# Добавляем легенду
ax1.legend()

root.mainloop()
