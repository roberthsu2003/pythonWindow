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

        self.cityvar = tk.StringVar()
        city_combobox = ttk.Combobox(left_label_frame, textvariable=self.cityvar)
        city_combobox.pack(side=tk.LEFT)
        city_combobox['values'] = cities
        city_combobox.state(["readonly"])
        city_combobox.bind('<<ComboboxSelected>>', self.city_selected)
        left_label_frame.pack(side=tk.LEFT,anchor=tk.N)
        #左邊容器==================end

        #右邊容器==================start
        right_label_frame = tk.LabelFrame(self, text="右邊容器",bg='blue')
        siteLabel = ttk.Label(right_label_frame, text="站點:")
        siteLabel.pack(side=tk.LEFT, padx=(50, 0),anchor=tk.N)


        self.choicesvar = tk.StringVar(value=[])
        site_listbox = tk.Listbox(right_label_frame, height=10,listvariable=self.choicesvar)
        site_listbox.pack(side=tk.LEFT,padx=(0,50),pady=(0,30))
        site_listbox.bind("<<ListboxSelect>>", self.site_selected)
        right_label_frame.pack(side=tk.RIGHT)
        # 右邊容器==================end

    #comboboxbind的事件
    def city_selected(self,event):
        selectedCity = self.cityvar.get()
        sites = dataSource.get_site_name(selectedCity)
        self.choicesvar.set(sites)

    #listboxbind事件
    def site_selected(self,event):
        selectedIndex = event.widget.curselection()
        if not selectedIndex:
            return
        site = event.widget.get(selectedIndex)
        siteInfo = dataSource.get_site_info(site)
        print(siteInfo)








if __name__ == "__main__":
    dataSource.download_save_to_DataBase()
    city_name_list = dataSource.get_city_name()
    window = Window(city_name_list)
    window.title("PM2.5")
    window.mainloop()