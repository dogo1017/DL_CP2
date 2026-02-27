import turtle

start_chords = [[-100,0]]

def draw_fractal(turtle,distance,chords,recursions):
    if recursions == 0: return
    turtle.goto(chords[0])
    chords.append([turtle.xcor(), turtle.ycor()])
    turtle.forward(distance)
    turtle.left(120)
    chords.append([turtle.xcor(), turtle.ycor()])
    turtle.forward(distance)
    turtle.left(120)
    chords.append([turtle.xcor(), turtle.ycor()])
    turtle.forward(distance)
    turtle.left(120)
    chords.pop(0)
    recursions -= 1
    return draw_fractal(turtle,distance,chords,recursions)


draw = turtle.Turtle()
draw.speed(0)
draw_fractal(draw,100,start_chords,5)
turtle.done()