import turtle
import sys
import math

screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Fractal Generator")
screen.bgcolor("black")
screen.tracer(0)

ui = turtle.Turtle()
ui.hideturtle()
ui.speed(0)

draw = turtle.Turtle()
draw.hideturtle()
draw.speed(0)

settings = {
    "fractal": None,
    "recursion": 4,
    "colors": ["purple", "black"],
    "size": 150,
    "snowflake_shape": "triangle",  # for koch snowflake base shape
}

COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "black", "white", "pink", "cyan"]
SNOWFLAKE_SHAPES = ["triangle", "square", "pentagon"]

buttons = []

def draw_button(x, y, w, h, text, highlight=False):
    ui.up()
    outline = "white" if highlight else "yellow"
    ui.color(outline, "black")
    ui.goto(x - w/2, y - h/2)
    ui.down()
    ui.begin_fill()
    for dx, dy in [(w,0),(0,h),(-w,0),(0,-h)]:
        ui.goto(ui.xcor()+dx, ui.ycor()+dy)
    ui.end_fill()
    ui.up()
    ui.goto(x, y - 8)
    ui.color(outline)
    ui.write(text, align="center", font=("Arial", 13, "normal"))

def add_button(x, y, w, h, text, action, highlight=False):
    draw_button(x, y, w, h, text, highlight)
    buttons.append((x, y, w, h, action))

def clicked(x, y, bx, by, bw, bh):
    return abs(x - bx) <= bw/2 and abs(y - by) <= bh/2

def on_click(x, y):
    for (bx, by, bw, bh, action) in buttons:
        if clicked(x, y, bx, by, bw, bh):
            action()
            return

screen.onscreenclick(on_click)

def clear():
    ui.clear()
    draw.clear()
    buttons.clear()

def main_menu():
    clear()
    ui.up(); ui.goto(0, 150)
    ui.color("yellow")
    ui.write("Fractal Generator", align="center", font=("Arial", 22, "bold"))
    add_button(0, 40, 200, 50, "Generate", fractal_select)
    add_button(0, -40, 200, 50, "Exit", sys.exit)
    screen.update()

def fractal_select():
    clear()
    ui.up(); ui.goto(0, 240)
    ui.color("yellow")
    ui.write("Pick a fractal:", align="center", font=("Arial", 16, "bold"))

    add_button(0, 130, 250, 45, "Sierpinski Triangle", lambda: pick_fractal("sierpinski"))
    add_button(0,  60, 250, 45, "Koch Snowflake",      lambda: pick_fractal("koch"))
    add_button(0, -10, 250, 45, "Fractal Tree",        lambda: pick_fractal("tree"))

    add_button(0, -200, 150, 40, "Back", main_menu)
    screen.update()

def pick_fractal(name):
    settings["fractal"] = name
    customize()

