import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 設定檔案路徑
file_path = os.path.join('processed_data_v2.csv')
data = pd.read_csv(file_path)

# 設定字體
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 選擇相關的數值列
numerical_cols = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']

# 刪除數值列中有缺失值的行
data_clean = data.dropna(subset=numerical_cols)

# 將數值列轉換為浮點型
data_clean[numerical_cols] = data_clean[numerical_cols].apply(pd.to_numeric, errors='coerce')

# 計算Q1（第25百分位）和Q3（第75百分位）
Q1 = data_clean[numerical_cols].quantile(0.25)
Q3 = data_clean[numerical_cols].quantile(0.75)

# 計算IQR（四分位距）
IQR = Q3 - Q1

# 過濾掉異常值
data_no_outliers = data_clean[~((data_clean[numerical_cols] < (Q1 - 1.5 * IQR)) | (data_clean[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 繪製盒鬚圖
plt.figure(figsize=(12, 8))
data_no_outliers.boxplot(column=numerical_cols)
plt.title('Box Plot of Numerical Columns (without outliers)', fontproperties=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)

# 儲存圖片
output_path = os.path.join('boxplot_no_outliers.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
