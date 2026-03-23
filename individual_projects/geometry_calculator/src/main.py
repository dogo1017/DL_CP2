#DL 1st, main 
import shapes
import menu
import create_shapes

try:
    shape_count = 0
    with open("individual_projects/geometry_calculator/docs/shapes.csv", 'r') as f:
        shapes = [line.strip() for line in f if line.strip()]
        line_count = len(shapes)
            
except:
    line_count = 0
    with open("individual_projects/geometry_calculator/docs/shapes.csv", 'w') as f:
        pass

def main():
    user_inp = menu_input(menu.create_menu(line_count), [1,2,3,4,5,6,7])
    if user_inp == 1:
        create_shapes.create_shape()
main()