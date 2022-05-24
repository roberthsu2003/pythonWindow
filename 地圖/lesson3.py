import tkinter as tk
import tkintermapview as tkmap

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #建立地圖
        map_widget = tkmap.TkinterMapView(self,
                                          width=800,
                                          height=600,
                                          corner_radius=0,
                                          )
        map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        marker_1 = map_widget.set_position(25.038128318756307, 121.56306490172479,marker=True) #台北市位置
        map_widget.set_zoom(13) #設定顯示大小
        marker_1.set_text("台北市中心")

        marker_2 = map_widget.set_marker(25.040978888281742, 121.56049337427295,text ="國父紀念館",command=self.click1) #國父紀念館
        marker_2.data = {'a':15,'b':'紀念館'}

        marker_3 = map_widget.set_marker(25.037249827231033, 121.50009738141222,text ="龍山寺",command=self.click2) #國父紀念館
        marker_3.data = {'a':18,'b':'紀念館'}

    def click1(self,marker):
        print("click1")
        print(marker.__class__)
        print(marker.data)

    def click2(self,marker):
        print("click2")
        print(marker.__class__)
        print(marker.data)

if __name__ == "__main__":
    window = Window()
    window.geometry("800x600")
    window.title("地圖")
    window.mainloop()

