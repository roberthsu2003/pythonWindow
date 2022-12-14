import datasource as ds
from Secrets import api_key
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import io
import urllib.request


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        tk.Label(self, text="地震資訊查詢", font=(
            'Arial', 20)).pack(padx=30, pady=30)

        # 建立存放按鈕的容器
        button_frame = tk.Frame(self)
        button_frame.pack(padx=50, pady=(0, 30))

        self.btn1 = tk.Button(
            button_frame, text="查詢", command=self.button_click, width=10, padx=20, pady=5)
        self.btn1.pack()
        # print(id(self.btn1))

        # self.btn2 = tk.Button(
        #     button_frame, text="在事件雙擊左鍵，再點擊開啟圖片", width=30, padx=20, pady=5)
        # self.btn2.pack(side="bottom", pady=5)
        # self.btn2.bind("<Button-1>", self.create_img)

        self.displayImage = tk.Frame(self)
        self.displayImage.pack()

    def create_img(self, event):
        print(hasattr(self, 'canvas'))
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        # try:
        #     image
        # except Exception:
        #     showinfo("警告", "尚未點擊資訊")

        self.canvas = tk.Canvas(self, width=600, height=450)
        self.canvas.create_image(
            0, 0, anchor="nw", image=image)   # 在 Canvas 中放入圖片
        self.canvas.pack(side="bottom")

 # 實體的方法

    def button_click(self):

        try:
            earthquake_report = ds.get_report_data(api_key)

        except Exception as e:
            # 出現錯誤訊息
            showinfo(message=e)
            return
        if hasattr(self, 'btn1'):
            print(id(self.btn1))
            self.btn1.destroy()

        self.displayFrame = DisplayFrame(
            self, data=earthquake_report, text="地震", borderwidth=2, relief=tk.GROOVE)
        self.displayFrame.pack(fill=tk.BOTH, padx=50)


class DisplayFrame(ttk.LabelFrame):
    def __init__(self, parent, data=None, **kwargs):  # **kwargs打包變成dict
        super().__init__(parent, **kwargs)
        self.window = parent
        self.earthquake_data = data

        centerData = self.earthquake_data  # [column_rows:column_rows*2]

        centerFrame = CustomFrame(
            self.window, width=200, data=centerData, height=200)
        centerFrame.pack(side=tk.BOTTOM, padx=10)


class CustomFrame(tk.Frame):
    def __init__(self, parent, data=None, **kwarge):
        super().__init__(parent, **kwarge)  # **進來是打包，**出去是解壓縮
        self.window = parent
        self.list_data = data
        self.tree = ttk.Treeview(
            self, columns=["#1", "#2", "#3",], show="headings", height=10)
        self.tree.pack(side=tk.LEFT)

        scrollbar1 = tk.Scrollbar(self)
        scrollbar1.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=self.tree.yview)

        # scrollbar2 = tk.Scrollbar(self, orient="horizontal")
        # scrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        # self.tree.config(xscrollcommand=scrollbar2.set)
        # scrollbar2.config(command=self.tree.xview)

        self.tree.heading("#1", text="事件")
        self.tree.heading("#2", text="資訊網址")
        self.tree.heading("#3", text="資訊圖片")

        self.tree.column("#1", width=300, anchor="center")
        self.tree.column("#2", width=300, anchor="center")
        self.tree.column("#3", width=300, anchor="center")

        for item in self.list_data:
            self.tree.insert('', tk.END, values=item)

        self.tree.bind("<<TreeviewSelect>>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        # print(self.window)
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            self.img_url = item['values'][2]

        with urllib.request.urlopen(self.img_url) as connection:
            raw_data = connection.read()
        im = Image.open(io.BytesIO(raw_data))
        im_resize = im.resize((600, 450))
        self.image = ImageTk.PhotoImage(im_resize)
        if hasattr(self, 'canvas'):
            self.canvas.destroy()

        self.canvas = tk.Canvas(
            self.window.displayImage, width=600, height=450)
        self.canvas.create_image(
            0, 0, anchor="nw", image=self.image)   # 在 Canvas 中放入圖片
        self.canvas.pack(side="bottom")


def main():

    window = Window()
    window.title("地震結果查詢")
    window.mainloop()


if __name__ == "__main__":
    main()
