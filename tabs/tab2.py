import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import export_ml_model_total

import pandas as pd

def create_tab(tab_control):
    
    def update_graph(event):
        ax1.clear()  # Clear the previous graph to avoid overlaying
        # Данные для столбчатой диаграммы
        df = pd.read_excel('trade_map\\tab2.xlsx')

        # Extract data from the DataFrame
        x = df['x'].tolist()
        y = df['y'].tolist()
        
        if get_predict():
            for i in range(get_predict_count()):
                x_add = x[-1] + 1
                predict = export_ml_model_total.perdict(x_add)
                x.append(x_add)
                y.append(predict)
                
        rounded_x = [str(round(val, 1)) for val in x]
        
        # Построение столбчатой диаграммы
        ax1.bar(rounded_x, y, label="Экспорт продукции АПК 2010 – 2023 гг. (млрд $)", color='skyblue')

        # Добавляем заголовок и метки осей
        ax1.set_title('Экспорт продукции АПК 2010 – 2023 гг. (млрд $)')
        ax1.set_xlabel('Год')
        ax1.set_ylabel('Экспорт (млрд $)')
        
        # Redraw the canvas
        canvas1.draw_idle()
   
    def get_predict():
        return predict.get()
    
    def get_predict_count():
        try:
            my_integer = int(count_predict.get())
            return min(max(my_integer, 1), 10)
        except ValueError:
            return 3
          
    def entry_changed(*args):
        value = count_predict.get()
        update_graph(None)  # Update graph after validation
    
    def checkbox_changed():
        update_graph(None)  # Update graph when checkbox state changes

    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Экспорт продукции АПК')
    tab_control.pack(expand=1, fill='both')

    predict_label_frame = ttk.Labelframe(tab1, text="Предсказать изменение АПК", bootstyle="info")
    predict_label_frame.pack(side="top", pady=(20, 5), padx=20, fill="both", expand=True)
    
    predict = tk.BooleanVar()
    predict.set(False)
    checkbox = ttk.Checkbutton(predict_label_frame, text="Предсказывать значение", variable=predict, bootstyle="success-round-toggle", command=checkbox_changed)
    checkbox.pack(side="top", pady=(5, 0), padx=20)

    count_predict_label = ttk.Label(predict_label_frame, text="Количество лет для предсказания", anchor="center")    
    count_predict_label.pack(side="top", pady=(20, 0), padx=20)

    count_predict = tk.StringVar(value="3")
    entry = ttk.Entry(predict_label_frame, textvariable=count_predict, bootstyle="success")
    entry.pack(side="top", pady=(5, 20), padx=20)
    count_predict.trace_add("write", entry_changed)  # Trace changes to the entry widget

    # Создаем график
    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax1 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    update_graph(None)  # Initial graph update
    return tab1
