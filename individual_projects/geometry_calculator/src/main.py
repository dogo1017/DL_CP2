#DL 1st, main 

import shapes

def main():

    with open("individual_projects\geometry_calculator\docs\shapes.csv", 'r') as f:
        line_count = sum(1 for line in f)
        
    print('='*38)
    print("📐 GEOMETRY CALCULATOR 📐")
    print('='*38)
    print("\nWelcome to the Shape Calculator!\n")
    print('='*38)
    print("🔷 MAIN MENU 🔷")
    print('='*38)
    print(f"Current Shapes: {line_count} created")

main()