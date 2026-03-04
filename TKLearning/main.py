import tkinter
#window
window = tkinter.Tk()
window.title("My first window")
window.minsize(400, 300)

#label
my_label=tkinter.Label(text="this is a label",font=("Arial",20,"bold"))
#my_label.config(bg="white",fg="black")
my_label.pack()
def click_buttom():
    print("buttom clicked")
    test()
#buttom
my_buttom=tkinter.Buttom(text="this is a button",command=click_buttom)
def test():
    pass

window.mainloop()