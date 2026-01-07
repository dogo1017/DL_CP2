import time

gravity = 1
air_res = 0.5
max_speed = 20
position = [0, 0]
x_vel = 0
y_vel = 0

# grav_dir[0] = Horizontal Gravity (-1: Left, 1: Right)
# grav_dir[1] = Vertical Gravity (-1: Up, 1: Down)
grav_dir = [0, 1] 

while True:
    
    x_vel += grav_dir[0] * gravity
    y_vel += grav_dir[1] * gravity


    if x_vel > 0:
        x_vel = max(0, x_vel - air_res)
    elif x_vel < 0:
        x_vel = min(0, x_vel + air_res)

    if y_vel > 0:
        y_vel = max(0, y_vel - air_res)
    elif y_vel < 0:
        y_vel = min(0, y_vel + air_res)


    if x_vel > max_speed: x_vel = max_speed
    if x_vel < -max_speed: x_vel = -max_speed
    if y_vel > max_speed: y_vel = max_speed
    if y_vel < -max_speed: y_vel = -max_speed

    position[0] += x_vel
    position[1] += y_vel

    print(f"Pos: {position} | Vel: [{x_vel}, {y_vel}]")
    time.sleep(0.1) 

    