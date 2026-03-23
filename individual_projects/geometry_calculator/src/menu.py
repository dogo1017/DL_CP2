
def create_menu(line_count,shapes):
    output = ""
    output += "=" * 38 + "\n"
    output += "📐 GEOMETRY CALCULATOR 📐\n"
    output += "=" * 38 + "\n"
    output += "\nWelcome to the Shape Calculator!\n\n"
    output += "=" * 38 + "\n"
    output += "🔷 MAIN MENU 🔷\n"
    output += "=" * 38 + "\n"
    output += f"Current Shapes: {line_count} created\n\n"
    output += "📊 SHAPE LIBRARY:\n"
    output += "┌─────────────────────────────────────┐\n"
    if line_count > 0:
        for i in range(line_count):
            output += f"|{shapes[i]}" + (" " * (36 - len(shapes[i]))) + "|\n"
    else:
        output += "| No shapes created yet               |\n"
        output += "| Create your first shape below!      |\n"
    output += "└─────────────────────────────────────┘"
    print(output)

    create_menu = ""
    create_menu += "=" * 38 + "\n"
    create_menu += "🆕 CREATE NEW SHAPE 🆕\n"
    create_menu += "=" * 38 + "\n"
    create_menu += "Available Shapes:\n"