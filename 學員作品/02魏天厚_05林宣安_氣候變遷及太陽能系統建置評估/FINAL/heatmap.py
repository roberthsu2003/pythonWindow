import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 加載 CSV 文件
file_path = os.path.join('processed_data_v2.csv')
data = pd.read_csv(file_path)

# Convert all relevant columns to float
columns_to_convert = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']
for col in columns_to_convert:
    data[col] = data[col].apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values in the relevant columns
data = data.dropna(subset=columns_to_convert)

# Calculate the correlation matrix
correlation_matrix = data[columns_to_convert].corr()

# Load the custom font
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# Update the font properties for matplotlib
plt.rcParams['font.family'] = font_properties.get_name()

# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)

# Set titles and labels with the custom font
plt.title('Correlation Heatmap of Weather Attributes', fontproperties=font_properties)
plt.xticks(fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)

# save png
output_path = os.path.join('heatmap.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
