## Matplotlib 整合

```python
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_chart():
    # Create a sample Matplotlib figure
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])
    ax.set_title("Sample Chart")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")

    return fig

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Matplotlib Chart in Tkinter")
        self.geometry("600x500")

        # Create a container frame for the chart
        chart_frame = ttk.Frame(self)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Matplotlib figure and embed it in Tkinter
        fig = create_chart()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()

```