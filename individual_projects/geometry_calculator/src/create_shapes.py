#DL create_shapes.py
import os
import shapes
import inputs


# Walks the user through creating a new shape step by step
# Asks for the shape type, a name, then the measurements needed for that shape
# Returns the finished shape object, or None if the user cancels at any point
def create_shape():
    os.system("cls")
    print("=" * 38)
    print("🆕 CREATE NEW SHAPE 🆕")
    print("=" * 38)
    print("Available Shapes:\n")
    print("[1] Circle ⭕")
    print("[2] Rectangle 📋")
    print("[3] Square ⬜")
    print("[4] Triangle 🔺")
    print("[r] Return\n")

    choice = inputs.get_menu_choice("Enter shape type (1-4): ", ['1', '2', '3', '4', 'r'])
    if choice == 'r':
        return None

    name = input("Name your shape (or 'r' to cancel): ").strip()
    if name.lower() == 'r' or name == '':
        return None

    if choice == '1':
        radius = inputs.get_positive_float("Enter radius (positive number): ")
        if radius is None:
            return None
        shape = shapes.Circle(radius, name)

    elif choice == '2':
        base = inputs.get_positive_float("Enter base (positive number): ")
        if base is None:
            return None
        height = inputs.get_positive_float("Enter height (positive number): ")
        if height is None:
            return None
        shape = shapes.Rectangle(base, height, name)

    elif choice == '3':
        side = inputs.get_positive_float("Enter side length (positive number): ")
        if side is None:
            return None
        shape = shapes.Square(side, name)

    elif choice == '4':
        # Keep asking for all three sides until they form a valid triangle
        while True:
            side1 = inputs.get_positive_float("Enter side 1 (positive number): ")
            if side1 is None:
                return None
            side2 = inputs.get_positive_float("Enter side 2 (positive number): ")
            if side2 is None:
                return None
            side3 = inputs.get_positive_float("Enter side 3 (positive number): ")
            if side3 is None:
                return None
            shape = shapes.Triangle(side1, side2, side3, name)
            if not shape.is_valid():
                print("❌ Those sides don't form a valid triangle.")
                print("   Each side must be less than the sum of the other two.")
                print("   Please try again.\n")
                continue
            break

    os.system("cls")
    print("\n✅ Shape created successfully!\n")
    shape.display()
    input("\nPress Enter to continue...")
    return shape