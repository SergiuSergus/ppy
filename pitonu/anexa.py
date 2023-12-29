import tkinter as tk
from pathlib import Path
from tkinter import ttk  #un upgrade estetic la tkinter
from tkinterdnd2 import DND_FILES, TkinterDnD  #wrapper peste tkinter cu functionalitati de drag and drop
import pandas as pd

dataframe = pd.DataFrame(pd.read_csv('data.csv'))

columns = list(dataframe.columns)

print(columns)

root = tk.Tk()

tabel = ttk.Treeview()

tabel.__setitem__("columns", columns)
tabel.__setitem__("show", "headings")

for col in columns:
    tabel.heading(col, text=col)

df_rows = dataframe.to_numpy().tolist() #!!!!!
for row in df_rows:
    tabel.insert("", "end", values=row)

tabel.pack(expand=True, fill='both')

root.mainloop()