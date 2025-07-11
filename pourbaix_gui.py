import sys
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    import pyCHNOSZ as pyc
except ImportError:
    pyc = None


def draw_pourbaix(selected_species):
    if pyc is None:
        messagebox.showerror("pyCHNOSZ not available", "pyCHNOSZ 0.9.1 must be installed")
        return None
    # Setup the aqueous basis species
    try:
        pyc.reset()
        pyc.basis("CHNOS+", selected_species)
        fig = plt.figure(figsize=(5,4))
        pyc.diagram("Eh-pH", fig=fig)
        return fig
    except Exception as e:
        messagebox.showerror("Diagram error", str(e))
        return None


def on_draw(fig_area, species_listbox):
    selected = [species_listbox.get(i) for i in species_listbox.curselection()]
    if not selected:
        messagebox.showinfo("Selection required", "Please select at least one species")
        return
    fig = draw_pourbaix(selected)
    if fig:
        for widget in fig_area.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=fig_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def main(species):
    root = tk.Tk()
    root.title("pyCHNOSZ Pourbaix Diagram")

    left_frame = ttk.Frame(root)
    left_frame.pack(side="left", fill="y")

    list_label = ttk.Label(left_frame, text="Compounds")
    list_label.pack(padx=5, pady=5)

    species_var = tk.StringVar(value=species)
    species_listbox = tk.Listbox(left_frame, listvariable=species_var, selectmode="multiple", height=15)
    species_listbox.pack(padx=5, pady=5)

    draw_btn = ttk.Button(left_frame, text="Draw", command=lambda: on_draw(fig_area, species_listbox))
    draw_btn.pack(padx=5, pady=5)

    fig_area = ttk.Frame(root, borderwidth=2, relief="sunken")
    fig_area.pack(side="right", fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    default_species = [
        "H2O", "O2", "H+", "H2", "CO2", "CO3--", "CH4"  # Example species
    ]
    main(default_species)
