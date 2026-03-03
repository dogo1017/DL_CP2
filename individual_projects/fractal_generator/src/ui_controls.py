# UI Control Module
# Handles the math for drawing buttons and detecting where the user clicks
# Uses the theme settings to decide which colors to use for text and boxes
import config

# Checks the current theme and returns a color that will be visible against the background
def get_text_color():
    if config.settings["theme"] == "dark":
        return "yellow"
    else:
        return "black"

# Draws a single rectangular button box with a text label in the middle
def draw_button(x, y, w, h, text, highlight=False):
    config.ui.up()
    
    # If the button is "active" (like a selected color), give it a special border
    if highlight:
        outline = "red" if config.settings["theme"] == "light" else "white"
    else:
        outline = get_text_color()

    # Draw the rectangle fill
    fill_color = "gray" if config.settings["theme"] == "light" else "black"
    config.ui.color(outline, fill_color)
    config.ui.goto(x - w / 2, y - h / 2)
    config.ui.down()
    config.ui.begin_fill()
    for dx, dy in [(w, 0), (0, h), (-w, 0), (0, -h)]:
        config.ui.goto(config.ui.xcor() + dx, config.ui.ycor() + dy)
    config.ui.end_fill()
    
    # Write the text label inside the rectangle
    config.ui.up()
    config.ui.goto(x, y - 8)
    config.ui.color(outline)
    config.ui.write(text, align="center", font=("Arial", 13, "normal"))

# Records a button's location and its function so the click handler can find it later
def add_button(x, y, w, h, text, action, highlight=False):
    draw_button(x, y, w, h, text, highlight)
    config.buttons.append((x, y, w, h, action))

# Takes the mouse click coordinates and loops through all buttons to see if one was hit
def on_click(x, y):
    for (bx, by, bw, bh, action) in config.buttons:
        # Check if the click (x, y) is within the bounds of the button (bx, by)
        if abs(x - bx) <= bw / 2 and abs(y - by) <= bh / 2:
            action()
            return

# Clears both the UI and Drawing turtles and empties the active button list
def clear():
    config.ui.clear()
    config.draw.clear()
    config.buttons.clear()