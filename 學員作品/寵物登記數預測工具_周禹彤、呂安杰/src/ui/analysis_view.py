import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from .map_renderer import TaiwanMapRenderer
import threading

class AnalysisView(ttk.Frame):
    """分析視圖類別,負責展示資料分析結果"""
    
    def __init__(self, master, data_manager):
        """
        初始化分析視圖
        
        Args:
            master: 父層視窗
            data_manager: 資料管理器實例
        """
        super().__init__(master)
        self.data_manager = data_manager
        self._update_lock = threading.Lock()
        
        # 設定matplotlib中文字型
        plt.rcParams['font.sans-serif'] = ['PingFang TC', 'Microsoft JhengHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 初始化圖表
        self._setup_chart()
        
        # 初始化UI元件
        self._initialize_ui()
        
        # 設定預設縣市為全臺
        self._current_county = "全臺"
        
        # 立即更新顯示 (不使用after延遲)
        self._update_display()
        
    def _setup_chart(self):
        """設定圖表布局"""
        # 建立主圖表
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.figure.set_tight_layout(True)
        
        # 建立子圖表
        self.gs = self.figure.add_gridspec(2, 2, height_ratios=[1.5, 1])
        self.axes = {
            'trend': self.figure.add_subplot(self.gs[0, :]),  # 趨勢圖
            'rate': self.figure.add_subplot(self.gs[1, 0]),   # 絕育率圖
            'ratio': self.figure.add_subplot(self.gs[1, 1])   # 比率圖
        }
        
    def _initialize_ui(self):
        """初始化使用者介面"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 建立左側面板 (縣市選擇與地圖)
        self._create_left_panel()
        
        # 建立右側面板 (資料表格與圖表)
        self._create_right_panel()
        
        # 綁定事件處理
        self.selected_county.trace('w', lambda *args: self.after(10, self._on_county_selected))
        self.map_renderer.on_county_select = self._on_map_county_selected
        
    def _create_left_panel(self):
        """建立左側面板"""
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky='ns', padx=10)
        
        # 建立縣市選擇器
        selector_frame = ttk.LabelFrame(left_frame, text="選擇縣市", padding=5)
        selector_frame.pack(fill='x', pady=5)
        
        county_frame = ttk.Frame(selector_frame)
        county_frame.pack(fill='x', pady=5)
        
        ttk.Label(county_frame, text="縣市:").pack(side='left')
        
        # 設定預設值為全臺
        self.selected_county = tk.StringVar(value="全臺")
        self.county_cb = ttk.Combobox(
            county_frame,
            textvariable=self.selected_county,
            values=self.data_manager.counties,
            state='readonly',
            width=15
        )
        self.county_cb.pack(side='left', padx=5)
        
        # 選擇第一個項目 (全臺)
        self.county_cb.current(0)
        
        # 建立地圖
        map_frame = ttk.LabelFrame(left_frame, text="台灣地圖", padding=5)
        map_frame.pack(fill='both', expand=True, pady=5)
        
        self.map_renderer = TaiwanMapRenderer(map_frame, self.data_manager)
        self.map_renderer.pack(fill='both', expand=True)
        
    def _create_right_panel(self):
        """建立右側面板"""
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky='nsew', padx=10)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # 建立資料表格
        tree_frame = ttk.LabelFrame(right_frame, text="詳細資料", padding=10)
        tree_frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        # 建立捲軸和表格
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        columns = ('year', 'county', 'registrations', 'deregistrations', 
                  'neutered', 'rate')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=5,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # 設定表格欄位
        headers = ['年份', '縣市', '登記數', '註銷數', '絕育數', '絕育率(%)']
        for col, header in zip(columns, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.pack(fill='x', expand=True)
        
        # 建立圖表框架
        self.chart_frame = ttk.LabelFrame(right_frame, text="圖表分析", padding=10)
        self.chart_frame.grid(row=1, column=0, sticky='nsew', pady=5)
        
        # 建立畫布
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def _on_county_selected(self):
        """處理縣市選擇事件"""
        with self._update_lock:
            selected = self.selected_county.get()
            if selected != self._current_county:
                self._current_county = selected
                self.map_renderer.select_county(selected)
                # 使用 after 方法避免阻塞UI
                self.after(10, self._update_display)
                
    def _on_map_county_selected(self, county):
        """處理地圖上縣市選擇事件"""
        if county != self.selected_county.get():
            self.selected_county.set(county)
            
    def _update_display(self):
        """更新顯示內容"""
        if not self._current_county:
            return
            
        # 使用快取的統計資料
        stats = self.data_manager.get_county_stats(self._current_county)
        if not stats:
            return
            
        # 更新表格
        self.tree.delete(*self.tree.get_children())
        for record in stats.records:
            self.tree.insert('', 'end', values=record)
            
        # 更新圖表
        self._plot_trend_chart(stats)
        self._plot_rate_charts(stats)
        
        # 優化圖表更新
        self.canvas.draw_idle()
        
    def _plot_trend_chart(self, stats):
        """
        繪製登記和註銷趨勢圖
        
        Args:
            stats: 縣市統計資料物件
        """
        ax = self.axes['trend']
        ax.clear()
        
        # 反轉年份順序（從舊到新）
        years = [str(y) for y in reversed(stats.years)]
        registrations = stats.registrations[::-1]
        deregistrations = stats.deregistrations[::-1]
        
        # 繪製趨勢線
        ax.plot(years, registrations, 'bo-', label='登記數', linewidth=2)
        ax.plot(years, deregistrations, 'ro-', label='註銷數', linewidth=2)
        
        # 設定圖表標題和標籤
        title = '全臺寵物登記與註銷趨勢' if stats.county == '全臺' else f'{stats.county} 寵物登記與註銷趨勢'
        ax.set_title(title)
        ax.set_xlabel('年份')
        ax.set_ylabel('數量')
        ax.legend()
        ax.grid(True)
        
        # 調整x軸標籤角度
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
    def _plot_rate_charts(self, stats):
        """
        繪製絕育率相關圖表
        
        Args:
            stats: 縣市統計資料物件
        """
        # 反轉資料順序
        years = [str(y) for y in reversed(stats.years)]
        neutering_rates = stats.neutering_rates[::-1]
        neutered = stats.neutered[::-1]
        registrations = stats.registrations[::-1]
        
        # 繪製絕育率趨勢圖
        ax_rate = self.axes['rate']
        ax_rate.clear()
        ax_rate.plot(years, neutering_rates, 'go-', linewidth=2)
        
        # 設定絕育率圖標題
        title = '全臺絕育率趨勢' if stats.county == '全臺' else f'{stats.county} 絕育率趨勢'
        ax_rate.set_title(title)
        ax_rate.set_xlabel('年份')
        ax_rate.set_ylabel('絕育率 (%)')
        ax_rate.grid(True)
        plt.setp(ax_rate.xaxis.get_majorticklabels(), rotation=45)
        
        # 繪製絕育比率圖
        ax_ratio = self.axes['ratio']
        ax_ratio.clear()
        ratio = np.divide(neutered, registrations) * 100
        ax_ratio.plot(years, ratio, 'mo-', linewidth=2)
        
        # 設定比率圖標題
        title = '全臺絕育數與登記數比率' if stats.county == '全臺' else f'{stats.county} 絕育數與登記數比率'
        ax_ratio.set_title(title)
        ax_ratio.set_xlabel('年份')
        ax_ratio.set_ylabel('比率 (%)')
        ax_ratio.grid(True)
        plt.setp(ax_ratio.xaxis.get_majorticklabels(), rotation=45)
        
    def destroy(self):
        """清理資源"""
        plt.close(self.figure)
        super().destroy()