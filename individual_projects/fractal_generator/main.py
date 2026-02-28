import turtle

chords = [[-50,0],[50,0],[0,100]]

def midpt(pt1,pt2):
  return ((pt1[0] + pt2[0])/2, ((pt1[1] + pt2[1]) /2))
  

def ind_triangle(points, turtle):
  turtle.up()
  turtle.goto(points[0])
  turtle.down()
  turtle.goto(points[1])
  turtle.goto(points[2])
  turtle.goto(points[0])

def draw_fractal(turtle,chords,recursion):
  ind_triangle(chords,turtle)
  
  if recursion > 0:
    draw_fractal(turtle,[chords[0],midpt(chords[0],chords[1]),midpt(chords[0],chords[2])],recursion-1)
    draw_fractal(turtle,[chords[1],midpt(chords[0],chords[1]),midpt(chords[1],chords[2])],recursion-1)
    draw_fractal(turtle,[chords[2],midpt(chords[2],chords[1]),midpt(chords[0],chords[2])],recursion-1)
  
    

draw = turtle.Turtle()
draw.speed(0)
draw_fractal(draw,chords,7)
turtle.done()