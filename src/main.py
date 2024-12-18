import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from main import get_figure, setq, get_mode, set_mode

def main():
    mode = ""
    def update_charge():
        try:
            q = float(charge_input.get())
        except ValueError:
            q = 1
            print("Defaulted to charge of 1")
        finally:
            setq(q)
    def update_mode(event=None):
        set_mode(mode_selector.get())
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
    ttk.Label(input_frame, text="Charge:").pack(side=tk.LEFT, padx=5)
    charge_input = ttk.Entry(input_frame, width=10)
    charge_input.pack(side=tk.LEFT, padx=5)
    
    update_q_button = ttk.Button(input_frame, text="Update Charge", command=update_charge)
    update_q_button.pack(side=tk.LEFT, padx=5)
    
    ttk.Label(input_frame, text="Select Mode:").pack(side=tk.LEFT, padx=5)
    mode_selector = ttk.Combobox(input_frame, textvariable=mode, values=["Add", "Del", "Move"], state="readonly")
    mode_selector.pack(side=tk.LEFT, padx=5)
    mode_selector.bind("<<ComboboxSelected>>", update_mode)

    root.mainloop()

if __name__ == "__main__":
    main()