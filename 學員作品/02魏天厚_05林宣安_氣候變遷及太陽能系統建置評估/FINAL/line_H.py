import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 讀取數據
file_path = os.path.join('processed_data_v2_with_daily_averages.csv')
data = pd.read_csv(file_path)

# 定義字體屬性
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 函數來可視化每個地區的年平均日照時數
def visualize_all_regions_sunshine_hours():
    regions = data['行政區'].unique()
    
    plt.figure(figsize=(15, 10))
    
    for region in regions:
        filtered_data = data[data['行政區'] == region]
        plt.plot(filtered_data['Year'], filtered_data['平均每日日照時數'], marker='o', linestyle='-', label=region)
    
    plt.title('Annual Average Daily Sunshine Hours for All Regions', fontproperties=font_properties)
    plt.xlabel('Year', fontproperties=font_properties)
    plt.ylabel('Average Daily Sunshine Hours (hours)', fontproperties=font_properties)
    plt.legend(prop=font_properties, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    
    output_path = os.path.join('line_H.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.show()

# 可視化所有地區的年平均日照時數
visualize_all_regions_sunshine_hours()
