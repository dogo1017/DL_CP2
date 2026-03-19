#DL 1st, main 

import dog_inp
import shapes

try:
    shape_count = 0
    with open("individual_projects/geometry_calculator/docs/shapes.csv", 'r') as f:
        shapes = [line.strip() for line in f if line.strip()]
        line_count = len(shapes)
            
except:
    line_count = 0
    with open("individual_projects/geometry_calculator/docs/shapes.csv", 'w') as f:
        pass

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

def create_shape(text):
    def create_circle():
        user_inp = dog_inp.menu(["Name","Return"],writable=[1])
        if user_inp.get("index") == 1: 
            create_shape(text)
            return
        

    user_inp = dog_inp.menu(["Circle⭕","Rectangle📋","Square⬜","Triangle🔺","Return"],heading=text).get("index")

    if user_inp == 0:
        create_circle()



def main():
    user_inp = dog_inp.menu(["Create New Shape","View All Shapes","Select Shape","Compare Shapes","Sort Shapes","Formula Guide","Quit"], heading=output)
    user_inp = user_inp.get("index")
    if user_inp == 0:
        create_shape(create_menu)

        
main()