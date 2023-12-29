from pandas import *
from matplotlib.pyplot import *
from tkinter import *
from tkinter import messagebox, font

df = read_csv('data.csv')
print(df.to_string()) 
print('\n')

print(df.head(10)) 
print('\n')

df1 = df[["Durata", "Puls"]] 
print(df1.tail(6)) 
print('\n')

print("Minimul duratei este " + str(df["Durata"].min()))
print("Media pulsului este " + str(df["Puls"].mean()) + ",iar deviatia standard este " + str(df["Puls"].std()))
print("Cel mai mare puls este " + str(df["MaxPuls"].max()))
print("Numarul total de calorii arse este " + str(df["Calorii"].sum()))
print('\n')

print(df.describe())
print('\n')

print(df.corr())
print('\n')

root = Tk()

flag = 0

myButton = Button(root, text="SHOW ME STATS!", padx=90, pady=60)
myButton.pack()

font_curent = myButton.cget("font")
font_nou = font.nametofont(font_curent).copy()
font_nou.config(family="Arial", size=10, weight="bold")

myButton1 = Label(root, text="Folosind tabelul de corelatii observam ca o crestere a duratei implica o crestere in calorii.", font=font_nou)
myButton2 = Label(root, text="De asemenea, un puls mediu ridicat implica si un puls maxim mai ridicat", font=font_nou)

df2 = df.sort_values(by = ["Durata"])
print(df2.to_string())
print('\n')

def plot_durata_calorii():
    figure()
    plot(df2["Durata"], df2["Calorii"], color='blue')
    title('Dependența dintre Durata și Calorii')
    xlabel('Durata')
    ylabel('Calorii')
    show()

def myClick():
    global flag
    global myButton
    if flag == 0:
        bargraph1 = df.plot.bar()
        myButton.config(text="NEXT")
        myButton1.pack()
        flag = 1
    elif flag == 1:
        bargraph2 = df.head(10).plot.bar()
        myButton2.pack()
        flag = 2
    elif flag == 2:
        bargraph3 = df1.tail(6).plot.bar()
        flag = 3
    else:
        plot_durata_calorii()
        flag = 72        
    show()         
    if flag == 72:
        flag = 0
        messagebox.showinfo(title="!", message="END OF STATS!")
        root.destroy()   
    

myButton.config(command=myClick)

root.mainloop()



