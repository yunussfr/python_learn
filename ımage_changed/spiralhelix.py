import turtle

turtle_screen = turtle.Screen()
turtle_screen.bgcolor("darkgrey")
turtle_screen.title("sallama_baba_sallama")


turtle_instance=turtle.Turtle()
turtle_instance.color("red")
turtle_instance.speed(0)
turtle_colors=["purple","green","blue"]
for i in range(10):
    turtle_instance.color(turtle_colors[i%3])
    turtle_instance.circle(10*i)
    turtle_instance.left(90)
    turtle_instance.circle(-10*i)
turtle.mainloop()
