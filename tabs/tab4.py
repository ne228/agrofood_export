import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import random


def generate_hex_color(i):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # Форматирование в строку в формате #RRGGBB
    return '#{r:02x}{g:02x}{b:02x}'.format(r=r, g=g, b=b)

def create_tab(tab_control):
    db_url = 'sqlite:///trade_map.db'
    engine = create_engine(db_url)
    sql_query = 'SELECT * FROM total_products'
    df = pd.read_sql(sql_query, engine)
    df = df.dropna()

    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Экспорт продукции АПК детализированный')
    tab_control.pack(expand=1, fill='both')

    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax2 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    product_frame = ttk.Frame(tab1)
    product_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    product_label = ttk.Label(product_frame, text="Выберите продукты:")
    product_label.pack(side="left", pady=(10, 0))

    product_list_box = tk.Listbox(product_frame, selectmode=tk.MULTIPLE)
    product_list_box.pack(side="left", fill=tk.BOTH, expand=True)
    cmap = plt.get_cmap('tab20') 
    count = df['product'].count()
    colors = [generate_hex_color(i) for i in range(count)]
   
    def update_graph(event):
        ax2.clear()
        selected_products = [product_list_box.get(idx) for idx in product_list_box.curselection()]
        filtered_df = df[df['product'].isin(selected_products)]
        x = list(filtered_df['product'])
        y = list(filtered_df['cost'])
        # Генерация цветов
        bar_colors = colors[:len(x)]
        bars = ax2.bar(x, y, color=bar_colors)
        ax2.set_title('Экспорт продукции АПК 2010 – 2023 гг. (млрд $)')
        ax2.set_xlabel('Продукты')
        ax2.set_ylabel('Экспорт (тыс $)')

        ax2.set_xticklabels(x, fontsize=8, rotation=0, ha='center')

        # Добавляем подсказки для каждого столбца
        for bar in bars:
            height = bar.get_height()
            ax2.annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 0),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom')
        fig1.canvas.draw_idle()

    def on_tab_load(event):
        products = df['product']
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