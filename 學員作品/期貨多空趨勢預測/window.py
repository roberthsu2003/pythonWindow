import tkinter as tk
from tkinter import ttk
from FinMind.data import DataLoader
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk

import Histo_stocksPx
from Histo_futPx import ComboFrame
from Histo_stocksPx import IndicatorFrame
from codeSearch import CodeWindow
from fut_margin import Fut_margin
from info import InfoFrame
from RT_futPx import get_realtime_futures_info

#pyinstaller --onefile --icon=icon.ico window.py

start_date = Histo_stocksPx.start_date
STD_DEV_set = 2.5

class Window(tk.Tk):
        def __init__(self,**kwargs):
                super().__init__(**kwargs)
                global start_date, STD_DEV_set

                #Create a class attribute to hold the plot object:
                self.plot = None 

                ttkStyle = ttk.Style()
                ttkStyle.theme_use('default') 
                
                ttkStyle.configure('back.TFrame',background="#52595D")
                ttkStyle.configure('titleLabel.TLabel',font=('Helvetica', 13,'bold'),foreground='#AFDCEC',background="#52595D")
                ttkStyle.configure('productLabel.TLabel',font=('Helvetica', 11,'bold'),foreground='#AFDCEC',background="#52595D")
                ttkStyle.configure('search.TButton',font=('Helvetica', 9,'bold'),foreground='#52595D',background="#B0CFDE", padding=(5, 0))
                ttkStyle.configure('marginLabel.TLabel',font=('Helvetica', 9,'bold'),foreground='#AFDCEC',background="#52595D")
                ttkStyle.configure('calc.TButton',font=('Helvetica', 11,'bold'),foreground='#52595D',background="#AFDCEC", padding=(0, 0))
                ttkStyle.configure('del.TButton',font=('Helvetica', 10,'bold'),foreground='#AFDCEC',background="#6D7B8D", padding=(2.5, 0))

######## fixLeftFrame =================================================================== 
                fixLeftFrame = ttk.Frame(self,style='back.TFrame',padding=(10))        
                fixLeftFrame.pack(side='left')

#插入圖片============================================================
                # create a frame for the image
                imageFrame = tk.Frame(fixLeftFrame)
                imageFrame.pack(expand=True,fill=tk.BOTH,side=tk.TOP)

                logoImage = Image.open('images/bullbear7.jpg')
                resizeImage = logoImage.resize((612,229),Image.LANCZOS)
                self.logoTkimage = ImageTk.PhotoImage(resizeImage)
                logoLabel = ttk.Label(imageFrame,image=self.logoTkimage)
                logoLabel.pack() # add the label to the imageFrame frame

######## MAINFrame ===================================================================                
                mainFrame = ttk.Frame(fixLeftFrame,style='back.TFrame',padding=(10))        
                mainFrame.pack(expand=True,fill=tk.BOTH,side='left')
                
        #mainFrame# titleFrame 標題 : 台指期多空指標
                titleFrame = ttk.Frame(mainFrame,style='back.TFrame')
                titleFrame.pack(pady=10)
                ttk.Label(titleFrame,text="== 期貨多空指標 ==",style='titleLabel.TLabel').pack()

######## FirstFrame =================================================================================
                firstFrame = ttk.Frame(mainFrame,style='back.TFrame')        
                firstFrame.pack(expand=True,fill=tk.BOTH)
                
        #firstFrame# leftTopFrame : 交易商品 Underlying Product
                ttk.Label(firstFrame,text="交易商品 Underlying Product",style='productLabel.TLabel').pack(side='left',pady=(10),padx=(0,30))

        #firstFrame# right-top futuresFrame : Futures ComboFrame
                self.futuresFrame = ComboFrame(firstFrame,style='back.TFrame')
                self.futuresFrame.pack(pady=(10))
                ttk.Label(self.futuresFrame,style='productLabel.TLabel').pack()
                self.futuresFrame.comboBox.bind('<<ComboboxSelected>>', self.futures_changed)

######## SECFrame =================================================================================
                secFrame = ttk.Frame(mainFrame,style='back.TFrame')        
                secFrame.pack(expand=True,fill=tk.BOTH)

        #secFrame#  
                ttk.Label(secFrame,text='指標商品 Leading Indicators',style='productLabel.TLabel').pack(side='left',pady=(10),padx=(0,30))

        #secFrame# button for codeSearch
                codeSearch_button= ttk.Button(secFrame,text="            查詢股票代號            ", style ='search.TButton',command=self.open_CodeSearch_window)
                codeSearch_button.pack(pady=(10),padx=(5,0))
                
