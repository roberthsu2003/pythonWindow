import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from plot_methods import (
    plot_kd_chart, plot_ma_chart, plot_normal_distribution, plot_boxplot, plot_rsi, plot_heatmap,
    plot_scatter_chart, plot_regression_chart, plot_price_chart, plot_decision_tree
)
from datetime import datetime, timedelta

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股價指標圖形整合系統")

        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.single_stock_dict = {
            "TSMC(ADR)": "TSM",
            "TSMC(台股)": "2330.TW",
            "NVIDIA": "NVDA",
            "APPLE": "AAPL"
        }

        self.multi_stock_dict = {
            "TSMC(ADR)": "TSM",
            "NVIDIA": "NVDA",
            "APPLE": "AAPL",
            "TSMC(ADR)xNVIDIA": ["TSM", "NVDA"],
            "TSMC(ADR)xAPPLE": ["TSM", "AAPL"],
            "NVIDIAxTSMC(ADR)": ["NVDA", "TSM"],
            "APPLExTSMC(ADR)": ["AAPL", "TSM"]
        }

        self.single_chart_options = ["KD指標圖", "均價指標圖", "RSI", "常態分佈圖", "盒鬚圖", "熱力圖"]
        self.multi_chart_options = ["散佈圖", "迴歸分析圖", "決策樹圖"]

        self.time_options = ["1佪月", "3個月", "6個月", "1年", "2年"]
        self.multi_time_options = ["1年", "3年", "5年"]

        self.create_widgets()

        # Add a protocol for handling window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Plot initial charts
        self.plot_single_chart()
        self.plot_multi_chart()

    def create_widgets(self):
        # Single Stock Widgets
        stock_label = tk.Label(self.root, text="單一股票 - 選擇股票:")
        stock_label.grid(row=0, column=0)
        self.stock_var = tk.StringVar(value="TSMC(ADR)")
        stock_menu = ttk.Combobox(self.root, textvariable=self.stock_var, values=list(self.single_stock_dict.keys()), state="readonly")
        stock_menu.grid(row=0, column=1)

        time_label = tk.Label(self.root, text="單一股票 - 選擇時間範圍:")
        time_label.grid(row=1, column=0)
        self.time_var = tk.StringVar(value="1年")
        time_menu = ttk.Combobox(self.root, textvariable=self.time_var, values=self.time_options, state="readonly")
        time_menu.grid(row=1, column=1)

        chart_label = tk.Label(self.root, text="單一股票 - 選擇圖形:")
        chart_label.grid(row=2, column=0)
        self.chart_var = tk.StringVar(value="KD指標圖")
        chart_menu = ttk.Combobox(self.root, textvariable=self.chart_var, values=self.single_chart_options, state="readonly")
        chart_menu.grid(row=2, column=1)

        plot_button = tk.Button(self.root, text="執行", command=self.plot_single_chart)
        plot_button.grid(row=3, column=0, columnspan=2)

        # Multi Stock Widgets
        multi_stock_label = tk.Label(self.root, text="多股票 - 選擇股票:")
        multi_stock_label.grid(row=4, column=0)
        self.multi_stock_var = tk.StringVar(value="TSMC(ADR)xNVIDIA")
        multi_stock_menu = ttk.Combobox(self.root, textvariable=self.multi_stock_var, values=list(self.multi_stock_dict.keys()), state="readonly")
        multi_stock_menu.grid(row=4, column=1)

        multi_time_label = tk.Label(self.root, text="多股票 - 選擇時間範圍:")
        multi_time_label.grid(row=5, column=0)
        self.multi_time_var = tk.StringVar(value="1年")
        multi_time_menu = ttk.Combobox(self.root, textvariable=self.multi_time_var, values=self.multi_time_options, state="readonly")
        multi_time_menu.grid(row=5, column=1)

        multi_chart_label = tk.Label(self.root, text="多股票 - 選擇圖形:")
        multi_chart_label.grid(row=6, column=0)
        self.multi_chart_var = tk.StringVar(value="散佈圖")
        multi_chart_menu = ttk.Combobox(self.root, textvariable=self.multi_chart_var, values=self.multi_chart_options, state="readonly")
        multi_chart_menu.grid(row=6, column=1)

        multi_plot_button = tk.Button(self.root, text="執行", command=self.plot_multi_chart)
        multi_plot_button.grid(row=7, column=0, columnspan=2)

    def get_period(self, time_option):
        time_map = {"1個月": 30, "3個月": 90, "6個月": 180, "1年": 365, "2年": 730}
        return time_map.get(time_option, 365)

    def get_multi_period(self, time_option):
        time_map = {"1年": 365, "3年": 1095, "5年": 1825}
        return time_map.get(time_option, 365)

    def plot_single_chart(self):
        stock = self.stock_var.get()
        chart_type = self.chart_var.get()
        time_option = self.time_var.get()
        ticker = self.single_stock_dict.get(stock, None)
        if ticker:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.get_period(time_option))
            try:
                stock_data = yf.download(ticker, start=start_date, end=end_date)
                if stock_data.empty:
                    raise ValueError("無數據")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法獲取股票數據: {e}")
                return

            chart_funcs = {
                "KD指標圖": plot_kd_chart,
                "均價指標圖": plot_ma_chart,
                "RSI": plot_rsi,
                "常態分佈圖": plot_normal_distribution,
                "盒鬚圖": plot_boxplot,
                "熱力圖": plot_heatmap
            }

            plot_func = chart_funcs.get(chart_type, plot_kd_chart)
            plot_func(self, stock_data)

    def plot_multi_chart(self):
        stock = self.multi_stock_var.get()
        chart_type = self.multi_chart_var.get()
        time_option = self.multi_time_var.get()

        tickers = self.multi_stock_dict.get(stock, None)
        if tickers:
            if isinstance(tickers, str):
                tickers = [tickers]
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.get_multi_period(time_option))
            try:
                stock_data = {ticker: yf.download(ticker, start=start_date, end=end_date) for ticker in tickers}

                if any(data.empty for data in stock_data.values()):
                    raise ValueError("無數據")
            except Exception as e:
                messagebox.showerror("錯誤", f"無法獲取股票數據: {e}")
                return

            if isinstance(tickers, list) and len(tickers) == 2:
                chart_funcs = {
                    "散佈圖": plot_scatter_chart,
                    "迴歸分析圖": plot_regression_chart,
                    "決策樹圖": plot_decision_tree
                }

                plot_func = chart_funcs.get(chart_type, plot_scatter_chart)
                plot_func(self, stock_data, tickers)
            else:
                plot_price_chart(self, stock_data, tickers)
        else:
            messagebox.showerror("錯誤", "無效的股票選擇")

    def display_chart(self, fig):
        for widget in self.root.grid_slaves(row=0, column=2):
            widget.grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=8)

    def on_closing(self):
        self.root.quit()  # 使用 quit 而不是 destroy

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
