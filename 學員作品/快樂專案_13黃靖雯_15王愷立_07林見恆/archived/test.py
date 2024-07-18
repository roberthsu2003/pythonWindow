import tkinter as tk
from tkinter import ttk, messagebox, Misc
from ttkthemes import ThemedTk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the custom dataset
data_path = '/Users/jesshuang/Documents/GitHub/jess_window/project/the_happiness_project/World Happiness Report_new.csv'
custom_data = pd.read_csv(data_path).to_dict(orient='records')

class Window(ThemedTk):
    def __init__(self, theme:str='arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title("World Happiness Report")
        try:
            self.__data = custom_data
        except Exception as error:
            messagebox.showwarning(title="Error", message=str(error))

        self._display_interface()

    @property
    def data(self) -> list[dict]:
        return self.__data

    def _display_interface(self):
        mainFrame = ttk.Frame(borderwidth=1, relief="groove")
        ttk.Label(mainFrame, text="World Happiness Report Data", font=('arial',16)).pack(pady=(20,10))

        tableFrame = ttk.Frame(mainFrame)
        columns = list(custom_data[0].keys())  # Extract columns from dataset
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings')

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor=tk.CENTER, width=100)

        tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Add data to the treeview
        for record in self.data:
            tree.insert('', tk.END, values=list(record.values()))

        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        tableFrame.pack(ipadx=20, ipady=20)

        self.pieChartFrame = PieChartFrame(mainFrame)
        self.pieChartFrame.pack()
        mainFrame.pack(padx=10, pady=10)

    def item_selected(self, event):
        tree = event.widget
        records = []
        for selected_item in tree.selection()[:3]:
            item = tree.item(selected_item)
            record = item['values']
            records.append(record)
        self.pieChartFrame.infos = records

class PieChartFrame(ttk.Frame):
    def __init__(self, master: Misc, **kwargs):
        super().__init__(master=master, **kwargs)
        self.configure({'borderwidth': 2, 'relief': 'groove'})
        style = ttk.Style()
        style.configure('abc.TFrame', background='#ffffff')
        self.configure(style='abc.TFrame')

    @property
    def infos(self) -> None:
        return None

    @infos.setter
    def infos(self, datas: list[list]) -> None:
        for w in self.winfo_children():
            w.destroy()

        for data in datas:
            oneFrame = ttk.Frame(self, style='abc.TFrame')
            for i, (key, value) in enumerate(zip(custom_data[0].keys(), data)):
                ttk.Label(oneFrame, text=f"{key}: ").grid(row=i, column=0, sticky='e')
                ttk.Label(oneFrame, text=str(value)).grid(row=i, column=1, sticky='w')

            oneFrame.pack(side='left', expand=True, fill='both')

def main():
    def on_closing():
        window.destroy()

    window = Window(theme='breeze')
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

if __name__ == '__main__':
    main()