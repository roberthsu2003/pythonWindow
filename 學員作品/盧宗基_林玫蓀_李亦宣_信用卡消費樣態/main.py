import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap import Style
import pandas as pd
import sqlite3
from tkinter.simpledialog import Dialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data


class Window(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title("信用卡消費樣態")
        self.conn = sqlite3.connect("creditcard.db")
        plt.rcParams["font.family"] = "Microsoft JhengHei"
        style = Style("lumen")

        # ------------介面-----------#
        mainFrame = tk.Frame(self, relief=tk.GROOVE, borderwidth=1)
        tk.Label(mainFrame, text="信用卡消費樣態", font=("arial", 20), fg="#333333").pack(
            padx=10, pady=10
        )
        mainFrame.pack(padx=5, pady=10, fill="both")

        # ------------搜尋------------#
        topFrame = ttk.Labelframe(self, text="搜尋")
        # ------Label------#
        self.dataLabel = ttk.Label(topFrame, text="資料類別:").grid(
            row=0, column=0, padx=(1, 0), pady=(20, 10), sticky="w"
        )
        self.yearLabel = ttk.Label(topFrame, text="年份:").grid(
            row=1, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        self.monthLabel = ttk.Label(topFrame, text="月份:").grid(
            row=2, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        self.areaLabel = ttk.Label(topFrame, text="地區:").grid(
            row=3, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        self.industryLabel = ttk.Label(topFrame, text="產業別:").grid(
            row=4, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        # ------StringVar------#
        self.data_var = tk.StringVar()
        self.data_var.set("請選擇資料類型")
        self.data_mapping = {
            "職業類別": "job",
            "年收入": "incom",
            "教育程度類別": "education",
            "性別": "sex",
            "年齡層": "age",
        }
        self.data = ttk.Combobox(
            topFrame,
            textvariable=self.data_var,
            values=["職業類別", "年收入", "教育程度類別", "性別", "年齡層"],
        )
        self.data.grid(row=0, column=1, padx=10, pady=(20, 10))

        self.year_var = tk.StringVar()
        self.year_var.set("請選擇年份")
        self.year = ttk.Combobox(
            topFrame,
            textvariable=self.year_var,
            values=[
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "2020",
                "2021",
                "2022",
                "2023",
            ],
        )
        self.year.grid(row=1, column=1, padx=10, pady=10)

        self.month_var = tk.StringVar()
        self.month_var.set("請選擇月份")
        self.month = ttk.Combobox(
            topFrame,
            textvariable=self.month_var,
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "ALL",
            ],
        )
        self.month.grid(row=2, column=1, padx=10, pady=10)

        self.area_var = tk.StringVar()
        self.area_var.set("請選擇地區")
        self.area = ttk.Combobox(
            topFrame,
            textvariable=self.area_var,
            values=[
                "臺北市",
                "高雄市",
                "新北市",
                "臺中市",
                "臺南市",
                "桃園市",
                "宜蘭縣",
                "新竹縣",
                "苗栗縣",
                "彰化縣",
                "南投縣",
                "雲林縣",
                "嘉義縣",
                "嘉義市",
                "屏東縣",
                "臺東縣",
                "花蓮縣",
                "澎湖縣",
                "基隆市",
                "新竹市",
                "金門縣",
                "連江縣",
                "ALL",
            ],
        )
        self.area.grid(row=3, column=1, padx=10, pady=10)

        self.industry_var = tk.StringVar()
        self.industry_var.set("請選擇產業別")
        self.industry = ttk.Combobox(
            topFrame,
            textvariable=self.industry_var,
            values=["食", "衣", "住", "行", "文教康樂", "百貨", "其他", "ALL"],
        )
        self.industry.grid(row=4, column=1, padx=10, pady=10)

        self.botton = tk.Button(
            topFrame, text="搜尋", state="active", command=self.load_treeview, width=30
        ).grid(row=5, column=0, padx=10, pady=20, columnspan=2)
        topFrame.pack(side=tk.LEFT, padx=(5, 5), pady=(0, 5),fill="y")

        # -------------資料呈現------------#
        middleFrame = ttk.Labelframe(self, text="資料")
        self.treeview = ttk.Treeview(middleFrame, show="headings", height=18)
        self.treeview.grid(row=0, column=0, padx=5, pady=10, sticky="ns")

        # ------scrollbar------#
        scrollBar = ttk.Scrollbar(
            middleFrame, orient="vertical", command=self.treeview.yview
        )
        scrollBar.grid(row=0, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollBar.set)
        middleFrame.pack(padx=(0, 5), pady=(0, 10), fill="x")

        # ------------圖表-------------#
        self.bottomFrame1 = ttk.Labelframe(self, text="圓餅圖")
        self.bottomFrame1.pack(
            side=tk.LEFT, padx=(0, 5), pady=(0, 5), expand=True, fill="both"
        )

        self.bottomFrame2 = ttk.Labelframe(self, text="長條圖")
        self.bottomFrame2.pack(
            side=tk.LEFT, padx=(0, 5), pady=(0, 5), expand=True, fill="both"
        )

        self.bottomFrame3 = ttk.Labelframe(self, text="折線圖")
        self.bottomFrame3.pack(
            side=tk.LEFT, padx=(0, 5), pady=(0, 5), expand=True, fill="both"
        )

        # ------Bind------#
        self.treeview.bind("<ButtonRelease-1>", self.selectedItem)

    # ------------treeview------------#
    def load_treeview(self):
        selected_option = self.data_var.get()
        selected_year = self.year_var.get()
        selected_month = self.month_var.get()
        selected_area = self.area_var.get()
        selected_industry = self.industry_var.get()
        table = self.data_mapping.get(selected_option)

        if table and selected_option and selected_year != "請選擇年份":
            if selected_option == "年齡層":
                sql = f"SELECT 年,月,地區,產業別,年齡層,信用卡交易筆數,信用卡金額 FROM {table} WHERE 年 = '{selected_year}'"
            else:
                sql = f"SELECT * FROM {table} WHERE 年 = '{selected_year}'"

            if selected_month and selected_month != "請選擇月份" and selected_month != "ALL":
                sql += f" AND 月 = '{selected_month}'"

            if selected_area and selected_area != "請選擇地區" and selected_area != "ALL":
                sql += f" AND 地區 = '{selected_area}'"

            if (
                selected_industry
                and selected_industry != "請選擇產業別"
                and selected_industry != "ALL"
            ):
                sql += f" AND 產業別 = '{selected_industry}'"

            data = pd.read_sql_query(sql, self.conn)
            self.display_data(data)

            self.show_line_charts()
            self.show_pie_charts()
            self.show_bar_charts()

    # ------------折線圖------------#
    def show_line_charts(self):
        selected_option = self.data_var.get()
        table = self.data_mapping.get(selected_option)
        conn = sqlite3.connect("creditcard.db")

        fig, ax = plt.subplots(figsize=(5, 3))
        fig.subplots_adjust(bottom=0.1, top=0.9)

        if (
            selected_option == "教育程度類別"
            or selected_option == "職業類別"
            or selected_option == "年收入"
        ):
            sql = f"SELECT 年, {selected_option}, SUM(信用卡金額) AS 信用卡交易總金額 FROM {table} GROUP BY 年, {selected_option}"
            df = pd.read_sql_query(sql, conn)
            pivot_df = df.pivot(
                index="年", columns=f"{selected_option}", values="信用卡交易總金額"
            )
            pivot_df.plot(kind="line", marker="o", linestyle="-", ax=ax)
            ax.set_title(f"各{selected_option}信用卡交易金額趨勢")
            ax.set_ylabel("信用卡交易總金額")
            ax.set_xticks(df["年"])
            ax.legend().set_visible(False)

        elif selected_option == "性別":
            sql_male = """
                SELECT 年, SUM(信用卡金額) AS 信用卡交易總金額
                FROM sex
                WHERE 性別 = '男性'
                GROUP BY 年
            """

            sql_female = """
                SELECT 年, SUM(信用卡金額) AS 信用卡交易總金額
                FROM sex
                WHERE 性別 = '女性'
                GROUP BY 年
            """

            df_male = pd.read_sql_query(sql_male, conn)
            df_female = pd.read_sql_query(sql_female, conn)

            ax.plot(df_male["年"], df_male["信用卡交易總金額"], marker="o", label="男性")
            ax.plot(df_female["年"], df_female["信用卡交易總金額"], marker="o", label="女性")

            ax.set_title("男女信用卡交易金額趨勢")
            ax.set_xlabel("年份")
            ax.set_ylabel("信用卡交易金額")
            ax.set_xticks(df_male["年"])

        elif selected_option == "年齡層":
            sql = """
                WITH ranked_data AS (
                    SELECT
                        年,
                        年齡層,
                        SUM(信用卡金額) AS 信用卡交易總金額,
                        RANK() OVER (PARTITION BY 年 ORDER BY SUM(信用卡金額) DESC) AS rnk
                    FROM
                        age
                    GROUP BY
                        年,
                        年齡層
                )
                SELECT
                    年,
                    年齡層,
                    信用卡交易總金額
                FROM
                    ranked_data
                WHERE
                    rnk <= 8;
            """
            df = pd.read_sql_query(sql, conn)
            pivot_df = df.pivot(
                index="年", columns=f"{selected_option}", values="信用卡交易總金額"
            )
            pivot_df.plot(kind="line", marker="o", linestyle="-", ax=ax)
            ax.set_title(f"各{selected_option}信用卡交易金額趨勢")
            ax.set_ylabel("信用卡交易總金額")
            ax.set_xticks(df["年"])
            ax.legend().set_visible(False)

        # ------create canvas------#
        if not hasattr(self, "canvas_line_chart"):
            self.canvas_line_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame3)
            canvas_widget = self.canvas_line_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)
        else:
            # ------update canvas content------#
            self.canvas_line_chart.get_tk_widget().destroy()
            self.canvas_line_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame3)
            canvas_widget = self.canvas_line_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.canvas_line_chart.draw()

    # ------------圓餅圖------------#
    def show_pie_charts(self):
        selected_option = self.data_var.get()
        table = self.data_mapping.get(selected_option)
        conn = sqlite3.connect("creditcard.db")

        fig, ax = plt.subplots(figsize=(3.85, 3))
        fig.subplots_adjust(bottom=0.1, top=0.9)
        if (
            selected_option == "教育程度類別"
            or selected_option == "職業類別"
            or selected_option == "年收入"
        ):
            if selected_option == "教育程度類別":
                sql = f"SELECT {selected_option}, SUM(信用卡金額) AS 信用卡交易總金額 FROM {table} GROUP BY {selected_option}"
                df = pd.read_sql_query(sql, conn)
                ax.set_title(f"各教育程度信用卡交易金額分布")
                ax.pie(df["信用卡交易總金額"], labels=df[selected_option])
            else:
                if selected_option == "職業類別":
                    sql = """
                        SELECT
                            CASE
                                WHEN 職業類別 = '其他公共行政類' THEN '公共行政'
                                WHEN 職業類別 = '專業及技術服務類' THEN '專業技術'
                                WHEN 職業類別 = '工商及服務類' THEN '工商服務'
                                WHEN 職業類別 = '教育類' THEN '教育'
                                WHEN 職業類別 IN ('軍警人員一', '軍警人員二') THEN '軍警'
                                ELSE 職業類別
                            END AS 職業類別,
                            SUM(信用卡金額) AS 信用卡交易總金額
                        FROM
                            job
                        GROUP BY
                            CASE
                                WHEN 職業類別 = '軍警人員一' THEN '軍警'
                                WHEN 職業類別 = '軍警人員二' THEN '軍警'
                                ELSE 職業類別
                            END;
                        """
                    df = pd.read_sql_query(sql, conn)
                else:
                    sql = f"SELECT {selected_option}, SUM(信用卡金額) AS 信用卡交易總金額 FROM {table} GROUP BY {selected_option}"
                    df = pd.read_sql_query(sql, conn)
                ax.set_title(f"各{selected_option}信用卡交易金額分布")
                ax.pie(
                    df["信用卡交易總金額"],
                    labels=df[selected_option],
                    startangle=10,
                    textprops={
                        "fontsize": 9.5,
                    },
                )

        elif selected_option == "性別":
            sql_male = """
                SELECT SUM(信用卡金額) AS 信用卡交易總金額
                FROM sex
                WHERE 性別 = '男性'
            """

            sql_female = """
                SELECT SUM(信用卡金額) AS 信用卡交易總金額
                FROM sex
                WHERE 性別 = '女性'
            """

            df_male = pd.read_sql_query(sql_male, conn)
            df_female = pd.read_sql_query(sql_female, conn)

            labels = ["男性", "女性"]
            sizes = [df_male["信用卡交易總金額"].values[0], df_female["信用卡交易總金額"].values[0]]
            ax.pie(
                sizes,
                labels=labels,
                startangle=90,
                textprops={"fontsize": 10},
                radius=1.2,
            )
            ax.set_title("男女信用卡交易金額分佈")

        elif selected_option == "年齡層":
            sql = """
                WITH ranked_data AS (
                    SELECT
                        年齡層,
                        SUM(信用卡金額) AS 信用卡交易總金額,
                        RANK() OVER (PARTITION BY 年 ORDER BY SUM(信用卡金額) DESC) AS rnk
                    FROM
                        age
                    GROUP BY
                        年齡層
                )
                SELECT
                    年齡層,
                    信用卡交易總金額
                FROM
                    ranked_data
                WHERE
                    rnk <= 8;
            """
            df = pd.read_sql_query(sql, conn)
            ax.pie(
                df["信用卡交易總金額"],
                labels=df["年齡層"],
                textprops={"fontsize": 10},
            )
            ax.set_title(f"各{selected_option}信用卡交易金額分布")

        # ------create canvas------#
        if not hasattr(self, "canvas_pie_chart"):
            self.canvas_pie_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame1)
            canvas_widget = self.canvas_pie_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)
        # ------update canvas content------#
        else:
            self.canvas_pie_chart.get_tk_widget().destroy()
            self.canvas_pie_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame1)
            canvas_widget = self.canvas_pie_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.canvas_pie_chart.draw()

    # ------------長條圖------------#
    def show_bar_charts(self):
        selected_option = self.data_var.get()
        table = self.data_mapping.get(selected_option)
        conn = sqlite3.connect("creditcard.db")

        fig, ax = plt.subplots(figsize=(5, 3))
        fig.subplots_adjust(bottom=0.1, top=0.9)

        if selected_option != "年齡層":
            sql = f"SELECT 產業別,{selected_option}, SUM(信用卡金額) AS 信用卡交易總金額 FROM {table} GROUP BY 產業別,{selected_option}"
            df = pd.read_sql_query(sql, conn)
            df_pivot = df.pivot(
                index="產業別", columns=f"{selected_option}", values="信用卡交易總金額"
            )
            if selected_option != "性別":
                df_pivot.plot(
                    kind="bar", stacked=True, ax=ax, cmap="viridis", legend=False
                )
            else:
                df_pivot.plot(
                    kind="bar",
                    stacked=True,
                    ax=ax,
                    legend=False,
                    color=["#ff7f0e","#1f77b4"],
                )

        elif selected_option == "年齡層":
            sql = """
                WITH ranked_data AS (
                    SELECT
                        年齡層,
                        產業別,
                        SUM(信用卡金額) AS 信用卡交易總金額,
                        RANK() OVER (PARTITION BY 產業別 ORDER BY SUM(信用卡金額) DESC) AS rnk
                    FROM
                        age
                    GROUP BY
                        年齡層,
                        產業別
                )
                SELECT
                    年齡層,
                    產業別,
                    信用卡交易總金額
                FROM
                    ranked_data
                WHERE
                    rnk <= 8;
            """

            df = pd.read_sql_query(sql, conn)
            df_pivot = df.pivot(
                index="產業別", columns=f"{selected_option}", values="信用卡交易總金額"
            )
            df_pivot.plot(kind="bar", stacked=True, ax=ax, cmap="viridis", legend=False)

        if selected_option == "教育程度類別":
            ax.set_title(f"各教育程度與產業別信用卡交易金額占比", pad=3)
        else:
            ax.set_title(f"各{selected_option}與產業別信用卡交易金額占比", pad=3)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.set_ylabel("信用卡交易總金額")
        ax.tick_params(axis="x", labelsize=10)
        ax.tick_params(axis="y", labelsize=10)

        # ------create canvas------#
        if not hasattr(self, "canvas_bar_chart"):
            self.canvas_bar_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame2)
            canvas_widget = self.canvas_bar_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)
        # ------update canvas content------#
        else:
            self.canvas_bar_chart.get_tk_widget().destroy()
            self.canvas_bar_chart = FigureCanvasTkAgg(fig, master=self.bottomFrame2)
            canvas_widget = self.canvas_bar_chart.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.canvas_bar_chart.draw()

    def selectedItem(self, event):
        selected_item = self.treeview.focus()
        data_dict = self.treeview.item(selected_item)
        data_list = data_dict["values"]
        if data_list:
            #index = self.treeview.index(selected_item)
            ShowDetail(self, self.treeview["columns"], data_list, title="資訊")

    def display_data(self, data):
        self.treeview.delete(*self.treeview.get_children())

        if not data.empty:
            columns = list(data.columns)
            self.treeview["columns"] = columns
            for col in columns:
                self.treeview.heading(col, text=col, anchor="w")
                self.treeview.column(col, anchor="w", width=100)

            data_list = data.values.tolist()
            for values in data_list:
                self.treeview.insert("", "end", values=values)


