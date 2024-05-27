import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

def create_tab(tab_control):
     tab1 = tk.Frame(tab_control)

     tab_control.add(tab1, text='Структура экспорта продукции АПК')
     tab_control.pack(expand=1, fill='both')

     # Создаем график
     fig1 = Figure(figsize=(5, 4), dpi=100)
     ax1 = fig1.add_subplot(111)
     canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
     canvas1.draw()
     canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

     # Данные для столбчатой диаграммы
     df = pd.read_excel('trade_map\\tab3.xlsx')

     # Извлекаем столбцы
     x = df['Продукция'].tolist()
     y = df['Значения'].tolist()


     # Добавляем заголовок и метки осей
     ax1.set_title('Структура экспорта продукции АПК из России в 2023 году, %')

     ax1.pie(y, labels=x, autopct='%1.1f%%')


     return tab1
