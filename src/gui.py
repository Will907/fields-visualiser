import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import get_figure

def main():
    # Create the main tkinter window
    root = tk.Tk()
    root.title("Electric Field Visualisation")

    plot_frame = ttk.Frame(root)
    plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    fig = get_figure()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Additional GUI here
    input_frame = ttk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    ttk.Label(input_frame, text="Additional controls here").pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()