# ------------Dialog------------#
class ShowDetail(Dialog):
    def __init__(self, parent, columns, data, **kwargs):
        self.columns = columns
        self.data = data
        super().__init__(parent, **kwargs)

    def body(self, master):
        self.geometry("200x260")

        try:
            for col, value in zip(self.columns, self.data):
                dataInfo = tk.Label(master, text=f"{col}:  {value}", font=("Microsoft JhengHei", 10, "bold"))
                dataInfo.pack(pady=(6,1), anchor="nw")
        except Exception as e:
            print(f"Exception in ShowDetail: {e}")
            print("Columns:", self.columns)
            print("Data:", self.data)

    def buttonbox(self):
        box = tk.Frame(self)
        w = tk.Button(box, text="確認", width=10, command=self.ok, default="active")
        w.pack(padx=5, pady=(5, 10))
        self.bind("<Return>", self.ok)

        box.pack()


def main():
    data.csv_to_database()
    def on_closing():
        print("window關閉")
        if hasattr(window, "canvas_line_chart"):
            window.canvas_line_chart.get_tk_widget().destroy()
        if hasattr(window, "canvas_pie_chart"):
            window.canvas_pie_chart.get_tk_widget().destroy()
        if hasattr(window, "canvas_bar_chart"):
            window.canvas_bar_chart.get_tk_widget().destroy()
        plt.close("all")
        window.destroy()

    window = Window()
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(width=False, height=False)
    window.mainloop()


if __name__ == "__main__":
    main()