def customize():
    clear()
    ui.up(); ui.goto(0, 250)
    ui.color("yellow")
    ui.write(f"Customize: {settings['fractal']}", align="center", font=("Arial", 16, "bold"))

    ui.goto(-200, 160)
    ui.write(f"Recursion depth: {settings['recursion']}", font=("Arial", 13, "normal"))
    add_button(-60, 110, 80, 35, "less", lambda: change_recursion(-1))
    add_button( 60, 110, 80, 35, "more", lambda: change_recursion(1))

    ui.up(); ui.goto(-200, 55)
    ui.write(f"Size: {settings['size']}", font=("Arial", 13, "normal"))
    add_button(-60, 10, 80, 35, "smaller", lambda: change_size(-30))
    add_button( 60, 10, 80, 35, "bigger",  lambda: change_size(30))

    # size preview box
    ui.up()
    ui.color("yellow")
    s = settings["size"]
    ui.goto(260 - s/2, -s/2)
    ui.down()
    for dx, dy in [(s,0),(0,s),(-s,0),(0,-s)]:
        ui.goto(ui.xcor()+dx, ui.ycor()+dy)
    ui.up()
    ui.goto(260, -s/2 - 15)
    ui.write("size preview", align="center", font=("Arial", 9, "normal"))

    # koch shape picker (only show if koch selected)
    if settings["fractal"] == "koch":
        ui.up(); ui.goto(-200, -45)
        ui.color("yellow")
        ui.write("Base shape:", font=("Arial", 13, "normal"))
        for i, shape in enumerate(SNOWFLAKE_SHAPES):
            active = settings["snowflake_shape"] == shape
            add_button(-130 + i*100, -85, 90, 32, shape, make_shape_picker(shape), highlight=active)

    # colors
    color_y_start = -130 if settings["fractal"] == "koch" else -60
    ui.up(); ui.goto(-200, color_y_start)
    ui.color("yellow")
    ui.write("Colors (click to toggle):", font=("Arial", 13, "normal"))

    for i, c in enumerate(COLORS):
        cx = -180 + (i % 5) * 75
        cy = color_y_start - 45 - (i // 5) * 50
        active = c in settings["colors"]
        ui.up(); ui.color("yellow", c)
        ui.goto(cx - 28, cy - 14)
        ui.down(); ui.begin_fill()
        for dx, dy in [(56,0),(0,28),(-56,0),(0,-28)]:
            ui.goto(ui.xcor()+dx, ui.ycor()+dy)
        ui.end_fill()
        if active:
            ui.up(); ui.goto(cx - 28, cy - 14)
            ui.color("yellow"); ui.down()
            ui.pensize(3)
            for dx, dy in [(56,0),(0,28),(-56,0),(0,-28)]:
                ui.goto(ui.xcor()+dx, ui.ycor()+dy)
            ui.pensize(1)
        def make_toggle(col):
            def t():
                if col in settings["colors"]: settings["colors"].remove(col)
                else: settings["colors"].append(col)
                customize()
            return t
        buttons.append((cx, cy, 56, 28, make_toggle(c)))

    add_button(-80, -285, 160, 45, "Draw!", run_fractal)
    add_button(100, -285, 120, 45, "Back", fractal_select)
    screen.update()

def make_shape_picker(shape):
    def a():
        settings["snowflake_shape"] = shape
        customize()
    return a

def change_recursion(d):
    settings["recursion"] = max(1, min(7, settings["recursion"] + d))
    customize()

def change_size(d):
    settings["size"] = max(50, min(280, settings["size"] + d))
    customize()



def midpt(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def fill_tri(t, pts, color):
    t.up(); t.color(color, color)
    t.begin_fill()
    t.goto(pts[0]); t.down()
    t.goto(pts[1]); t.goto(pts[2]); t.goto(pts[0])
    t.end_fill()

def draw_sierpinski(t, pts, depth, max_depth, colors):
    if not colors:
        t.up(); t.color("white")
        t.goto(pts[0]); t.down()
        t.goto(pts[1]); t.goto(pts[2]); t.goto(pts[0])
        t.up()
    else:
        c = colors[depth % len(colors)]
        fill_tri(t, pts, c)
    if depth > 0:
        m01 = midpt(pts[0], pts[1])
        m02 = midpt(pts[0], pts[2])
        m12 = midpt(pts[1], pts[2])
        draw_sierpinski(t, [pts[0], m01, m02], depth-1, max_depth, colors)
        draw_sierpinski(t, [pts[1], m01, m12], depth-1, max_depth, colors)
        draw_sierpinski(t, [pts[2], m02, m12], depth-1, max_depth, colors)

# Koch snowflake — draw one side recursively
def koch_side(t, depth, length, colors, depth_level):
    if depth == 0:
        if colors:
            t.color(colors[depth_level % len(colors)])
        else:
            t.color("white")
        t.down()
        t.forward(length)
        return
    length /= 3
    koch_side(t, depth-1, length, colors, depth_level+1)
    t.left(60)
    koch_side(t, depth-1, length, colors, depth_level+1)
    t.right(120)
    koch_side(t, depth-1, length, colors, depth_level+1)
    t.left(60)
    koch_side(t, depth-1, length, colors, depth_level+1)

def draw_koch(t, size, depth, colors, shape):
    if shape == "triangle":
        sides = 3; angle = 120; start_angle = 0
    elif shape == "square":
        sides = 4; angle = 90; start_angle = 45
    else:  # pentagon
        sides = 5; angle = 72; start_angle = 18

    length = size * 1.5

    # figure out starting position so shape is centered
    r = length / (2 * math.sin(math.pi / sides))
    t.up()
    t.goto(0, -r * 0.5)
    t.setheading(start_angle)

    for _ in range(sides):
        koch_side(t, depth, length, colors, 0)
        t.right(angle)

# Fractal tree
def draw_tree(t, x, y, angle, length, depth, colors):
    if depth == 0:
        return
    if colors:
        t.color(colors[depth % len(colors)])
    else:
        t.color("white")
    t.pensize(max(1, depth))

    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    t.up(); t.goto(x, y)
    t.down(); t.goto(x2, y2)

    draw_tree(t, x2, y2, angle + 30, length * 0.7, depth-1, colors)
    draw_tree(t, x2, y2, angle - 30, length * 0.7, depth-1, colors)

def run_fractal():
    clear()
    ui.up(); ui.goto(0, 270)
    ui.color("yellow")
    ui.write("Drawing... (this may take a sec)", align="center", font=("Arial", 12, "normal"))
    screen.update()

    s = settings["size"]
    colors = settings["colors"]
    fractal = settings["fractal"]
    depth = settings["recursion"]

    screen.tracer(1)
    if fractal == "sierpinski":
        pts = [(-s, -s*0.7), (s, -s*0.7), (0, s*0.9)]

        draw.up(); draw.color("white")
        draw.goto(pts[0]); draw.down()
        draw.goto(pts[1]); draw.goto(pts[2]); draw.goto(pts[0])
        draw.up()
        draw_sierpinski(draw, pts, depth, depth, colors)

    elif fractal == "koch":
        draw_koch(draw, s, depth, colors, settings["snowflake_shape"])

    elif fractal == "tree":
        draw_tree(draw, 0, -s, 90, s * 0.7, depth, colors)

    screen.tracer(0)
    add_button(0, -270, 150, 45, "Back", customize)
    screen.update()

main_menu()
turtle.mainloop()