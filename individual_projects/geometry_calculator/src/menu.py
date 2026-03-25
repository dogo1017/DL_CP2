import os
import inputs


def show_main_menu(shape_list):
    os.system("cls")
    print("=" * 38)
    print("📐 GEOMETRY CALCULATOR 📐")
    print("=" * 38)
    print("\nWelcome to the Shape Calculator!\n")
    print("=" * 38)
    print("🔷 MAIN MENU 🔷")
    print("=" * 38)
    print(f"Current Shapes: {len(shape_list)} created\n")
    print("📊 SHAPE LIBRARY:")
    print("┌─────────────────────────────────────┐")
    if len(shape_list) == 0:
        print("│ No shapes created yet               │")
        print("│ Create your first shape below!      │")
    else:
        for i, s in enumerate(shape_list):
            label = f"[{i+1}] {s.info()}"
            if len(label) > 36:
                label = label[:36]
            print(f"│ {label:<36}│")
            area_line = f"     Area: {s.area()} units²"
            perim_line = f"     Perimeter: {s.perimeter()} units"
            if len(area_line) > 36:
                area_line = area_line[:36]
            if len(perim_line) > 36:
                perim_line = perim_line[:36]
            print(f"│ {area_line:<36}│")
            print(f"│ {perim_line:<36}│")
    print("└─────────────────────────────────────┘\n")
    print("🎯 ACTIONS:")
    print("[1] Create New Shape")
    print("[2] View All Shapes")
    print("[3] Select Shape")
    print("[4] Compare Shapes")
    print("[5] Sort Shapes")
    print("[6] Formula Guide")
    print("[7] Quit\n")
    return inputs.get_menu_choice("Enter your choice (1-7): ", ['1','2','3','4','5','6','7'])


def view_all(shape_list):
    os.system("cls")
    if len(shape_list) == 0:
        print("No shapes created yet.")
    else:
        for s in shape_list:
            s.display()
            print()
    input("Press Enter to continue...")


def select_shape(shape_list):
    os.system("cls")
    if len(shape_list) == 0:
        print("No shapes to select.")
        input("Press Enter to continue...")
        return
    print("Select a shape:\n")
    for i, s in enumerate(shape_list):
        print(f"[{i+1}] {s.name}")
    print("[r] Return\n")
    valid = [str(i+1) for i in range(len(shape_list))] + ['r']
    choice = inputs.get_menu_choice("Enter choice: ", valid)
    if choice == 'r':
        return
    shape = shape_list[int(choice) - 1]
    os.system("cls")
    shape.display()
    input("\nPress Enter to continue...")


def compare_shapes(shape_list):
    os.system("cls")
    if len(shape_list) < 2:
        print("You need at least 2 shapes to compare.")
        input("Press Enter to continue...")
        return
    print("Choose shapes to compare:\n")
    for i, s in enumerate(shape_list):
        print(f"[{i+1}] {s.name}")
    print()
    valid = [str(i+1) for i in range(len(shape_list))]
    a = int(inputs.get_menu_choice("First shape: ", valid)) - 1
    b = int(inputs.get_menu_choice("Second shape: ", valid)) - 1
    s1 = shape_list[a]
    s2 = shape_list[b]
    os.system("cls")
    print("=" * 38)
    print(f"Comparing: {s1.name} vs {s2.name}")
    print("=" * 38 + "\n")
    print(f"  {s1.name:<18} area: {s1.area()} units²")
    print(f"  {s2.name:<18} area: {s2.area()} units²")
    if s1.area() > s2.area():
        print(f"  ➡ {s1.name} has the larger area.\n")
    elif s2.area() > s1.area():
        print(f"  ➡ {s2.name} has the larger area.\n")
    else:
        print(f"  ➡ Both shapes have equal area.\n")
    print(f"  {s1.name:<18} perimeter: {s1.perimeter()} units")
    print(f"  {s2.name:<18} perimeter: {s2.perimeter()} units")
    if s1.perimeter() > s2.perimeter():
        print(f"  ➡ {s1.name} has the longer perimeter.")
    elif s2.perimeter() > s1.perimeter():
        print(f"  ➡ {s2.name} has the longer perimeter.")
    else:
        print(f"  ➡ Both shapes have equal perimeter.")
    input("\nPress Enter to continue...")


def sort_shapes(shape_list):
    os.system("cls")
    if len(shape_list) == 0:
        print("No shapes to sort.")
        input("Press Enter to continue...")
        return
    print("Sort by:\n")
    print("[1] Area")
    print("[2] Perimeter\n")
    choice = inputs.get_menu_choice("Enter choice: ", ['1', '2'])
    if choice == '1':
        def area_key(s):
            return s.area()
        sorted_list = sorted(shape_list, key=area_key)
        label = "Area"
    else:
        def perim_key(s):
            return s.perimeter()
        sorted_list = sorted(shape_list, key=perim_key)
        label = "Perimeter"
    os.system("cls")
    print(f"Sorted by {label} (smallest to largest):\n")
    print("┌─────────────────────────────────────┐")
    for i, s in enumerate(sorted_list):
        line = f"[{i+1}] {s.name}"
        print(f"│ {line:<36}│")
        area_line = f"     Area: {s.area()} units²"
        perim_line = f"     Perimeter: {s.perimeter()} units"
        print(f"│ {area_line:<36}│")
        print(f"│ {perim_line:<36}│")
    print("└─────────────────────────────────────┘")
    input("\nPress Enter to continue...")


def formula_guide():
    os.system("cls")
    print("=" * 38)
    print("📘 FORMULA GUIDE 📘")
    print("=" * 38 + "\n")
    import shapes
    shapes.Circle(1,"").formula()
    print()
    shapes.Rectangle(1,1,"").formula()
    print()
    shapes.Square(1,"").formula()
    print()
    shapes.Triangle(1,1,1,"").formula()
    input("\nPress Enter to continue...")