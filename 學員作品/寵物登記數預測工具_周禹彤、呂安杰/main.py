import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from src.ui.analysis_view import AnalysisView
from src.data.data_source import PetDataManager

class MainWindow(ThemedTk):
    """主視窗類別,負責初始化程式介面與資料管理"""
    def __init__(self):
        """初始化主視窗,設定基本屬性與建立元件"""
        super().__init__(theme="arc")  # 使用 arc 佈景主題
        self.title('寵物登記與絕育分析')  # 設定視窗標題
        self.geometry('1300x720')  # 設定視窗大小
        
        # 禁止視窗調整大小
        #self.resizable(False, False)
        
        # 初始化資料管理器,用於處理寵物相關資料
        self.data_manager = PetDataManager()
        
        # 建立主要分析視圖
        self.view = AnalysisView(self, self.data_manager)
        self.view.pack(fill='both', expand=True)
        
        # 註冊視窗關閉事件處理程序
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        """處理視窗關閉事件,確保資源正確釋放"""
        try:
            # 先停止所有更新
            if hasattr(self.view.map_renderer.map_widget, "after_id"):
                self.after_cancel(self.view.map_renderer.map_widget.after_id)
            
            # 清理地圖資源    
            if hasattr(self.view.map_renderer, "map_widget"):
                self.view.map_renderer.clear_markers()
                self.view.map_renderer.map_widget.destroy()
            
            # 關閉視窗
            self.quit()
        finally:
            self.destroy()

def main():
    """程式進入點"""
    app = MainWindow()
    app.mainloop()

if __name__ == '__main__':
    main()