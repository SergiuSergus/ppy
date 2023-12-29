import tkinter as tk
from pathlib import Path
from tkinter import ttk  #un upgrade estetic la tkinter
from tkinterdnd2 import DND_FILES, TkinterDnD  #wrapper peste tkinter cu functionalitati de drag and drop
import pandas as pd

class Aplication(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
            #spun ca main_frame trebuie sa se extinda in interiorul ferestrei principale a clasei Aplication ocupand tot spatiul
            #de exemplu daca aveam second_frame atunci spatiul trebuie impartit intre cele doua, dar noi avem una singura.
            #pt a intelege mai bine am facut main_frame de tip Label si am pus un text
            #in cazul pack(fill="both", expand="true") scrisul era centrat, dar in cazul pack() nu.
        self.geometry("900x500")
        self.search_page = SearchPage(parent=self.main_frame) 
            #deci practic main frameul este un spatiu mare cat toata fereastra pe care vin si il populez
            #cu un obiect de tip search page care este legat de main frame-ul meu, de aceea folosesc parent,
            #main-frameul(parent) este ca un suport pentru restul interfetei

class DataTable(ttk.Treeview): #Treeview este o clasa care ofera vizualizarea datelor sub forma unui tabel multi-coloana, fiecarei coloana corespunzand un header
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
            #yview este o metoda a widgetului de tip Treeview care permite scrollbarului sa controleze comportamentul scroll-ului pe axa verticala a widgetului        
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
            #aici configuram Treeview-ul ca scrolatul prin el sa se faca folosind "butoanele" pe care le-am definit folosind tkinter
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        self.stored_dataframe = pd.DataFrame() #un data frame gol

class SearchPage(tk.Frame): # deci pagina asta este un Frame din tkinter
    def __init__(self, parent):
        super().__init__(parent)
        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray") # SINGLE, putem selecta sa vizualizam un singur csv odata
        self.file_names_listbox.place(relheight=1, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
            #drop_target_register este o metoda care inregistreaza widgetul ca loc in care sa dau drop la fisiere
            #DND_FILES este un tip de data pentru operatii de tip drag-and-drop care implica fisiere, deci dandu-l ca argument inseamna ca widgetul poate sa accepte fisiere
            #care au fost trase si dropate pe el, totodata aste inseamna ca widgetul primeste path-ul fisierului.
        self.file_names_listbox.dnd_bind("<<Drop>>")
            #leg eventimentul de dropare cu o functie care face ceva in legatura cu asta
        self.file_names_listbox.bind("<Double-1>")
            #leg evenimetul de dublu click cu o functie care face ceva in legatura cu asta
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.75)
        self.search_entrybox.bind("<Return>")

        self.data_table = DataTable(parent)
        self.data_table.place(rely=0.05, relx=0.25, relwidth=0.75, relheight=0.95)

root = Aplication()
root.mainloop()
