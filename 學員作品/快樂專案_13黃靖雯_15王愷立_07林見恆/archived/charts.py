import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'
data = pd.read_csv(file_path)

# List of columns to plot against Life Ladder
columns_to_plot = [
    'Log GDP Per Capita', 'Social Support', 'Healthy Life Expectancy At Birth',
    'Freedom To Make Life Choices', 'Generosity', 'Perceptions Of Corruption',
    'Positive Affect', 'Negative Affect', 'Confidence In National Government'
]

# Set the aesthetics for the plots
sns.set(style="whitegrid")

# Create separate scatter plots
for column in columns_to_plot:
    plt.figure(figsize=(6,6), dpi=120)
    sns.scatterplot(data=data, x=column, y='Life Ladder', hue='Region', palette='pastel')
    plt.title(f'Life Ladder vs {column}')
    plt.xlabel(column)
    plt.ylabel('Life Ladder')
    plt.legend(loc='upper left', fontsize='8')
    plt.show()