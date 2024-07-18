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

# Load the data
file_path = '/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/World Happiness Report_new.csv'

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
    print(data.head())
else:
    print(f"File not found: {file_path}")

# Create the main Tkinter window
root = tk.Tk()
root.title("The Happiness Project")

# Title label
titleFrame = ttk.Frame(root)
title_label = ttk.Label(root, text="WHAT Makes You Happy?", justify="center", font=("Helvetica", 20))
title_label.pack(pady=20)
titleFrame.pack(padx=100, pady=(0, 10))

# Insert and resize the PNG image
img_path = "/Users/jesshuang/Documents/GitHub/jess_project/the_happiness_project/img.png"
image = Image.open(img_path)
image = image.resize((140, 140))
photo = ImageTk.PhotoImage(image)

img_label = tk.Label(root, image=photo)
img_label.pack(pady=5)

# Subtitle label
titleFrame = ttk.Frame(root)
title_label = ttk.Label(root, text="See What The World Thinks", font=("Helvetica", 20))
title_label.pack(pady=20)
titleFrame.pack(padx=100, pady=(0, 10))

# Plot frame
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True, pady=5)

# Create a dictionary for column alternatives
column_alternatives = {
    'Life Ladder': "Overall Happiness",
    'Log GDP Per Capita': "Economic Strength",
    'Social Support': "Support Systems",
    'Healthy Life Expectancy At Birth': "Health Expectancy",
    'Freedom To Make Life Choices': "Personal Freedom",
    'Generosity': "Generosity Levels",
    'Perceptions Of Corruption': "Corruption Perception",
    'Positive Affect': "Positive Emotions",
    'Negative Affect': "Negative Emotions",
    'Confidence In National Government': "Government Trust"
}

# Reverse dictionary for lookup
alternative_to_column = {v: k for k, v in column_alternatives.items()}

# Create a combobox for selecting columns
selected_column = tk.StringVar()
column_menu = ttk.Combobox(plot_frame, textvariable=selected_column, width=40)

# Set combobox values to the alternative texts
column_menu['values'] = list(column_alternatives.values())
column_menu.set('Take a Guess')
column_menu.pack()

# Create a figure for the plot
fig = Figure(figsize=(6, 6), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

sns.set(style="whitegrid")

# Messages dictionary
messages = {
    'Life Ladder': "Alright 🙂\n\n🇺🇸🇨🇦🇦🇺🇳🇿\nseem the HAPPIEST!\n\nFollowed by Western Europe 🌍 & Latin America & Carribean 🌎",
    'Log GDP Per Capita': "💰\n  MONEY isn't everything!\n\n Though GDP is reportedly #1 factor here for happiness - \n\nLatin America & Carribean here surely shows that you don't need to be the richest to be happy. 🤠",
    'Social Support': "👨‍👩‍👧‍👦\n HUMAN RELATIONSHIPS\n\n Social Support is #3\nfactor for happiness - \n\nInstead of social welfare, it refers to when you feel low, there are people you can trust and turn to 🥹",
    'Healthy Life Expectancy At Birth': "🩺\n  Well yeah. HEALTH matters!\n\n It is #4 important factor for happiness as you don't want to have to worry too much about\nsimply 'surviving'.",
    'Freedom To Make Life Choices': "🤸🏽‍♀️\nFREEDOM\n\nFreedom To Make Life Choices\n is #2 most important\nfactor for your happiness!\n\nYou can see that the bar\nfor freedom is highhhh~ 🌿",
    'Generosity': "❤️‍🩹\nGENEROSITY\nTo gve is to receive!\n\n Though not everyone is capable to do charity, you can see here that for those who do,\nthey seem happy! ☺️",
    'Perceptions Of Corruption': "🤑\nApprently, CORRUPTION is bad!\n\nThough it seems like it's not a very big factor here for one's happiness. 🤠",
    'Positive Affect': "😁\n POSITIVITY\n\nFrequency of feeling positive emotions such as 'contentment', 'excitement', 'joy', etc.\n\nThe results are pretty scattered, relatively affected by different cultural context!",
    'Negative Affect': "😣\n NEGATIVITY\n\nFrequency of feeling negative emotions such as 'anger', 'sadness', 'anxiousness', etc.\n\nThe results are pretty scattered, relatively affected by different cultural context!",
    'Confidence In National Government': "📡\n POLITICS\n\nInterestingly, Confidence In National Government doesn't really reflect on how happy people are."
}

# Update plot function
def update_plot(event):
    alt_selected_col = selected_column.get()
    if alt_selected_col in alternative_to_column:
        selected_col = alternative_to_column[alt_selected_col]
        if selected_col in data.columns:
            ax.clear()  # Clear previous plot
            sns.scatterplot(data=data, x=selected_col, y='Life Ladder', hue='Region', palette='pastel', ax=ax)
            ax.set_title(f'Life Ladder vs {alt_selected_col}')
            ax.set_xlabel(alt_selected_col)
            ax.set_ylabel('Life Ladder')
            ax.legend(loc='upper left', fontsize='8')
            canvas.draw()  # Update canvas

            # Show corresponding message box
            messagebox.showinfo("Happiness Message", messages[selected_col], icon="warning")

# Bind combobox selection event
column_menu.bind("<<ComboboxSelected>>", update_plot)

# Run the Tkinter main loop
root.mainloop()