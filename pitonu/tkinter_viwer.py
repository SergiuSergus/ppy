import tkinter as tk
from pathlib import Path
from tkinter import ttk  #un upgrade estetic la tkinter
from tkinterdnd2 import DND_FILES, TkinterDnD  #wrapper peste tkinter cu functionalitati de drag and drop
import pandas as pd
from tkinter import messagebox

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

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children()) #curatam tot ce era in treeview
        columns = list(dataframe.columns) #facem o lista cu numele coloanelor, cuma ar fi Durata, Puls, MaxPuls, Calorii din data.csv
        self.__setitem__("column", columns) #setam coloanele treeview-ului("column") cu numele coloanelor din dataframe
        self.__setitem__("show", "headings") #spunem ca treeview-ul vrem sa aibe headings

        for col in columns:
            self.heading(col, text=col)  #setam headings cu numele coloanelor din dataframe, primul argument col este un index, astfel
            #primului heading(0) ii corepsunde numele coloanei de la indexul 0 si tot asa mai departe. 

        df_rows = dataframe.to_numpy().tolist() #facem o lista de liste cu continutul efectiiv al tabelului si le inseram in acesta
        for row in df_rows:
            self.insert("", "end", values=row)
        return None
        
    def find_value(self, pairs): #pairs este un dictionar
        #deci o sa caut spre exemplu Calorii=10
        new_df = self.stored_dataframe
        for col, value in pairs.items():
            new_df = new_df[new_df[col].astype(str).str.contains(str(value))] #!!!!
        self._draw_table(new_df)    
        #pentru fiecare pereche coloana-valoare din tabelul de perechi va cauta coloana cu numele col(Durata) si stringuri care contin
        #pe value(10) de pe aceasta coloana si va face un nou dataframe cu ele si il va desena

    def reset_table(self):
        self._draw_table(self.stored_dataframe) #pt ca stored_dataframe era un DataFrame() gol   

class SearchPage(tk.Frame): # deci pagina asta este un Frame din tkinter
    def __init__(self, parent):
        super().__init__(parent)
        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray") # SINGLE, putem selecta sa vizualizam un singur csv odata
        self.file_names_listbox.place(relheight=1, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
            #drop_target_register este o metoda care inregistreaza widgetul ca loc in care sa dau drop la fisiere
            #DND_FILES este un tip de data pentru operatii de tip drag-and-drop care implica fisiere, deci dandu-l ca argument inseamna ca widgetul poate sa accepte fisiere
            #care au fost trase si dropate pe el, totodata aste inseamna ca widgetul primeste path-ul fisierului.
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_listbox)
            #leg eventimentul de dropare cu o functie care face ceva in legatura cu asta
        self.file_names_listbox.bind("<Double-1>", self._display_file)
            #leg evenimetul de dublu click cu o functie care face ceva in legatura cu asta
            #cand voi da dublu click pe unul dintre csv-urile pe care le am adugat in listbox, voi vedea un treeview corespunzator dataframeului din csv
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.75)
        self.search_entrybox.bind("<Return>", self.search_table)
            #leg evenimetul de press Enter cu o functie care face ceva in legatura cu asta
            #adica scriu in searchbar/entrybox si cand amterminat de adugat sau ster caractere dau enter ca vad noul tabel
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0.05, relx=0.25, relwidth=0.75, relheight=0.95)

        self.path_map = {} #dictionar gol

    def drop_inside_listbox(self, event):
        file_paths = self._parse_drop_files(event.data) #deci file_paths este o lsita
        current_listbox_items = set(self.file_names_listbox.get(0, "end"))
        for file_path in file_paths:
            if Path(file_path).suffix != '.csv': #!!!!
                messagebox.showinfo(title="!", message="Sorry, this is not a CSV file")
                raise Exception("Sorry, this is not a CSV file")
            path_object = Path(file_path)
            file_name = path_object.name
            #am folosit obiecte de tip Path din libraria pathlib pentru a obtine mai rapid numele fisierului folosind metoda .name
            if file_name not in current_listbox_items:
                self.file_names_listbox.insert("end", file_name)
                self.path_map[file_name] = file_path
      #de asemenea am lucrat cu set pentru a nu regasi in lista de fisiere un fisier de mai multe ori
                  
    def _display_file(self, event):
        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection()) #folosim curselection ca sa obtinem numele fisierului pe care dam dubluclick
        path = self.path_map[file_name]
        df = pd.read_csv(path)
        self.data_table.set_datatable(dataframe=df)

    def search_table(self, event):
        #column=value,column2=value2,.......
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
                #[column=value,column2=value2,.......]
            column_value_pairs = {} #dictionar
            for pair in entry_split:
                pair_split = pair.split("=")
                    #[[column,value],[column2,value2],.......]
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs = column_value_pairs)        


    def _parse_drop_files(self, filename):
        #cu functia aceasta vom stoca path-urile fisierelor
        #observam in ss2 si ss3 ca pathrile sunt concatenate in acelasi string si se regasesc si o pereche de {}
        #functia trateaza orice caz posibil si stocheaza cu succes path-urile 
        #acesta este filename-ul cand fac drag and drop la data 2.csv si data.csv simultan
        #'{D:/py/pitonu/data 2.csv} D:/py/pitonu/data.csv'
        size = len(filename)
        res = [] #lista path-urilor fisierelor cu care am facut drag and drop
        name = ""
        idx = 0
        while idx<size:
            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":
                    name += filename[j]
                    j+=1
                res.append(name)
                name=""
                idx = j
            elif filename[idx] == " " and name != "":
                #pentru exemplul '{D:/py/pitonu/data 2.csv} D:/py/pitonu/data.csv' nu se intra in acest elif
                #dar pentru exemplul 'D:/py/pitonu/data2.csv D:/py/pitonu/data.csv' observam ca se intra in elif si deci se trateaza si genul asta de date de intrare in event
                res.append(name)
                name=""
            elif filename[idx] != " ":
                name += filename[idx]
            idx += 1
        if name != "":
            res.append(name)
        return res            

root = Aplication()
root.mainloop()