######## ThirdFrame ===========================================================================
                thirdFrame = ttk.Frame(mainFrame,style='back.TFrame')        
                thirdFrame.pack(expand=True,fill=tk.BOTH)

        #thirdFrame# Indicators Frame
                self.indicatorFrame = IndicatorFrame(thirdFrame)
                self.indicatorFrame.pack()

###### 4x1 grid 輸入交易口數=====================================================================
                numContrFrame = ttk.Frame(mainFrame,style='back.TFrame')
                numContrFrame.pack(expand=True,fill=tk.BOTH)

                numContrFrame.columnconfigure(0,weight=1) 
                numContrFrame.columnconfigure(1,weight=1) 
                numContrFrame.columnconfigure(2,weight=1) 
                numContrFrame.columnconfigure(3,weight=1)

        #Entry輸入口數======================================================
                ttk.Label(numContrFrame,text='口數:',style='productLabel.TLabel').grid(column=0,row=0,sticky=tk.E,padx=(50,0),pady=(0,10))

                self.nContracts_entry=ttk.Entry(numContrFrame,width=10, justify='center')
                self.nContracts_entry.grid(column=1,row=0,sticky=tk.W,padx=(6,0),pady=(0,10))
                
        
        #顯示所需保證金======================================================
                ttk.Label(numContrFrame,text='初始保證金:',style='marginLabel.TLabel').grid(column=2,row=0,sticky=tk.W,padx=(30,5),pady=(0,10))

                self.messageText = tk.Text(numContrFrame,height=1,width=15,state=tk.DISABLED,pady=(3))
                self.messageText.configure(font=('Helvetica', 9,'bold'),foreground='#AFDCEC',background="#52595D",padx=10)
                self.messageText.grid(column=3,row=0,pady=(0,10),padx=(0,30))

###### 2x1 grid 計算 & 清除按鈕======================================================
                calcuFrame = ttk.Frame(mainFrame,style='back.TFrame')
                calcuFrame.pack(expand=True,fill=tk.BOTH)
                numContrFrame.columnconfigure(0,weight=1) 
                numContrFrame.columnconfigure(1,weight=1) 
        #清除按鈕
                delbtn = ttk.Button(calcuFrame,text="清除重算",style='del.TButton',command=self.clear)
                delbtn.grid(column=0,row=0, padx=(96,0),pady=(10,0))

        #計算按鈕
                calcbtn = ttk.Button(calcuFrame,text="           開始計算          ",style='calc.TButton',command=self.calculate)
                calcbtn.grid(column=1,row=0,padx=(85,0),pady=(10,0))

                self.fut_margin = Fut_margin()

##### InfoFrame 數據分析 =========================== 
                midFrame = ttk.Frame(fixLeftFrame,style="back.TFrame")
                midFrame.pack(side='right')

                self.infoFrame = InfoFrame(midFrame)
                self.infoFrame.pack() 

##### ChartFrame畫圖 Embed the chart in the main window===========================                
                self.chartFrame = ttk.Frame(self, style='back.TFrame')
                self.chartFrame.pack(expand=True, fill=tk.BOTH,side=tk.TOP)

                # create the second chart frame
                self.chartFrame2 = ttk.Frame(self, style='back.TFrame')
                self.chartFrame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#清除除按鈕功能==========================================================================
        def clear(self):
                self.indicatorFrame.clear_entries()
                self.nContracts_entry.delete(0, tk.END)
                #清除所需保證金
                self.messageText.configure(state=tk.NORMAL)
                self.messageText.delete('1.0', tk.END)
                self.messageText.configure(state=tk.DISABLED)

                self.futuresFrame.comboBox.current(0)

                self.infoFrame.messageText1.configure(state=tk.NORMAL)
                self.infoFrame.messageText1.delete('1.0', tk.END)
                self.infoFrame.messageText1.configure(state=tk.DISABLED)

                self.infoFrame.messageText2.configure(state=tk.NORMAL)
                self.infoFrame.messageText2.delete('1.0', tk.END)
                self.infoFrame.messageText2.configure(state=tk.DISABLED)

                self.infoFrame.messageText3.configure(state=tk.NORMAL)
                self.infoFrame.messageText3.delete('1.0', tk.END)
                self.infoFrame.messageText3.configure(state=tk.DISABLED)

                self.infoFrame.messageText4.configure(state=tk.NORMAL)
                self.infoFrame.messageText4.delete('1.0', tk.END)
                self.infoFrame.messageText4.configure(state=tk.DISABLED)

                self.infoFrame.messageTextTime.configure(state=tk.NORMAL)
                self.infoFrame.messageTextTime.delete('1.0', tk.END)
                self.infoFrame.messageTextTime.configure(state=tk.DISABLED)

                self.infoFrame.messageText5.configure(state=tk.NORMAL)
                self.infoFrame.messageText5.delete('1.0', tk.END)
                self.infoFrame.messageText5.configure(state=tk.DISABLED)

                self.infoFrame.messageText6.configure(state=tk.NORMAL)
                self.infoFrame.messageText6.delete('1.0', tk.END)
                self.infoFrame.messageText6.configure(state=tk.DISABLED)
        #簡化寫法
                # widgets = [self.infoFrame.messageText1, self.infoFrame.messageText2, self.infoFrame.messageText3, self.infoFrame.messageText4]

                # for widget in widgets:
                #         widget.configure(state=tk.NORMAL)
                #         widget.delete('1.0', tk.END)
                #         widget.configure(state=tk.DISABLED)

