from tkinter import *

root = Tk()

camp = Entry(root, width=50, bg="blue", fg="white", borderwidth=10)
camp.pack()
camp.insert(0, "Enter your name, sir: ")

def myClick():
    myLabel = Label(root, text="Hello "+camp.get(),padx=100, bg="blue")
    myLabel.pack()

myButton = Button(root, text="ENTER", padx=100, pady=100, command=myClick, bg="red", fg="blue")
myButton.pack()


root.mainloop()
