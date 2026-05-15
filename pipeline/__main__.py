"""Entry point: py -m pipeline (run from observatory root)"""
from pipeline.gui import WorkbenchApp
import tkinter as tk

root = tk.Tk()
WorkbenchApp(root)
root.mainloop()