#計算按鈕功能===========================================================================
        def calculate(self):
                #print(self.futuresFrame.comboBox.current())

                # 如果原本已經有圖--先destroy刪掉在畫新的
                # checks if the object "self" has an attribute named "canvas"
                if hasattr(self, 'canvas'):
                        self.canvas.get_tk_widget().destroy()
                if hasattr(self, 'canvas2'):
                        self.canvas2.get_tk_widget().destroy()

                if self.futuresFrame.comboBox.current() == 0:
                        messagebox.showerror("Error", "請選擇期貨商品")
                        return

                # Call the update_histo_stockPx method to update the stock data
                success = self.indicatorFrame.update_histo_stockPx()
                # Check if the operation was successful
                if not success:
                        # Stop the operation if there was an error
                        return
                
                #檢查口數是否為有效的數字
                numCon=self.nContracts_entry.get()
                if numCon.strip() == '':
                # Empty input is not allowed
                        messagebox.showerror("Error","請輸入口數")
                        return False
                elif not numCon.isdigit() or int(numCon) < 0:
                # Invalid input: show error message and return False
                        messagebox.showerror("Error","口數請輸入正整數")
                        return False
                
                self.combined_csv()
                self.combinedCalc()#要在create_chart2前面，因為chart2參照的csv檔事在combinedCalc裡面算的

                self.create_chart()
                self.create_chart2()
                
                self.calculate_margin()
                self.nContracts_entry.bind('<KeyRelease>', lambda event: self.calculate_margin())

                #Get the value of the margin variable from the def calculate_margin(self)
                margin=self.margin 
                self.start_capital='{:,}'.format(margin*2)#千位數加逗點
                
                #原始所需資金放入messageText2
                self.infoFrame.messageText2.configure(state=tk.NORMAL)
                self.infoFrame.messageText2.delete('1.0', tk.END)
                self.infoFrame.messageText2.insert(tk.END,f'  {self.start_capital}') 
                self.infoFrame.messageText2.configure(state=tk.DISABLED)

                #年平均損益放入messageText3
                self.infoFrame.messageText3.configure(state=tk.NORMAL)
                self.infoFrame.messageText3.delete('1.0', tk.END)
                self.infoFrame.messageText3.insert(tk.END,f'  {self.avg_annual_profit}') 
                self.infoFrame.messageText3.configure(state=tk.DISABLED)

                #年報酬率放入messageText4
                self.infoFrame.messageText4.configure(state=tk.NORMAL)
                self.infoFrame.messageText4.delete('1.0', tk.END)
                self.infoFrame.messageText4.insert(tk.END,f'  {self.annual_return_percentage}') 
                self.infoFrame.messageText4.configure(state=tk.DISABLED)

                #self.update_RT_futPx()
                #最新交易資料接收時間放入messageTextTime
                self.infoFrame.messageTextTime.configure(state=tk.NORMAL)
                self.infoFrame.messageTextTime.delete('1.0', tk.END)
                self.infoFrame.messageTextTime.insert(tk.END,f'  {self.current_time}') 
                self.infoFrame.messageTextTime.configure(state=tk.DISABLED)

                #今日應持有部位放入messageText5
                self.infoFrame.messageText5.configure(state=tk.NORMAL)
                self.infoFrame.messageText5.delete('1.0', tk.END)

                self.infoFrame.messageText5.tag_configure('center', justify='center')  # Add a centered alignment tag
                
                self.infoFrame.messageText5.insert(tk.END,f'{self.currentPosition_msg}','center') 
                self.infoFrame.messageText5.configure(state=tk.DISABLED)

                #昨日應持有部位放入messageText6
                self.infoFrame.messageText6.configure(state=tk.NORMAL)
                self.infoFrame.messageText6.delete('1.0', tk.END)
                self.infoFrame.messageText6.insert(tk.END,f'  {self.yesterdayPosition_msg}') 
                self.infoFrame.messageText6.configure(state=tk.DISABLED)
                
        #secFrame# button FUNCTION for codeSearch======================================
        def open_CodeSearch_window(self):
                search_window = CodeWindow()
                search_window.geometry("+50+50")

        #計算保證金======================================================================
        def calculate_margin(self):
                # Get the selected product from the ComboFrame
                selected_fut = self.futuresFrame.comboBox.get()

                # Get the number of contracts entered by the user
                try:
                        self.num_contracts = int(self.nContracts_entry.get())
                except ValueError:
                        pass

                # Calculate the margin based on the selected product and number of contracts
                if selected_fut == '台指期近月':
                        self.margin =  int(self.fut_margin.TX) * self.num_contracts
                elif selected_fut == '電子期近月':
                        self.margin = int(self.fut_margin.TE) * self.num_contracts
                elif selected_fut == '金融期近月':
                        self.margin = int(self.fut_margin.TF) * self.num_contracts
                else:
                        self.margin = 0

                #所需保證金放入messageText
                self.messageText.configure(state=tk.NORMAL)
                self.messageText.delete('1.0', tk.END)
                self.messageText.insert(tk.END, '{:,}'.format(self.margin))#千位數加逗點 
                self.messageText.configure(state=tk.DISABLED)

