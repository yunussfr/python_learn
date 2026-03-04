import turtle
turtle_screen=turtle.Screen()
turtle_screen.bgcolor("black")
turtle_screen.title("Tıtututurırlrfneewl")


turtle_instance=turtle.Turtle()
turtle_instance.color("blue")

def shirkingSquare(size):
    for i in range(4):
      turtle_instance.forward(size)
      turtle_instance.left(90)
      size=size-5

shirkingSquare(150)
shirkingSquare(120)
shirkingSquare(90)
shirkingSquare(60)
shirkingSquare(30)

turtle.done()