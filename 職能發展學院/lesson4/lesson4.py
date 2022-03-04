import tkinter as tk
from tkinter import ttk
from tkinter import font
import dataSource

class Window(tk.Tk):
    def __init__(self,cities):
        super().__init__()
        #title_Font = font.nametofont('TkCaptionFont')
        self.configure(background='white')
        title_Font = font.Font(family='Helvetica', size=20, weight='bold')
        titleLabel = ttk.Label(self, text="台灣即時PM2.5",font=title_Font,anchor=tk.CENTER)
        titleLabel.pack(fill=tk.X, pady=20)

        #左邊容器==================start
        left_label_frame = tk.LabelFrame(self,text="左邊容器",background="red")
        cityLabel = ttk.Label(left_label_frame, text="城市:")
        cityLabel.pack(side=tk.LEFT,padx=(50,0))

        cityvar = tk.StringVar()
        city_combobox = ttk.Combobox(left_label_frame, textvariable=cityvar)
        city_combobox.pack(side=tk.LEFT)
        city_combobox['values'] = cities
        city_combobox.state(["readonly"])
        left_label_frame.pack(side=tk.LEFT)
        #左邊容器==================end

        #右邊容器==================start
        right_label_frame = tk.LabelFrame(self, text="右邊容器",bg='blue')
        siteLabel = ttk.Label(right_label_frame, text="站點:")
        siteLabel.pack(side=tk.LEFT, padx=(50, 0))

        site_listbox = tk.Listbox(right_label_frame, height=10)
        site_listbox.pack(side=tk.LEFT,padx=(0,50),pady=(0,30))
        right_label_frame.pack(side=tk.RIGHT)
        # 右邊容器==================end



if __name__ == "__main__":
    dataSource.download_save_to_DataBase()
    city_name_list = dataSource.get_city_name()
    window = Window(city_name_list)
    window.title("PM2.5")
    window.mainloop()