#選取不同的期貨商品來計算保證金=====================================================
        def futures_changed(self, event=None):
                if event is not None and event.widget is not None:
                        combobox = event.widget
                        self.selected_value = combobox.get()
                        if self.selected_value == '台指期近月':
                                self.futures_ids = ['TX']
                        elif self.selected_value == '電子期近月':
                                self.futures_ids = ['TE']
                        elif self.selected_value == '金融期近月':
                                self.futures_ids = ['TF']
                        else:
                                self.futures_ids = []
                        self.update_histo_futPx(self.futures_ids) ##FF0000 歷史期貨價格

                #========= 增加期貨即時行情 =========
                        selected_fut_value = self.futuresFrame.comboBox.get()
                        if selected_fut_value == '台指期近月':
                                self.fut_id = 'TXF'
                        elif selected_fut_value == '電子期近月':
                                self.fut_id = 'EXF'
                        elif selected_fut_value == '金融期近月':
                                self.fut_id = 'FXF'
                        else:
                                self.fut_id = ""
                        self.update_RT_futPx(self.fut_id) ##FF0000 即時期貨價格
                        
#存取期貨歷史價格至csv檔案========================================================
        def update_histo_futPx(self, futures_ids):
                dl = DataLoader()
                futures_data = pd.DataFrame()
                for future_id in futures_ids:
                        future_data = dl.taiwan_futures_daily(futures_id=future_id, start_date=start_date) #FinMind function (data source for Taiwan Futures Exchange (TAIFEX))

                future_data = future_data[(future_data.trading_session == "position")]
                future_data = future_data[(future_data.settlement_price > 0)]
                future_data = future_data[future_data['contract_date'] == future_data.groupby('date')['contract_date'].transform('min')]

                selected_data = future_data.loc[:, ['date', 'futures_id', 'close']] # select only three columns

                futures_data = pd.concat([futures_data, selected_data]) # concatenate to the existing DataFrame
                        
                #settin "date" column as index, "futures_id" column as columns, and "close" column as values.
                futures_data = futures_data.pivot(index='date', columns='futures_id', values='close')

                # sort the dataframe by index in descending order
                futures_data = futures_data.sort_index(ascending=False)

                #======加這兩行 CHECK NULL and 0 =======
                # drop rows with null values for all columns
                futures_data = futures_data.dropna(how='any', axis=0)
                # drop rows with 0 values for all columns
                futures_data = futures_data[(futures_data!= 0).all(axis=1)]

                futures_data.to_csv('Histo_futPx.csv', index=True)

                return True ## Return True if the operation was successful

