import tkinter
#window
window = tkinter.Tk()
window.title("My first window")
window.minsize(400, 300)

#label
my_label=tkinter.Label(text="this is  label",font=("Arial",20,"italic"))
#my_label.config(bg="white",fg="black")
#my_label.pack(side="bottom")
#my_label.place(x=0,y=0)
my_label.grid(row=0,column=0)
def click_buttom():
    user_input=my_entry.get()
    print(user_input)
    test()
#buttom
my_buttom=tkinter.Button(text="this is button",command=click_buttom)
#my_buttom.pack(side="bottom")
my_buttom.grid(row=1,column=1)
def test():
    pass
#entry
my_entry=tkinter.Entry(width=30)
#my_entry.pack(side="bottom")
my_entry.grid(row=2,column=2)
window.mainloop()