from tkinter import *
#window
window=Tk()
window.title("My window")
window.minsize(width=700,height=600)
#label
label=Label(text="My label")
label.config(bg="white",fg="black",font=("times new roman",20))
label.config(padx=10,pady=10)
label.pack()

def buttonClick():
    print("You pressed the button")
    print(text.get("1.0",END))
    print(entry.get())
#button
button=Button(text="click here",command=buttonClick)
button.config(padx=10,pady=10)
button.pack(side="bottom")
#entry
entry=Entry(width=30)
entry.pack(side="left")
#multiline
text=Text(width=30)
text.focus()
text.pack()

#scale
def scale_selected(value):
    print(value)
my_scale=Scale(from_=0,to=50,command=scale_selected)
my_scale.pack(side="right")

#spinbox
spinbox=Spinbox(from_=0,to=50)
spinbox.pack()

#checkbutton
def checkbutton_selected():
   print(check_state.get())
check_state=IntVar()
my_checkbutton=Checkbutton(text="My checkbutton",variable=check_state,command=checkbutton_selected)
my_checkbutton.pack()
window.mainloop()