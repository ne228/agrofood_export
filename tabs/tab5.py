# Мировой экспорте, доля страны (%)
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import random

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
    sql_query = 'SELECT * FROM dolya_products'
    df = pd.read_sql(sql_query, engine)
    df = df.dropna()

    tab1 = tk.Frame(tab_control)
    tab_control.add(tab1, text='Мировой экспорт продуктов')
    tab_control.pack(expand=1, fill='both')

    fig1 = Figure(figsize=(5, 4), dpi=100)
    ax2 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
    canvas1.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    product_frame = ttk.Frame(tab1)
    product_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    product_label = ttk.Label(product_frame, text="Выберите продукты:")
    product_label.pack(side="top", pady=(10, 0))

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
        y = list(filtered_df['percent'])
        # Генерация цветов
        bar_colors = colors[:len(x)]
        
        ax2.pie(y, labels=x, autopct='%1.1f%%')
        # bars = ax2.bar(x, y, color=bar_colors)
        ax2.set_title('Эскпорт продуктов в РФ, %')

        # ax2.set_xticklabels(x, fontsize=8, rotation=0, ha='center')

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