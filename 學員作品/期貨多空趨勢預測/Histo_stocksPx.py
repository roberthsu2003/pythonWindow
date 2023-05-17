import tkinter as tk
from tkinter import ttk
import csv
from FinMind.data import DataLoader
import pandas as pd
from tkinter import messagebox
import datetime as dt

import twstock
from datetime import datetime
#from RT_stocksPX import get_realtime_stock_info #盤中抓及時股價有點不穩定

# number of stocks to input
number_of_stocks = 10
start_date = '2009-12-01'

class IndicatorFrame(ttk.Frame):
    def __init__(self, master,**kwargs): 
        super().__init__(master, **kwargs)
        global number_of_stocks, start_date
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default') 

        ttkStyle.configure('back.TFrame',background="#52595D")
        ttkStyle.configure('stockLabel.TLabel',font=('Helvetica', 11,'bold'),foreground='#AFDCEC',background="#52595D")
        ttkStyle.configure('nameLabel.TLabel',font=('Helvetica', 9,'bold'),foreground='#AFDCEC',background="#52595D")
        
# mainFrame
        mainFrame = ttk.Frame(self,padding=(20),style='back.TFrame')        
        mainFrame.pack(expand=True,fill=tk.BOTH)
        
# Create the labels and entry boxes for each stock input
        stocks = []
        weights = []
        name_labels = []
        for i in range(number_of_stocks):
            stock_label = ttk.Label(mainFrame, text=f"Stock {i+1}", style='stockLabel.TLabel')
            stock_label.grid(row=i, column=0, padx=(0, 5), sticky=tk.W)
            self.stock_entry = ttk.Entry(mainFrame, width=10, justify='center')
            self.stock_entry.grid(row=i, column=1)

            name_label = ttk.Label(mainFrame, width=17, text="請輸入正確股票代號", style='nameLabel.TLabel', anchor='center')
            name_label.grid(row=i, column=2, padx=(0))
            name_labels.append(name_label)

            weight_label = ttk.Label(mainFrame, text="~ weight", style='stockLabel.TLabel', font=('Helvetica', 9))
            weight_label.grid(row=i, column=3, padx=(10))

            self.weight_entry = ttk.Entry(mainFrame, width=5, justify='center')
            self.weight_entry.insert(0, "1")
            self.weight_entry.grid(row=i, column=4)

            stocks.append(self.stock_entry)
            weights.append(self.weight_entry)
        
        self.stocks = stocks
        self.weights = weights
        self.name_labels = name_labels

        self.update_name_label() # update_name events here
        self.bind_events()  # bind events here
        
