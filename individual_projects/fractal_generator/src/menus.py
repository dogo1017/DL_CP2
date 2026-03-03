# Menu and Navigation Logic
# Controls the flow between the start screen, settings, and drawing screens
# Updates the global settings dictionary based on user button clicks
import sys
import config
import ui_controls
import fractals

# Displays the title and main three navigation buttons
def main_menu():
    ui_controls.clear()
    config.ui.up(); config.ui.goto(0, 150)
    config.ui.color(ui_controls.get_text_color())
    config.ui.write("Fractal Generator", align="center", font=("Arial", 22, "bold"))
    
    ui_controls.add_button(0, 40, 200, 50, "Generate", fractal_select)
    ui_controls.add_button(0, -30, 200, 50, "Settings", setting_screen)
    ui_controls.add_button(0, -100, 200, 50, "Exit", sys.exit)
    config.screen.update()

# Screen for global application settings like Light/Dark mode
def setting_screen():
    ui_controls.clear()
    config.ui.up(); config.ui.goto(0, 150)
    config.ui.color(ui_controls.get_text_color())
    config.ui.write("Settings", align="center", font=("Arial", 22, "bold"))

    current_theme = config.settings["theme"].capitalize()
    ui_controls.add_button(0, 40, 250, 50, f"Theme: {current_theme}", toggle_theme)
    ui_controls.add_button(0, -30, 200, 50, "Back", main_menu)
    config.screen.update()

# Switches the theme variable and updates the background color immediately
def toggle_theme():
    if config.settings["theme"] == "dark":
        config.settings["theme"] = "light"
        config.screen.bgcolor("white")
    else:
        config.settings["theme"] = "dark"
        config.screen.bgcolor("black")
    setting_screen()

# Sub-menu for choosing which fractal type to customize
def fractal_select():
    ui_controls.clear()
    config.ui.up(); config.ui.goto(0, 240)
    config.ui.color(ui_controls.get_text_color())
    config.ui.write("Pick a fractal:", align="center", font=("Arial", 16, "bold"))

    ui_controls.add_button(0, 130, 250, 45, "Sierpinski Triangle", lambda: pick_fractal("sierpinski"))
    ui_controls.add_button(0, 60, 250, 45, "Koch Snowflake", lambda: pick_fractal("koch"))
    ui_controls.add_button(0, -10, 250, 45, "Fractal Tree", lambda: pick_fractal("tree"))
    ui_controls.add_button(0, -200, 150, 40, "Back", main_menu)
    config.screen.update()

# Sets the active fractal and enters the customization phase
def pick_fractal(name):
    config.settings["fractal"] = name
    customize()

# Increments or decrements recursion depth within a safe range
def change_recursion(d):
    config.settings["recursion"] = max(1, min(7, config.settings["recursion"] + d))
    customize()

# Updates the fractal size multiplier
def change_size(d):
    config.settings["size"] = max(50, min(280, config.settings["size"] + d))
    customize()

# Toggles the fill state for the Sierpinski Triangle
def toggle_fill():
    config.settings["fill"] = not config.settings["fill"]
    customize()

# Factory function to create a closure for picking a snowflake base shape
def make_shape_picker(shape):
    def pick():
        config.settings["snowflake_shape"] = shape
        customize()
    return pick

# Factory function to create a closure for toggling individual colors in the list
def make_toggle(col):
    def toggle():
        if col in config.settings["colors"]: config.settings["colors"].remove(col)
        else: config.settings["colors"].append(col)
        customize()
    return toggle

