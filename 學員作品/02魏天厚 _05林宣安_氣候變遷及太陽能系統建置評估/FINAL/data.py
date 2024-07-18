import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

file_path = os.path.join('processed_data_v2.csv')

# 字體設置
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

df = pd.read_csv(file_path)

# 定義需要計算的欄位
columns_to_analyze = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']

# 初始化統計結果字典
stats_dict = {}
describe_dict = {}

# 計算每個欄位的統計量
for column in columns_to_analyze:
    d = pd.to_numeric(df[column], errors='coerce').dropna()
    stats = {
        '計數': d.count(),
        '最小值': d.min(),
        '最大值': d.max(),
        '最小值索引': d.idxmin(),
        '最大值索引': d.idxmax(),
        '10%分位數': d.quantile(0.1),
        '總和': d.sum(),
        '均值': d.mean(),
        '中位數': d.median(),
        '眾數': d.mode().tolist(),  # 眾數可以有多個值
        '方差': d.var(),
        '標準差': d.std(),
        '偏度': d.skew(),
        '峰度': d.kurt()
    }
    stats_dict[column] = stats
    describe_dict[column] = d.describe().to_dict()

# 將統計數據轉換為 DataFrame
stats_df = pd.DataFrame(stats_dict)
describe_df = pd.DataFrame(describe_dict)

# 創建圖表以顯示統計數據
fig, ax = plt.subplots(figsize=(15, 5))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=stats_df.values, colLabels=stats_df.columns, rowLabels=stats_df.index, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 1.2)
plt.title('統計摘要', fontsize=16, fontproperties=font_properties)

# 設置表格內文字體
for key, cell in table.get_celld().items():
    cell.set_text_props(fontproperties=font_properties)

output_path = os.path.join('data.png')
plt.savefig(output_path, bbox_inches='tight')

# 顯示統計數據圖表
plt.show()
