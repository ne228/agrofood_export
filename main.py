import tkinter as tk
from tkinter import ttk

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tabs import tab1
from tabs import tab2
from tabs import tab3
from tabs import tab4
from tabs import tab5
from tabs import tab6
from tabs import tab7

from ttkbootstrap import Style

def main():
    root = tk.Tk()
    root.title("Экспорт АПК")
    root.minsize(1000, root.winfo_height())
    style = Style(theme="litera")
    tab_control = ttk.Notebook(root, bootstyle="secondary")
    tab1.create_tab(tab_control)
    tab2.create_tab(tab_control)
    tab3.create_tab(tab_control)
    tab4.create_tab(tab_control)
    tab5.create_tab(tab_control)
    tab6.create_tab(tab_control)
    tab7.create_tab(tab_control)
    
    

    tab_control.pack(expand=1, fill='both')

    root.mainloop()

if __name__ == "__main__":
    main()
