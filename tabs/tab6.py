# Мировой экспорте, доля страны (%)
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import random



def create_tab(tab_control):
    db_url = 'sqlite:///trade_map.db'
    engine = create_engine(db_url)
    sql_query = 'SELECT * FROM concentration'
    df = pd.read_sql(sql_query, engine)
    df = df.dropna()

    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Концентрация стран-экспортеров') 
    tab_control.pack(expand=1, fill='both')

    
    label_h1 = ttk.Label(tab1, text="Концентрация стран-экспортеров и среднее расстояние до стран назначения",  font=("Arial", 12, "bold"))
    label_h1.pack(side="top", pady=(10, 0))
    
    frame = ttk.Frame(tab1)
    frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    label = ttk.Label(frame, text="Выберите страны:")
    label.pack(side="top", pady=(10, 0))

    country_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE)
    country_listbox.pack(side="left", fill=tk.BOTH, expand=True)
    
    
    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax2 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=frame)
    canvas1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

   
    def update_graph(event):
        ax2.clear()
        selected_products = [country_listbox.get(idx) for idx in country_listbox.curselection()]
        filtered_df = df[df['country'].isin(selected_products)]

        x = list(filtered_df['percent'])
        y = list(filtered_df['distance'])
        z = list(filtered_df['balance'])
        countries_labels = list(filtered_df['country'])
        labels =  [f"Концентрация стран-экспортеров: {x[i]}\nСреднее расстояние со странами назначения, км: {y[i]}\nТорговый баланс: {z[i]}" for i in range(len(filtered_df))]
        colors = ['yellow' if balance < 0 else 'blue' for balance in filtered_df['balance']]

        # Нормализация массива z от 100 до 5000
        z_min = min(z)
        z_max = max(z)
        new_min, new_max = 100, 5000
        z_normalized = [((value - z_min) / (z_max - z_min)) * (new_max - new_min) + new_min for value in z]


        # fig, ax = plt.subplots()

        scatter = ax2.scatter(x, y, s=z_normalized, c=colors)  # s определяет радиус каждой точки

        # Создание подсказок
        annot = ax2.annotate("", xy=(0,0), xytext=(20,20),
                    textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            pos = scatter.get_offsets()[ind["ind"][0]]
            annot.xy = pos
            text = f"{labels[ind['ind'][0]]}"
            annot.set_text(text)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax2:
                cont, ind = scatter.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    fig1.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig1.canvas.draw_idle()

        fig1.canvas.mpl_connect("motion_notify_event", hover)
        for i, txt in enumerate(countries_labels):
            ax2.text(x[i], y[i], txt, fontsize=12, ha='center', va='center')

        fig1.canvas.draw_idle()
        # Добавление условной метки
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Отрицательный торговый баланс',
                                markerfacecolor='yellow', markersize=10),
                        Line2D([0], [0], marker='o', color='w', label='Положительный торговый баланс',
                                markerfacecolor='blue', markersize=10)]
        ax2.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1.15))
        ax2.set_xlabel('Концентрация стран-экспортеров')
        ax2.set_ylabel('Среднее расстояние со странами назначения, км')

    def on_tab_load(event):
        countries = df['country']
        for country in countries:
            country_listbox.insert(tk.END, country)
        country_listbox.selection_set(2)
        country_listbox.selection_set(4)
        country_listbox.selection_set(5)
        update_graph(None)

    on_tab_load(None)
    country_listbox.bind("<<ListboxSelect>>", update_graph)
    tab1.bind("<Visibility>", on_tab_load)

    return tab1