import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import datasource

filterWrose_numbers=3

class MyWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.selectdata = None  # Placeholder for the data

        # add menubar that contains a menu
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        # add command menu in menubar
        self.command_menu = tk.Menu(self.menubar)
        self.command_menu.add_command(label="設定", command=self.menu_setting_click)
        self.command_menu.add_command(label="離開", command=self.destroy)
        self.menubar.add_cascade(label="選項", menu=self.command_menu)

        
        # topFrame
        self.topFrame = ttk.Labelframe(self)
        self.topFrame.pack(side=tk.TOP)

        # bottomFrame
        self.bottomFrame = ttk.LabelFrame(self)
        self.bottomFrame.pack()

        # add pic
        pic001Image1 = Image.open("./images/pic001.jpg")
        self.pic001 = ImageTk.PhotoImage(pic001Image1)
        self.canvas = tk.Canvas(self.topFrame, width=500, height=250)
        self.canvas.pack()
        self.canvas.create_image(0, 5, image=self.pic001, anchor='nw')
        # add logo
        logoImage = Image.open('./Images/co2logo.png')
        resizeImage = logoImage.resize((89, 82), Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        self.canvas.create_image(20, 30, image=self.logoTkimage, anchor='nw')

        # Create the combobox
        self.combobox_frame = ttk.Frame(self.topFrame)
        self.combobox_frame.pack(pady=10)
        self.combobox_label = ttk.Label(self.combobox_frame, text="Select Country:")
        self.combobox_label.pack(side=tk.LEFT)
        self.combobox = ttk.Combobox(self.combobox_frame, state="readonly")
        self.combobox.pack(side=tk.LEFT)

        self.selectdata = datasource.getInfo()

        country_list = self.selectdata['country'].unique().tolist()
        country_list = sorted(country_list)
        country_list.insert(0, '請選擇一個國家vvv')
        self.combobox_values = tuple(country_list)
        self.combobox['values'] = self.combobox_values
        self.combobox.current(0)  # select the first country by default
        self.combobox.bind("<<ComboboxSelected>>", self.update_treeview)

        # Create the treeview
        columns = ('#1', '#2', '#3', '#4', '#5', '#6')
        self.tree = ttk.Treeview(self.bottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='year')
        self.tree.column("#1", minwidth=0, width=80)
        self.tree.heading('#2', text='co2')
        self.tree.column("#2", minwidth=0, width=80)
        self.tree.heading('#3', text='coal_co2')
        self.tree.column("#3", minwidth=0, width=80)
        self.tree.heading('#4', text='gas_co2')
        self.tree.column("#4", minwidth=0, width=80)
        self.tree.heading('#5', text='oil_co2')
        self.tree.column("#5", minwidth=0, width=80)
        self.tree.heading('#6', text='trade_co2')
        self.tree.column("#6", minwidth=0, width=80)

        self.tree.pack(side=tk.LEFT)

        for i in range(self.selectdata['country'].size):
            self.tree.insert('', tk.END, values=[self.selectdata.iloc[i, 1], self.selectdata.iloc[i, 2], self.selectdata.iloc[i, 3],self.selectdata.iloc[i, 4], self.selectdata.iloc[i, 5], self.selectdata.iloc[i, 6]], tags=self.selectdata.index[i])

        # add scrollbat ontreeview
        scrollbar = ttk.Scrollbar(self.bottomFrame, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)


    def menu_setting_click(self):
        pass


    def update_treeview(self, event):
        combobox = event.widget
        selected_index = combobox.current()
        selected_country = self.combobox_values[selected_index]
        #self.filterWrose3 = datasource.filterWrose3(self.combobox_values,filterWrose_numbers)

        if selected_country != '請選擇國家別vvv':
            filtered_data = self.selectdata[self.selectdata['country'] == selected_country]
            self.tree.delete(*self.tree.get_children())
            for i in range(filtered_data.shape[0]):
                self.tree.insert('', tk.END, values=[filtered_data.iloc[i, 1], filtered_data.iloc[i, 2], filtered_data.iloc[i, 3], filtered_data.iloc[i, 4], filtered_data.iloc[i, 5], filtered_data.iloc[i, 6]], tags=filtered_data.index[i])

    def show_line_chart(self):
        selected_country = self.combobox.get()
        if selected_country != '請選擇國家別vvv':
            filtered_data = self.selectdata[self.selectdata['country'] == selected_country]
            years = filtered_data['year']
            co2_values = filtered_data['co2']
            plt.plot(years, co2_values)
            plt.xlabel('Year')
            plt.ylabel('CO2 Emissions')
            plt.title(f'CO2 Emissions in {selected_country}')
            plt.show()


    def create_widgets(self):
        # Create the plot button
        self.plot_button = ttk.Button(self.combobox_frame, text="查看線圖", command=self.show_line_chart)
        self.plot_button.pack(side=tk.RIGHT, padx=10)

    def run(self):
        self.title("Co2 Data")
        self.geometry("700x600")
        self.create_widgets()
        self.mainloop()


if __name__ == '__main__':
    window = MyWindow()
    window.run()