#將即時期貨價格和歷史期貨價格合併並輸出成csv 
        def update_RT_futPx(self,fut_id): #FF0000
                futures_RT_df, self.current_time = get_realtime_futures_info(fut_id)
                
                #把下載的資料另存成csv檔
                futures_RT_df.to_csv('RT_futPx.csv')

                # read both CSV files into dataframes
                df1 = pd.read_csv('RT_futPx.csv')
                df2 = pd.read_csv('Histo_futPx.csv')

#=============== 以下兩行程式碼是重點，缺一不可 ===============
        # Convert the 'date' column of df2 to a DatetimeIndex type
                df1['date'] = pd.to_datetime(df1['date'])
                df2['date'] = pd.to_datetime(df2['date'])

                # Concatenate the dataframes vertically and drop any duplicate rows based on the index (date)
                combined_futures_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()

                combined_futures_df.to_csv('combined_futuresPx.csv', index=False)

                return True ## Return True if the operation was successful

#將期貨和指標股Portfolio合併成一個csv檔======================================
        def combined_csv(self):
                # Load the first CSV file
                df1 = pd.read_csv('combined_futuresPx.csv', index_col='date')

                # Load the second CSV file
                df2 = pd.read_csv('combined_stocksPx.csv', index_col='date')

                #======加這行 Drop 重複值======= 
                # Combine the two DataFrames and drop any duplicate rows based on the index (date)
                combined_csv = pd.concat([df1, df2], axis=1).drop_duplicates()

                #======加這行 CHECK NULL======= 
                # Drop rows with any NaN values
                combined_csv = combined_csv.dropna(how='any')

                # sort the dataframe by index in descending order
                #combined_csv = combined_csv.sort_index(ascending=False)

                # Save the combined DataFrame to a new CSV file
                combined_csv.to_csv('combined_FINAL.csv')

        def is_valid_stock_code(self, stock_code):
                # Check if the stock code is valid
                if len(stock_code) != 4:
                        return False
                if not stock_code.isalpha():
                        return False
                return True

