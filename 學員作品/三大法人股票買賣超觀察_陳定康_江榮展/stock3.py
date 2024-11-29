from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from datetime import datetime, timedelta
import matplotlib.font_manager as fm
import finlab
from finlab import data
import os
os.system('cls')
# 載入環境變數
load_dotenv()
# 使用環境變數
finlab.login(os.getenv('FINLAB_API_KEY'))
# 設定數據存儲路徑
data.set_storage(data.FileStorage(path="D:\\pickle"))
# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 用來正常顯示負號



class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("國內外投信股票買賣查詢系統")
        self.close_price = pd.DataFrame()  # 預設為空 DataFrame
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=365)

        # 左側導航
        self.nav_frame = tk.Frame(root)
        self.nav_frame.pack(side="left", fill="y", padx=10, pady=10)
        tk.Label(self.nav_frame, text="選擇股票").pack(anchor="w")

        self.stock_combobox = ttk.Combobox(self.nav_frame, state="readonly")
        self.stock_combobox.pack(fill="x")
        self.stock_combobox.bind("<<ComboboxSelected>>", self.display_data)

        # 右側顯示區域
        self.display_frame = tk.Frame(root)
        self.display_frame.pack(side="right", fill="both", expand=True)

        # 表格區域
        self.table_frame = tk.Frame(self.display_frame)
        self.table_frame.pack(side="top", fill="x", padx=10, pady=5)

        tk.Label(self.table_frame, text="三大法人買賣超資訊",
                 font=("Arial", 14)).pack(anchor="w")

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.table = ttk.Treeview(self.table_frame, columns=[
                                  "Month", "Foreign", "Investment Trust", "Dealer"], show="headings", yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.table.yview)

        for col, name in zip(["Month", "Foreign", "Investment Trust", "Dealer"], ["月份", "外資買賣超", "投信買賣超", "自營商買賣超"]):
            self.table.heading(col, text=name)
            self.table.column(col, anchor="center" if col ==
                              "Month" else "e", width=150)

        self.table.pack(fill="x", expand=True)

        # 繪圖區域
        self.plot_frame = tk.Frame(self.display_frame)
        self.plot_frame.pack(side="bottom", fill="both", expand=True)

        # 加載數據並初始化
        self.data = self.load_data()

        # 獲取所有股票代碼和名稱
        self.stock_list = self.get_stock_list_from_excel()
        self.stock_combobox['values'] = self.stock_list
        self.input_frame = tk.Frame(self.nav_frame)
        self.input_frame.pack(fill="x", pady=10)
        self.analyze_button = tk.Button(
            self.input_frame,
            text="分析主力買超比例",
            command=self.analyze_institutional_ratio
        )
        self.analyze_button.pack(fill="x", pady=2)

        self.top_stocks_button = tk.Button(
            self.input_frame,
            text="顯示主力買超前15名",
            command=self.show_top_stocks
        )
        self.top_stocks_button.pack(fill="x", pady=2)

        # 新增股票代號輸入框
        tk.Label(self.input_frame, text="輸入股票代號:").pack(anchor="w")
        self.stock_entry = tk.Entry(self.input_frame)
        self.stock_entry.pack(fill="x", pady=2)

        # 新增搜尋按鈕
        self.search_button = tk.Button(
            self.input_frame, text="搜尋", command=self.search_stock)
        self.search_button.pack(fill="x", pady=2)

        # 新增錯誤訊息標籤
        self.error_label = tk.Label(self.input_frame, text="", fg="red")
        self.error_label.pack(fill="x")

