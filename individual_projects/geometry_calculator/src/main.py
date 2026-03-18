#DL 1st, main 

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
def main():
    print('='*38)
    print("📐 GEOMETRY CALCULATOR 📐")
    print('='*38)
    print("\nWelcome to the Shape Calculator!\n")
    print('='*38)
    print("🔷 MAIN MENU 🔷")
    print('='*38)
    print(f"Current Shapes: {line_count} created")
    print("┌─────────────────────────────────────┐")
    for i in range(line_count):
        print(f"| {shapes[i]}" + " "*(36-len(shapes[i])) + "|")
    print("└─────────────────────────────────────┘")

main()