#自動出現股票名稱        
    def update_name_label(self, event=None):
        with open('codeSearch.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader) # skip the header row
            stock_data = {row[2]: row[3] for row in reader}

        # update the name_label widgets with the stock names
            for j, entry in enumerate(self.stocks):
                self.stock_code = entry.get().strip()
                if self.stock_code in stock_data:
                    self.name_labels[j]['text'] = stock_data[self.stock_code]
                else:
                    self.name_labels[j]['text'] = "請輸入正確股票代號"
    def move_focus(self, event):
        widget = event.widget
        idx = None
        if widget in self.stocks:
            idx = self.stocks.index(widget)
            if idx < len(self.stocks) - 1:
                next_widget = self.stocks[idx + 1]
            else:
                next_widget = self.weights[0]
        elif widget in self.weights:
            idx = self.weights.index(widget)
            if idx < len(self.weights) - 1:
                next_widget = self.weights[idx + 1]
            else:
                next_widget = self.stocks[0]
        else:
            return
        next_widget.focus()

        #Select the text in the next widget when click enter
        next_widget.selection_range(0, 'end')

    def bind_events(self):
        for stock_entry in self.stocks:
            stock_entry.bind('<FocusOut>', self.update_name_label)
            stock_entry.bind('<Return>', self.move_focus)
        for weight_entry in self.weights:
            weight_entry.bind('<FocusOut>', self.update_name_label)
            weight_entry.bind('<Return>', self.move_focus)

    def clear_entries(self):
        for stock_entry, weight_entry in zip(self.stocks, self.weights):
            stock_entry.delete(0, tk.END)
            weight_entry.delete(0, tk.END)
            weight_entry.insert(0, "1") # set weight back to default 1
        self.update_name_label()
        
    def update_histo_stockPx(self):
        dl = DataLoader()
        stock_data = pd.DataFrame()
        stock_ids = []
        weights = []
        for stock_entry, weight_entry in zip(self.stocks, self.weights):
            stock_code = stock_entry.get().strip()
            if stock_code:
                stock_ids.append(stock_code)
                data = dl.taiwan_stock_daily(stock_id=stock_code, start_date=start_date) #FinMind function

                #檢查股票代號是否正確
                if data is None or data.empty:
                    messagebox.showerror("Error", f"請輸入正確股票代號\n可利用上方的'查詢股票代號'\nInvalid stock code: {stock_code}")
                    return False # Return False if there was an error
                
                #檢查權重是否為有效的數字
                try:
                    weight = float(weight_entry.get())
                    if weight <= 0:
                        #raise ValueError
                        messagebox.showerror("Error", f"股票權重weight需為正整數\nInvalid weight for stock code: {stock_code}")
                        return False
                except ValueError:
                    messagebox.showerror("Error", f"請輸入有效的股票權重weight\nInvalid weight for stock code: {stock_code}")
                    return False
                
                weights.append(float(weight_entry.get()))
                
                if {'date', 'stock_id', 'close'}.issubset(data.columns):
                        data = data.loc[:, ['date', 'stock_id', 'close']] # only download three columns
                        stock_data = pd.concat([stock_data, data])
                        
                else:
                    print(f"Missing columns in stock data for {stock_code}: {data.columns}")

        if stock_data.empty:
            messagebox.showerror("Error", f"股票代號不可為空白\n可利用上方的'查詢股票代號")
            return False  # Return False if there was an error

        stock_data = stock_data.drop_duplicates(subset=['date', 'stock_id']) # remove any duplicate values
        stock_data['date'] = pd.to_datetime(stock_data['date']) # convert date column to datetime
        stock_data = stock_data.pivot(index='date', columns='stock_id', values='close')

        # Multiply each stock price by its weight
        for stock_id, weight in zip(stock_ids, weights):
            stock_data[stock_id] = stock_data[stock_id] * weight

        # Calculate the portfolio value for each day
        stock_data['portfolio_value'] = stock_data.sum(axis=1)

        # sort the dataframe by index in descending order
        stock_data = stock_data.sort_index(ascending=False)

        #======加這兩行 CHECK NULL and 0 =======
        # drop rows with null values for all columns
        stock_data = stock_data.dropna(how='any', axis=0)
        # drop rows with 0 values for all columns
        stock_data = stock_data[(stock_data!= 0).all(axis=1)]
        
        stock_data.to_csv('Histo_stocksPx.csv', index=True)

#=========== #FF0000 增 加 即 時 股 價 #FF0000 =======================
# Call the get_realtime_stock_info() function with the list of stock codes
        stock_codes = [stock_entry.get().strip() for stock_entry in self.stocks if stock_entry.get().strip()] # => a list of [stock codes]
        #stock_RT_df = get_realtime_stock_info(stock_codes) 
        
        # Create an empty dataframe to store the results
        newstock_RT_df = pd.DataFrame()

        # Iterate over the stock codes and fetch real-time data for each stock code
        for code in stock_codes:
            # Fetch real-time data for the stock code
            stock = twstock.realtime.get(code) #twstock

            # Check if the data is real-time or not
            if stock['success']:
                # Extract the required data
                latest_trade_price = stock['realtime']['latest_trade_price']

#FF0000#FF0000#FF0000 取得股票最佳買賣價，用來算最新市場價格，以防沒有latest_trade_price #FF0000#FF0000#FF0000
                best_bid_price = float(stock['realtime']['best_bid_price'][0])
                best_ask_price = float(stock['realtime']['best_ask_price'][0])
                
                # 把即時股價的時間改成今天的日期年月日，不要有小時分秒
                time = datetime.strptime(stock['info']['time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

                # Add the extracted data to the newstock_RT_df dataframe
                newstock_RT_df.loc[time, code] = latest_trade_price
                newstock_RT_df.loc[time, f"{code}_best_bid"] = best_bid_price
                newstock_RT_df.loc[time, f"{code}_best_ask"] = best_ask_price

                #newstock_RT_df.index = pd.to_datetime([time])
                newstock_RT_df.index.name = 'date'
            else:
                messagebox.showerror("Error", "無法下載即時資料")
                print(f'Error: Data for stock code {code} is not real-time')

        # Multiply each stock price by its weight
        for index, row in newstock_RT_df.iterrows():
            for RTstock_id, weight in zip(stock_codes, weights):
                try:
                    newstock_RT_df.loc[index, RTstock_id] = float(row[RTstock_id]) * weight
                except ValueError:
                    # If the stock price is a string, use (best_bid + best_ask) * 0.5 as the stock price
                    try:
                        best_bid = row[f"{RTstock_id}_best_bid"]
                        best_ask = row[f"{RTstock_id}_best_ask"]
                        newstock_RT_df.loc[index, RTstock_id] = (float(best_bid) + float(best_ask)) * 0.5 * weight
                    except ValueError:
                        # If best_bid or best_ask is also a string, set a default value or ignore the row with the '-' value
                        messagebox.showerror("Error", "無法下載即時資料")
                        newstock_RT_df.loc[index, RTstock_id]  = 0.0

                # except ValueError:
                #     best_bid = row[f"{RTstock_id}_best_bid"]
                #     best_ask = row[f"{RTstock_id}_best_ask"]
                #     newstock_RT_df.loc[index, RTstock_id] = (float(best_bid) + float(best_ask)) * 0.5 * weight
            
        # Drop the columns with best_bid and best_ask prices from newstock_RT_df
        drop_columns = [f"{code}_best_bid" for code in stock_codes] + [f"{code}_best_ask" for code in stock_codes]
        newstock_RT_df = newstock_RT_df.drop(columns=drop_columns)
# #FF0000#FF0000#FF0000#FF0000#FF0000#FF0000

        # Calculate the portfolio value for each day
        newstock_RT_df['portfolio_value'] = newstock_RT_df.sum(axis=1)

        # convert the index to a DatetimeIndex
        newstock_RT_df.index = pd.to_datetime(newstock_RT_df.index) #這裡的date是index(有的時候是column要確定清楚)

        newstock_RT_df.index = pd.to_datetime(newstock_RT_df.index)

        newstock_RT_df.to_csv('RT_stocksPx.csv')

# 將RT即時股價和歷史股價合併=================
        # read both CSV files into dataframes
        df1 = pd.read_csv('RT_stocksPx.csv')
        df2 = pd.read_csv('Histo_stocksPx.csv')
    
#=============== 以下三行程式碼是重點，缺一不可 ===============
        # Convert the 'date' column of df2 to a DatetimeIndex type
        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        # rename the "Date" column to "date"
        df1 = df1.rename(columns={'Date': 'date'})
#=============== 以上三行程式碼是重點，缺一不可 ===============

        # Concatenate the dataframes vertically and drop any duplicate rows based on the index (date)
        combined_stocks_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()

        # Select only the date and the last column of the combined dataframe
        combined_stocks_df = combined_stocks_df[['date', combined_stocks_df.columns[-1]]]

        # Set the "date" column as the index
        combined_stocks_df = combined_stocks_df.set_index('date')

        # save the combined dataframe to a new CSV file
        combined_stocks_df.to_csv('combined_stocksPx.csv', index=True)

        return True  # Return True if the operation was successful

def main():
    root = tk.Tk()
    root.title("Choose Your Indicators")
    window = IndicatorFrame(root)
    window.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()