# Main customization screen that dynamically shows options based on fractal type
# Main customization screen that dynamically shows options based on fractal type
def customize():
    ui_controls.clear()
    text_color = ui_controls.get_text_color()
    
    config.ui.up(); config.ui.goto(0, 250); config.ui.color(text_color)
    config.ui.write(f"Customize: {config.settings['fractal']}", align="center", font=("Arial", 16, "bold"))

    # Render Depth controls
    config.ui.goto(-200, 160)
    config.ui.write(f"Recursion depth: {config.settings['recursion']}", font=("Arial", 13, "normal"))
    ui_controls.add_button(-60, 110, 80, 35, "less", lambda: change_recursion(-1))
    ui_controls.add_button(60, 110, 80, 35, "more", lambda: change_recursion(1))

    # Render Size controls
    config.ui.up(); config.ui.goto(-200, 55)
    config.ui.write(f"Size: {config.settings['size']}", font=("Arial", 13, "normal"))
    ui_controls.add_button(-60, 10, 80, 35, "smaller", lambda: change_size(-30))
    ui_controls.add_button(60, 10, 80, 35, "bigger", lambda: change_size(30))

    # Size preview box on the right
    config.ui.up(); config.ui.color(text_color)
    s = config.settings["size"]
    config.ui.goto(260 - s / 2, -s / 2); config.ui.down()
    for dx, dy in [(s, 0), (0, s), (-s, 0), (0, -s)]:
        config.ui.goto(config.ui.xcor() + dx, config.ui.ycor() + dy)
    config.ui.up(); config.ui.goto(260, -s / 2 - 15)
    config.ui.write("size preview", align="center", font=("Arial", 9, "normal"))

    # Adjust layout based on fractal type to prevent overlap
    if config.settings["fractal"] == "koch":
        config.ui.up(); config.ui.goto(-200, -45); config.ui.color(text_color)
        config.ui.write("Base shape:", font=("Arial", 13, "normal"))
        for i, shape in enumerate(config.SNOWFLAKE_SHAPES):
            active = config.settings["snowflake_shape"] == shape
            ui_controls.add_button(-130 + i * 100, -85, 90, 32, shape, make_shape_picker(shape), highlight=active)
        color_y_start = -130
    elif config.settings["fractal"] == "sierpinski":
        config.ui.up(); config.ui.goto(-200, -45); config.ui.color(text_color)
        config.ui.write("Fill Shape:", font=("Arial", 13, "normal"))
        fill_text = "ON" if config.settings["fill"] else "OFF"
        ui_controls.add_button(-100, -85, 90, 32, fill_text, toggle_fill, highlight=config.settings["fill"])
        color_y_start = -130
    else:
        color_y_start = -50

    # Draw the color palette grid manually to show actual colors
    config.ui.up(); config.ui.goto(-200, color_y_start); config.ui.color(text_color)
    config.ui.write("Colors (click to toggle):", font=("Arial", 13, "normal"))
    
    for i, c in enumerate(config.COLORS):
        cx = -180 + (i % 5) * 75
        cy = color_y_start - 45 - (i // 5) * 50
        active = c in config.settings["colors"]
        
        # Draw the colored rectangle for each option
        config.ui.up(); config.ui.color(text_color, c)
        config.ui.goto(cx - 28, cy - 14)
        config.ui.down(); config.ui.begin_fill()
        for dx, dy in [(56, 0), (0, 28), (-56, 0), (0, -28)]:
            config.ui.goto(config.ui.xcor() + dx, config.ui.ycor() + dy)
        config.ui.end_fill()
        
        # If the color is selected, draw a thick border around it
        if active:
            config.ui.up(); config.ui.goto(cx - 28, cy - 14); config.ui.color(text_color)
            config.ui.down(); config.ui.pensize(3)
            for dx, dy in [(56, 0), (0, 28), (-56, 0), (0, -28)]:
                config.ui.goto(config.ui.xcor() + dx, config.ui.ycor() + dy)
            config.ui.pensize(1)
            
        # Add the invisible click detection for the color box
        config.buttons.append((cx, cy, 56, 28, make_toggle(c)))

    ui_controls.add_button(-80, -285, 160, 45, "Draw!", run_fractal)
    ui_controls.add_button(100, -285, 120, 45, "Back", fractal_select)
    config.screen.update()

# Exports the current canvas to a PostScript file
def save_image():
    config.screen.getcanvas().postscript(file="fractal.eps")
    config.ui.up(); config.ui.goto(0, -220)
    config.ui.color("green" if config.settings["theme"] == "dark" else "red")
    config.ui.write("Saved as fractal.eps!", align="center", font=("Arial", 14, "bold"))

# Core logic that starts the drawing process based on all current settings
def run_fractal():
    ui_controls.clear()
    config.ui.up(); config.ui.goto(0, 270)
    config.ui.color(ui_controls.get_text_color())
    config.ui.write("Drawing... (this may take a sec)", align="center", font=("Arial", 12, "normal"))
    config.screen.update()

    # Grab current settings from the config dictionary
    s = config.settings["size"]
    colors = config.settings["colors"]
    fractal = config.settings["fractal"]
    depth = config.settings["recursion"]

    # Show the drawing process in real-time
    config.screen.tracer(1)
    
    if fractal == "sierpinski":
        pts = [(-s, -s * 0.7), (s, -s * 0.7), (0, s * 0.9)]
        config.draw.up(); config.draw.color("black" if config.settings["theme"] == "light" else "white")
        config.draw.goto(pts[0]); config.draw.down()
        config.draw.goto(pts[1]); config.draw.goto(pts[2]); config.draw.goto(pts[0])
        config.draw.up()
        fractals.draw_sierpinski(config.draw, pts, depth, depth, colors, config.settings["fill"])

    elif fractal == "koch":
        fractals.draw_koch(config.draw, s, depth, colors, config.settings["snowflake_shape"])

    elif fractal == "tree":
        fractals.draw_tree(config.draw, 0, -s, 90, s * 0.7, depth, colors)

    # Drawing finished, switch back to manual updates
    config.screen.tracer(0)
    ui_controls.add_button(-80, -270, 130, 45, "Save Image", save_image)
    ui_controls.add_button(80, -270, 130, 45, "Back", customize)
    config.screen.update()