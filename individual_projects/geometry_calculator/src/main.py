#DL main.py
import menu
import create_shapes

# Holds all the shape objects the user creates during the session
shape_list = []


# Main loop - keeps showing the menu and running the chosen action
# until the user chooses Quit
def main():
    while True:
        choice = menu.show_main_menu(shape_list)

        if choice == '1':
            # create_shape returns None if the user cancels, so only append if we got something
            new_shape = create_shapes.create_shape()
            if new_shape is not None:
                shape_list.append(new_shape)

        elif choice == '2':
            menu.view_all(shape_list)

        elif choice == '3':
            menu.select_shape(shape_list)

        elif choice == '4':
            menu.compare_shapes(shape_list)

        elif choice == '5':
            menu.sort_shapes(shape_list)

        elif choice == '6':
            menu.formula_guide()

        elif choice == '7':
            print("Goodbye!")
            break


main()