from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="HEHE",padx=100, bg="blue")
    myLabel.pack()

myButton = Button(root, text="Click Me!", padx=100, pady=100, command=myClick, bg="red", fg="blue")
myButton.pack()


root.mainloop()
