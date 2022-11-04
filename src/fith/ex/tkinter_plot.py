import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()

# First create a figure
fig = Figure(figsize=(5, 4), dpi=100)
# Create a plot on that figure
plot = fig.add_subplot()

# Plot the values on the figure
value1 = (27, 28.3, 25.7, 26.9, 29.9, 30, 30.03, 31.2, 27.9, 27.1, 25.4,
          26.5, 26.2, 28.5, 29.1, 29)
value2 = (26.8, 27.9, 25.1, 28, 29, 29.6, 29.9, 30.7, 23, 27.5, 24.3, 28,
          27.5, 31.5, 30, 32)
box_plot_data = (value1, value2)
plot.boxplot(box_plot_data)

# Create a canvas widget from the figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
# And then `.pack` it
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()

if __name__ == '__main__':
    pass