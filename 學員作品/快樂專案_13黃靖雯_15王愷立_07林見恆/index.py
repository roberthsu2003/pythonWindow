import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageTk

file_path = '/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
    print(data.head())
else:
    print(f"File not found: {file_path}")

root = tk.Tk()
root.title("The Happiness Project 人生快樂專案")

titleFrame = ttk.Frame(root)
title_label = ttk.Label(root, text="The Happiness Project\n什麼使你「快樂」？", justify="center", font=("Helvetica", 20))
title_label.pack(pady=(60,0))
titleFrame.pack(padx=100, pady=(10, 5))

img_path = "/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/img.png"
image = Image.open(img_path)
image = image.resize((140, 140))
photo = ImageTk.PhotoImage(image)

img_label = tk.Label(root, image=photo)
img_label.pack(pady=5)

titleFrame = ttk.Frame(root)
title_label = ttk.Label(root, text="看看世界各地怎麼說", font=("Helvetica", 20))
title_label.pack(pady=20)
titleFrame.pack(padx=100, pady=(0, 10))

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True, pady=5)

column_alternatives = {
    'Life Ladder': "誰最快樂",
    'Log GDP Per Capita': "經濟發展",
    'Social Support': "人際關係",
    'Healthy Life Expectancy At Birth': "健康醫療",
    'Freedom To Make Life Choices': "身心自由",
    'Generosity': "慷慨助人",
    'Perceptions Of Corruption': "社會腐敗",
    'Positive Affect': "正面情緒",
    'Negative Affect': "負面情緒",
    'Confidence In National Government': "政治信心"
}

alternative_to_column = {v: k for k, v in column_alternatives.items()}

selected_column = tk.StringVar()
column_menu = ttk.Combobox(plot_frame, textvariable=selected_column, width=40)

column_menu['values'] = list(column_alternatives.values())
column_menu.set('選擇影響快樂的成因')
column_menu.pack()

fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

sns.set(style="whitegrid")

messages = {
    'Life Ladder': "好吧 🙂\n\n🇺🇸🇨🇦🇦🇺🇳🇿\n美加紐澳地區看起來最快樂！\n\n緊追在後的是西歐 🌍 以及\n拉丁美洲及加勒比海地區 🌎",
    'Log GDP Per Capita': "💰\n  錢不是萬能的\n\n 雖然此數據顯示\nGDP 是 #1 影響快樂的指標 - \n\n拉丁美洲及加勒比海地區證明了\n不用最經濟富裕也能活得快樂！🤠",
    'Social Support': "👨‍👩‍👧‍👦\n 人際關係\n\n 擁有健全的社會人際互助是此數據\n顯示 #3 影響快樂的指標 - \n\n此處並非指「社會福利制度」，而是「當遇到人生中困難挫折，是否有可以信任的人給予支持幫助」🥹",
    'Healthy Life Expectancy At Birth': "🩺\n  沒錯！健康很重要\n\n 肝不好，人生就是黑白的～\n有進步的醫療水平，能預期腳長壽命是此數據顯示 #4 影響快樂的指標！",
    'Freedom To Make Life Choices': "🤸🏽‍♀️\n身心自由\n\n能夠自由決定人生及工作方向是此指標中顯示 #2 重要影響快樂的指標！\n\n可以發現連快樂指數低的地區，嚮往自由的標準也相當高～ 🌿",
    'Generosity': "❤️‍🩹\n慷慨助人\n施比受更有福\n\n儘管不是所有人都有餘力助人，此處資料顯示，能滿足自身需求並有額外能力已捐款或志工方式幫助他人，能有效提升快樂程度。☺️",
    'Perceptions Of Corruption': "🤑\n沒人喜歡腐敗\n\n不過此處資料顯示，社會的腐敗程度並無直接重大影響人民快樂程度！",
    'Positive Affect': "😁\n 正面情緒\n\n感受到正面情緒如：\n「滿足」、「興奮」、「愉悅」的頻率。\n\n此處資料顯示較分散，\n說明人們情緒波動受各國不同文化民情影響，較不適合直接代表快樂程度。",
    'Negative Affect': "😣\n 負面情緒\n\n感受到負面情緒如：\n「沮喪」、「生氣」、「難過」的頻率。\n\n此處資料顯示較分散，\n說明人們情緒波動受各國不同文化民情影響，較不適合直接代表快樂程度。",
    'Confidence In National Government': "📡\n 政治信心\n\n雖然政治議題無所不在，此處資料有趣地顯示，人民對國民政府的信心度並無重大影響其快樂程度。"
}

def update_plot(event):
    alt_selected_col = selected_column.get()
    if alt_selected_col in alternative_to_column:
        selected_col = alternative_to_column[alt_selected_col]
        if selected_col in data.columns:
            ax.clear()
            sns.scatterplot(data=data, x=selected_col, y='Life Ladder', hue='Region', palette='pastel', ax=ax)
            ax.set_title(f'Life Ladder vs {alt_selected_col}')
            ax.set_xlabel(alt_selected_col)
            ax.set_ylabel('Life Ladder')
            ax.legend(loc='upper left', fontsize='8')
            canvas.draw()

            messagebox.showinfo("Happiness Message", messages[selected_col], icon="warning")

column_menu.bind("<<ComboboxSelected>>", update_plot)

root.mainloop()