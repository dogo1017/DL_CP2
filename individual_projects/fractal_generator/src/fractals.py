# Fractal Algorithms Module
# Contains the recursive math functions for the Triangle, Snowflake, and Tree
# Each function calls itself with a smaller 'depth' until it hits the base case of 0
import math

# Finds the middle point between two coordinates to help split triangles
def midpt(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

# Recursive Sierpinski Triangle: Splits a triangle into 3 smaller ones
def draw_sierpinski(t, pts, depth, max_depth, colors, fill_shape):
    # Determine color based on current recursion level
    c = colors[depth % len(colors)] if colors else "gray"
    
    # Draw the current triangle
    t.up()
    if fill_shape:
        t.color(c, c); t.begin_fill()
    else:
        t.color(c)
    t.goto(pts[0]); t.down()
    t.goto(pts[1]); t.goto(pts[2]); t.goto(pts[0])
    if fill_shape: t.end_fill()
        
    # Base case check: if we have depth left, split into 3 more triangles
    if depth > 0:
        m01 = midpt(pts[0], pts[1])
        m02 = midpt(pts[0], pts[2])
        m12 = midpt(pts[1], pts[2])
        draw_sierpinski(t, [pts[0], m01, m02], depth - 1, max_depth, colors, fill_shape)
        draw_sierpinski(t, [pts[1], m01, m12], depth - 1, max_depth, colors, fill_shape)
        draw_sierpinski(t, [pts[2], m02, m12], depth - 1, max_depth, colors, fill_shape)

# Recursive Koch Side: Breaks a straight line into a 'bumped' line segment
def koch_side(t, depth, length, colors, depth_level):
    if depth == 0:
        # Base case: actually draw the line once we stop recursing
        t.color(colors[depth_level % len(colors)] if colors else "white")
        t.down(); t.forward(length)
        return
        
    length = length / 3
    koch_side(t, depth - 1, length, colors, depth_level + 1)
    t.left(60)
    koch_side(t, depth - 1, length, colors, depth_level + 1)
    t.right(120)
    koch_side(t, depth - 1, length, colors, depth_level + 1)
    t.left(60)
    koch_side(t, depth - 1, length, colors, depth_level + 1)

# Recursive Fractal Tree: Draws a branch and then two smaller branches at the end
def draw_tree(t, x, y, angle, length, depth, colors):
    if depth == 0:
        return
        
    t.color(colors[depth % len(colors)] if colors else "white")
    t.pensize(max(1, depth))
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    t.up(); t.goto(x, y); t.down(); t.goto(x2, y2)

    # Call itself twice: once for a left branch and once for a right branch
    draw_tree(t, x2, y2, angle + 30, length * 0.7, depth - 1, colors)
    draw_tree(t, x2, y2, angle - 30, length * 0.7, depth - 1, colors)