#第一章圖 : 折線圖 =============================================
        def create_chart(self):
                df = pd.read_csv('combined_FINAL.csv', header=0, names=['Date', 'Futures', 'Portfolio_value'])

                # 設定中文字型及負號正確顯示
                plt.rcParams['font.family'] = 'Microsoft JhengHei' #微軟正黑體竹

                # Convert the 'Date' column to a datetime object
                df['Date'] = pd.to_datetime(df['Date'])

                # Set the 'Date' column as the index
                df.set_index('Date', inplace=True)

                # Create a figure and two subplots, one for each Y-axis
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                fig.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9)

                # # Create a line chart using the 'Portfolio_value' column on the left Y-axis
                ax1.plot(df['Portfolio_value'], label='Leading Indicators Portfolio', color='#2B547E')
                ax1.set_ylabel('Leading Indicators Portfolio', fontsize =10)

                # Create another line chart using the 'Futures' column on the right Y-axis
                ax2.plot(df['Futures'], label='Underlying Futures', color='#B22222')
                ax2.set_ylabel('Underlying Futures', fontsize =10)

                # Set the chart title and axis labels
                plt.title('Leading Indicators Portfolio and Underlying Futures 價格走勢', fontsize =10)
                ax1.set_xlabel('Year', fontsize =10)

                # Show the legend for both lines
                lines, labels = ax1.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax2.legend(lines + lines2, labels + labels2, loc='best', fontsize =10)

                # Set the font size and rotation angle of the tick labels on the x and y axes
                ax1.tick_params(axis='x', labelsize=8, rotation=45)
                ax1.tick_params(axis='y', labelsize=8)
                ax2.tick_params(axis='y', labelsize=8)

                # Set the background color of the chart
                fig.patch.set_facecolor('#BCC6CC') #change the bg color of the area outside the plot area
                ax1.set_facecolor('#52595D') #change the bg color of  the chart

                # Set the size of the figure
                fig.set_size_inches(6, 3)

                # Adjust the spacing between subplots to minimize the overlaps
                fig.tight_layout()

                self.plot, = ax1.plot(df.index, df['Portfolio_value'], label='Leading Indicators Portfolio')

                # Create a canvas to display the chart
                self.canvas = FigureCanvasTkAgg(fig, master=self.chartFrame)
                self.canvas.draw()

                # Pack the canvas in the chart frame and display it
                self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#第二章圖 : 直條圖 ===========================================
        def create_chart2(self):
                # Read the CSV file and set the 'date' column as the index column
                df = pd.read_csv('yearly_profit.csv', index_col='date')

                # 設定中文字型及負號正確顯示
                plt.rcParams['font.family'] = 'Microsoft JhengHei' #微軟正黑體竹

                # Create a new column of colors based on the values in the 'net_profit' column
                df['color'] = df['net_profit'].apply(lambda x: '#B22222' if x < 0 else '#2B547E')

                # Create a bar chart of the data, negative in red
                fig, ax = plt.subplots()
                ax.bar(df.index, df['net_profit'], color=df['color'])

                plt.title('Annual Net Profit and Loss 年損益$', fontsize =10)
                ax.set_xlabel('Year')
                ax.set_ylabel('Net P&L in $TWD')

                # Set the background color of the chart
                fig.patch.set_facecolor('#BCC6CC') #change the bg color of the area outside the plot area
                ax.set_facecolor('#797979') #change the bg color of  the chart

                # Set the size of the figure
                fig.set_size_inches(6, 3)

                # Set the y-axis tick labels to display numbers with commas
                ax.ticklabel_format(style='plain', axis='y')
                ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Set the font size and rotation angle of the tick labels on the x and y axes
                ax.tick_params(axis='x', labelsize=8, rotation=45)
                ax.tick_params(axis='y', labelsize=8)

                # Adjust the spacing between subplots to minimize the overlaps
                fig.tight_layout()

                # Create a canvas to display the chart
                self.canvas2 = FigureCanvasTkAgg(fig, master=self.chartFrame2)
                self.canvas2.draw()

                # Pack the canvas in the chart frame and display it
                self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def adjust_position(self, position, n_contracts):
                n_contracts = float(n_contracts)
                if position < 0:
                        return max(-n_contracts, position)
                else:
                        return min(n_contracts, position)

        def combinedCalc(self):
                # read the csv file
                df = pd.read_csv('combined_FINAL.csv', index_col='date')

                # sort the dataframe by index in descending order
                df = df.sort_index(ascending=False)

                # Get the selected product from the ComboFrame
                fut_select = self.futuresFrame.comboBox.get()

                # Calculate the margin based on the selected product and number of contracts
                #用字典來簡化多個if
                fut_map = {
                        '台指期近月': 'TX',
                        '電子期近月': 'TE',
                        '金融期近月': 'TF',
                        }
                self.fut = fut_map.get(fut_select, 'wrong fut')

                periods = [1, 3, 5, 10, 20]

                for period in periods:
                        col_name = f'{self.fut}_{period}d'
                        df[col_name] = 100 * (df[f'{self.fut}'] - df[f'{self.fut}'].shift(-period)) / df[f'{self.fut}'].shift(-period)

                for P_period in periods:
                        col_name = f'Portf_{P_period}d'
                        df[col_name] = 100 * (df['portfolio_value'] - df['portfolio_value'].shift(-P_period)) / df['portfolio_value'].shift(-P_period)

                df = df.dropna()  # remove any rows with missing values
                corr_coef = df[f'{self.fut}_1d'].corr(df['Portf_1d'])

        #相關係數放入messageText1
                self.infoFrame.messageText1.configure(state=tk.NORMAL)
                self.infoFrame.messageText1.delete('1.0', tk.END)
                self.infoFrame.messageText1.insert(tk.END,f'  {round(corr_coef,2)}')
                self.infoFrame.messageText1.configure(state=tk.DISABLED)

                d_periods = [1, 3, 5, 10, 20]
                for p in d_periods:
                        col_name = f'{p}d_diff'
                        df[col_name] = df[f'Portf_{p}d'] - df[f'{self.fut}_{p}d']

                stdev_dict = {}
                for p_stdev in d_periods:
                        col = df[f'{p_stdev}d_diff']
                        var = col.var()
                        std_dev = var ** 0.5
                        stdev_dict[f'stdev_{p_stdev}d'] = std_dev
                
                for p2 in d_periods:
                        col_name2 = f'{p2}d_diff_std'
                        df[col_name2] = df[f'{p2}d_diff'] / stdev_dict[f'stdev_{p2}d']
                
                df['SUM'] = df[[f'{p2}d_diff_std' for p2 in d_periods]].sum(axis=1)
                var_SUM = df['SUM'].var()
                std_dev_SUM = var_SUM ** 0.5
                df['SUM_stdev']= df['SUM'] / std_dev_SUM
                var_Ss=df['SUM_stdev'].var()
                std_Ss = var_Ss ** 0.5

                df['Position'] = df['SUM_stdev'] / STD_DEV_set * float(self.nContracts_entry.get())
                df['Position_adj'] = df['Position'].apply(self.adjust_position, n_contracts=self.nContracts_entry.get())
                df['Position_adj'] = df['Position_adj'].apply(round).astype(int)

                #期貨每一點的台幣價值
                if fut_select == '台指期近月':
                        fut_tickValue = 200 # 臺股期貨(TX)  指數×臺幣200元
                elif fut_select == '電子期近月':
                        fut_tickValue = 4000 # 電子期貨(TE)  指數×臺幣4000元
                elif fut_select == '金融期近月':
                        fut_tickValue = 1000 # 金融期貨(TF)  指數×臺幣1000元
                else:
                        print("wrong fut")

                df['DailyPL'] = (df['Position_adj'].shift(-1) * df[f'{self.fut}'].shift(-1) * df[f'{self.fut}_1d']) / 100 * fut_tickValue
                df['position_chg'] = df['Position_adj'] - df['Position_adj'].shift(-1)
                df['abs_position_chg'] = abs(df['position_chg'])
                df['transaction_fee'] = df['abs_position_chg'] *50

                df.to_csv('CAL$$$$$$$$.csv')

                df = pd.read_csv('CAL$$$$$$$$.csv', index_col='date', parse_dates=True)

                df.index = pd.to_datetime(df.index)

                yearly_profit = df.resample('Y')['DailyPL'].sum()
                yearly_profit = yearly_profit[1:]  # exclude the first year

                yearly_fee = df.resample('Y')['transaction_fee'].sum()
                yearly_fee = yearly_fee[1:]

                df_profit = pd.DataFrame({'yearly_profit': yearly_profit, 'yearly_fee': yearly_fee})
                df_profit['net_profit'] = df_profit['yearly_profit'] - df_profit['yearly_fee']
                df_profit.index = df_profit.index.year

                df_profit.to_csv('yearly_profit.csv')
                total_net_profit = df_profit['net_profit'].sum()

                today = date.today()
                start_of_year = date(today.year, 1, 1)
                days_passed = (today - start_of_year).days
                percentage_of_CurrentYear = round(days_passed / 365, 2)
                num_years = df_profit.shape[0] -1 + percentage_of_CurrentYear

                avg_net_yr_profit = round(total_net_profit / num_years, 0)
                self.avg_annual_profit = '{:,.0f}'.format(avg_net_yr_profit)#千位數加逗點

                self.calculate_margin() 
                self.annual_return_p = avg_net_yr_profit / (self.margin*2)

                self.annual_return_percentage= '{:.2%}'.format(self.annual_return_p)

                print(f"There are {num_years} yr in yearly_profit.CSV") #{num_years:.2f%}

                indexPosition = df.columns.get_loc('Position_adj')

                self.currentPosition = df.iloc[0, indexPosition]

                if self.currentPosition > 0:
                        self.currentPosition_msg = f"做多{self.currentPosition}口"
                elif self.currentPosition == 0:
                        self.currentPosition_msg = f"無部位"
                else:
                        self.currentPosition_msg = f"放空{abs(self.currentPosition)}口"
                print(self.currentPosition_msg)
                
                self.yesterdayPosition = df.iloc[1, indexPosition]
                if self.yesterdayPosition > 0:
                        self.yesterdayPosition_msg = f"做多{self.yesterdayPosition}口"
                elif self.yesterdayPosition == 0:
                        self.yesterdayPosition_msg = f"無部位"
                else:
                        self.yesterdayPosition_msg = f"放空{abs(self.yesterdayPosition)}口"
                print(self.yesterdayPosition_msg)


def main():
    window = Window()
    window.title("Winning Indicators")
    window.resizable(width=False, height=False)

    image = tk.PhotoImage(file='icon2.png')
    window.iconphoto(False,image)

    window.geometry("+350+50")
    window.mainloop()

if __name__ == "__main__":
    main()