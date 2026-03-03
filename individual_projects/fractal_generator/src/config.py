# Fractal Generator Configuration
# Stores the global settings, turtle objects, and shared data for the whole program
# This allows different files to access the same "settings" and "draw" turtles
import turtle

# Create the main window and set the background to black by default
screen = turtle.Screen()
screen.setup(800, 600)
screen.title("Fractal Generator")
screen.bgcolor("black")

# Turn off animation updates so we can manually refresh the screen for speed
screen.tracer(0)

# Create a dedicated turtle for drawing the menu buttons and text
ui = turtle.Turtle()
ui.hideturtle()
ui.speed(0)

# Create a dedicated turtle for drawing the actual fractal shapes
draw = turtle.Turtle()
draw.hideturtle()
draw.speed(0)

# Dictionary to store all user choices so they persist between different menus
settings = {
    "fractal": None,
    "recursion": 4,
    "colors": ["purple", "black"],
    "size": 150,
    "snowflake_shape": "triangle",
    "theme": "dark",
    "fill": False
}

# Constants for the available colors and base shapes for the Koch snowflake
COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "black", "white", "pink", "cyan"]
SNOWFLAKE_SHAPES = ["triangle", "square", "pentagon"]

# List that will hold the coordinates and actions for every button currently on screen
buttons = []