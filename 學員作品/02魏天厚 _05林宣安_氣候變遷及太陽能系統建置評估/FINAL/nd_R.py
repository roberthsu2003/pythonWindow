import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import os

# 讀取數據
file_path = os.path.join('processed_data_v2_with_daily_averages.csv')
data = pd.read_csv(file_path)

# 定義字體屬性
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 清理 '總日射量MJ/ m2' 列，移除非數字字符
data['總日射量MJ/ m2'] = pd.to_numeric(data['總日射量MJ/ m2'], errors='coerce')

# 移除 NaN 值
data_filtered = data['總日射量MJ/ m2'].dropna()

# 計算IQR並移除異常值
Q1 = data_filtered.quantile(0.25)
Q3 = data_filtered.quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

data_no_outliers = data_filtered[(data_filtered >= lower_bound) & (data_filtered <= upper_bound)]

# 繪製常態分佈圖並存為PNG文件
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data_no_outliers, 30, density=True, alpha=0.6, color='g', edgecolor='black')

mu, sigma = data_no_outliers.mean(), data_no_outliers.std()
best_fit_line = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
                 np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
plt.plot(bins, best_fit_line, '--', color='red')

plt.xlabel('總日射量MJ/ m2', fontproperties=font_properties)
plt.ylabel('頻率', fontproperties=font_properties)
plt.title('去除異常值後的總日射量常態分佈圖', fontproperties=font_properties)

plt.grid(True)
output_path = os.path.join('normaldistribution_R.png')
plt.savefig(output_path, bbox_inches='tight')
plt.show()