# 在 StockApp 類別中新增搜尋函數：


    def search_stock(self):
        """搜尋股票並更新顯示"""
        stock_id = self.stock_entry.get().strip()

        # 檢查是否為空
        if not stock_id:
            self.error_label.config(text="請輸入股票代號")
            return

        # 檢查是否為數字
        if not stock_id.isdigit():
            self.error_label.config(text="請輸入有效的股票代號（純數字）")
            return

        # 在股票清單中搜尋
        matching_stocks = [s for s in self.stock_list if s.startswith(stock_id)]

        if matching_stocks:
            # 找到符合的股票
            self.stock_combobox.set(matching_stocks[0])
            self.error_label.config(text="")
            self.display_data()
        else:
            self.error_label.config(text="找不到此股票代號")

            if self.stock_list:
                self.stock_combobox.set(self.stock_list[0])  # 預設選擇第一個股票

            self.display_data()

    def get_stock_list_from_excel(self):
        """從 Excel 檔案獲取股票清單"""
        try:
            df = pd.read_excel("./data/tw_stock_topics.xlsx")  # 調整路徑至正確位置
            return [f"{row['stock_no']} {row['stock_name']}" for index, row in df.iterrows()]
        except Exception as e:
            print(f"讀取 Excel 檔案時發生錯誤: {e}")
            return []


    def load_data(self):
        """使用 finlab API 載入資料"""
        try:
            # 獲取三大法人買賣超資料
            foreign = data.get(
                'institutional_investors_trading_summary:外陸資買賣超股數(不含外資自營商)')
            foreign_dealer = data.get(
                'institutional_investors_trading_summary:外資自營商買賣超股數')

            if foreign is None or foreign_dealer is None:
                print("無法獲取外資數據")
                foreign = pd.DataFrame()
                foreign_dealer = pd.DataFrame()

            foreign_total = foreign.fillna(0) + foreign_dealer.fillna(0)
            investment_trust = data.get(
                'institutional_investors_trading_summary:投信買賣超股數')
            dealer = data.get(
                'institutional_investors_trading_summary:自營商買賣超股數(自行買賣)')

            # 價格和交易資料
            self.close_price = data.get("price:收盤價")
            if self.close_price is None or self.close_price.empty:
                print("無法獲取收盤價數據")
                self.close_price = pd.DataFrame()

            return {
                "foreign_trading": foreign_total,
                "investment_trust_trading": investment_trust.fillna(0) if investment_trust is not None else pd.DataFrame(),
                "dealer_trading": dealer.fillna(0) if dealer is not None else pd.DataFrame()
            }
        except Exception as e:
            print(f"載入數據時發生錯誤: {e}")
            return {
                "foreign_trading": pd.DataFrame(),
                "investment_trust_trading": pd.DataFrame(),
                "dealer_trading": pd.DataFrame()
            }

    def process_monthly_data(self, stock):
        """處理月度資料"""
        stock_code = stock.split()[0]

        try:
            if (self.data["foreign_trading"].empty or
                self.data["investment_trust_trading"].empty or
                    self.data["dealer_trading"].empty):
                print(f"無法獲取 {stock_code} 的數據")
                return [], pd.DataFrame()

            if (stock_code not in self.data["foreign_trading"].columns or
                stock_code not in self.data["investment_trust_trading"].columns or
                    stock_code not in self.data["dealer_trading"].columns):
                print(f"股票代碼 {stock_code} 不在數據中")
                return [], pd.DataFrame()

            monthly_data = pd.DataFrame({
                "Foreign": self.data["foreign_trading"][stock_code],
                "Investment Trust": self.data["investment_trust_trading"][stock_code],
                "Dealer": self.data["dealer_trading"][stock_code],
            }).fillna(0)

            monthly_data = monthly_data.resample("ME").sum()
            monthly_data = monthly_data.sort_index(ascending=False)
            monthly_data.index = monthly_data.index.strftime("%Y-%m")
            monthly_data = monthly_data.round().astype(int)

            for col in monthly_data.columns:
                monthly_data[col] = monthly_data[col].apply(
                    lambda x: f"{x/1000:,.0f}")

            return monthly_data.reset_index().values.tolist(), monthly_data

        except Exception as e:
            print(f"處理 {stock} 的數據時發生錯誤: {e}")
            return [], pd.DataFrame()

    def plot_data(self, data):
            """ 繪製股票交易趨勢圖 """
            data = data.sort_index()
            stock_name = self.stock_combobox.get()
            stock_code = stock_name.split()[0]

            try:
                if stock_code not in self.close_price.columns:
                    print(f"股票代碼 {stock_code} 不在收盤價數據中")
                    return

                price_data = self.close_price[stock_code].loc[data.index.intersection(
                    self.close_price.index)]

                if price_data.empty:
                    print(f"無法找到 {stock_code} 的價格數據")
                    return

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])

                # 繪製股價走勢
                ax1.plot(data.index, price_data, label="收盤價", color='black', linewidth=2)
                ax1.set_title(f"{stock_name} 股價與三大法人買賣超趨勢", fontsize=16, pad=20)
                ax1.set_ylabel("股價", fontsize=12)
                ax1.grid(True, linestyle='--', alpha=0.7)
                ax1.legend(fontsize=10)

                # 繪製三大法人買賣超
                for col, color, label in zip(
                    ["Foreign", "Investment Trust", "Dealer"], 
                    ['red', 'green', 'blue'], 
                    ['外資', '投信', '自營商']
                ):
                    values = data[col].str.replace(",", "").astype(float)
                    ax2.bar(data.index, values, label=label, alpha=0.7)

                ax2.set_xlabel("月份", fontsize=12)
                ax2.set_ylabel("買賣超張數(張)", fontsize=12)
                ax2.legend(fontsize=10)
                ax2.grid(True, linestyle='--', alpha=0.7)

                for ax in [ax1, ax2]:
                    ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune="both", nbins=12))

                plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
                plt.tight_layout()

                if hasattr(self, 'canvas') and self.canvas:
                    self.canvas.get_tk_widget().destroy()

                self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            except Exception as e:
                print(f"繪製圖表時發生錯誤: {str(e)}")



    def display_data(self, event=None):
        """顯示選定股票的資料"""
        stock = self.stock_combobox.get()
        table_data, plot_data_values = self.process_monthly_data(stock)

        # 更新表格
        for row in self.table.get_children():
            self.table.delete(row)

        for row in table_data:
            self.table.insert("", "end", values=row)

        # 更新圖表
        self.plot_data(plot_data_values)
        
    def analyze_institutional_ratio(self):
        """分析主力買超比例"""
        stock_code = self.stock_combobox.get().split()[0]
        stock_name = self.stock_combobox.get()
        
        try:
            # 獲取成交量數據
            volume = data.get("price:成交股數")
            
            # 獲取最近20個交易日的數據
            end_date = datetime.now()
            latest_data = pd.DataFrame({
                'foreign': self.data['foreign_trading'][stock_code],
                'trust': self.data['investment_trust_trading'][stock_code],
                'dealer': self.data['dealer_trading'][stock_code],
                'volume': volume[stock_code]
            }).tail(20)
            
            # 計算比例
            latest_data['foreign_ratio'] = latest_data['foreign'] / latest_data['volume'] * 100
            latest_data['trust_ratio'] = latest_data['trust'] / latest_data['volume'] * 100
            latest_data['total_ratio'] = (latest_data['foreign'] + latest_data['trust'] + latest_data['dealer']) / latest_data['volume'] * 100
            
            # 創建新視窗顯示圖表
            ratio_window = tk.Toplevel(self.root)
            ratio_window.title(f"{stock_name} 主力買超比例分析")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # 繪製比例圖
            ax.plot(latest_data.index, latest_data['foreign_ratio'], 
                    label='外資買超比例', color='red', linewidth=2)
            ax.plot(latest_data.index, latest_data['trust_ratio'], 
                    label='投信買超比例', color='green', linewidth=2)
            ax.plot(latest_data.index, latest_data['total_ratio'], 
                    label='三大法人買超比例', color='blue', linewidth=2)
            
            ax.set_title(f"{stock_name} 近20日主力買超比例", fontsize=14, pad=20)
            ax.set_xlabel("日期", fontsize=12)
            ax.set_ylabel("買超比例(%)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend(fontsize=10)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=ratio_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            self.error_label.config(text=f"分析時發生錯誤: {str(e)}")


    def show_top_stocks(self):
        """顯示主力買超前15名"""
        try:
            # 計算最近20日三大法人買超總和
            end_date = datetime.now()
            
            # 創建所有股票的買超數據DataFrame
            all_stocks_data = pd.DataFrame()
            
            for stock in self.stock_list:
                stock_code = stock.split()[0]
                try:
                    # 獲取該股票的三大法人買超數據
                    foreign = self.data['foreign_trading'][stock_code].tail(20).sum()
                    trust = self.data['investment_trust_trading'][stock_code].tail(20).sum()
                    dealer = self.data['dealer_trading'][stock_code].tail(20).sum()
                    
                    all_stocks_data.loc[stock, '外資買超'] = foreign
                    all_stocks_data.loc[stock, '投信買超'] = trust
                    all_stocks_data.loc[stock, '自營商買超'] = dealer
                    all_stocks_data.loc[stock, '三大法人買超'] = foreign + trust + dealer
                    
                except Exception:
                    continue
            
            # 排序並獲取前15名
            top_15 = all_stocks_data.nlargest(15, '三大法人買超')
            
            # 創建新視窗顯示結果
            top_window = tk.Toplevel(self.root)
            top_window.title("主力買超前15名")
            top_window.geometry("800x400")  # 設定視窗大小
            
            # 創建標題標籤
            title_label = tk.Label(top_window, 
                                text="近20日主力買超排行榜", 
                                font=("Microsoft JhengHei", 16, "bold"))
            title_label.pack(pady=10)
            
            # 創建表格框架
            tree_frame = ttk.Frame(top_window)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # 創建捲軸
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 創建表格
            tree = ttk.Treeview(tree_frame, columns=[
                "Rank", "Stock", "Foreign", "Trust", "Dealer", "Total"
            ], show="headings", yscrollcommand=scrollbar.set)
            
            # 設置捲軸
            scrollbar.config(command=tree.yview)
            
            # 設置列標題和寬度
            tree.heading("Rank", text="排名")
            tree.heading("Stock", text="股票")
            tree.heading("Foreign", text="外資買超")
            tree.heading("Trust", text="投信買超")
            tree.heading("Dealer", text="自營商買超")
            tree.heading("Total", text="三大法人買超")
            
            tree.column("Rank", width=50, anchor="center")
            tree.column("Stock", width=150, anchor="center")
            tree.column("Foreign", width=100, anchor="center")
            tree.column("Trust", width=100, anchor="center")
            tree.column("Dealer", width=100, anchor="center")
            tree.column("Total", width=100, anchor="center")
            
            # 插入數據
            for rank, (idx, row) in enumerate(top_15.iterrows(), 1):
                tree.insert("", "end", values=(
                    rank,
                    idx,
                    f"{row['外資買超']/1000:,.0f}",
                    f"{row['投信買超']/1000:,.0f}",
                    f"{row['自營商買超']/1000:,.0f}",
                    f"{row['三大法人買超']/1000:,.0f}"
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            # 添加說明標籤
            note_label = tk.Label(top_window, 
                                text="註：買超單位為張", 
                                font=("Microsoft JhengHei", 10))
            note_label.pack(pady=5)
            
        except Exception as e:
            self.error_label.config(text=f"獲取前15名時發生錯誤: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()  # 啟動應用程式主循環

# python stock3.py
