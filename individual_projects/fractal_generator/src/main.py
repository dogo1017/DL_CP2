# Fractal Generator Entry Point
# Initializes the turtle event listener and opens the first menu
# This is the file the user runs to start the program
import turtle
import config
import ui_controls
import menus

# Main setup function
def main():
    # Tell turtle to call our on_click function whenever the mouse is clicked
    config.screen.onscreenclick(ui_controls.on_click)
    
    # Start the program by opening the main menu
    menus.main_menu()
    
    # Keep the window open and wait for user input
    turtle.mainloop()


main()