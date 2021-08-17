from .window import Window
from .data import getCovid19Data

class Covid19Controller:
    def __init__(self):
        self.covid19Data = getCovid19Data()
        self.window = Window(callback=self.callback,covid19Data=self.covid19Data)
        self.output_view = self.window
        self.output_view.title(" 全球 COVID-19 累積病例數與死亡數 ")
    def run(self):
        self.window.mainloop()

    def callback(self):  # 給視窗執行的回呼
        # 讀取資料
        covid19Lst = getCovid19Data()
        # 建立 資料模型 model
        self.covid19Data = covid19Lst
        # 輸出結果 output_view  更新畫面
        self.output_view.bottomRootFrame.destroy()
        self.output_view.designLabel.destroy()
        self.output_view.createDisplayFrame(self.covid19Data)



