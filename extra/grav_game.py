import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Cube")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

gravity = 1
air_res = 0.05
max_speed = 15
friction = 0.1
bounce = -1.5

position = [WIDTH // 2, 50]
x_vel = 0
y_vel = 0
grav_dir = [0, 1]

cube_size = 30
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        grav_dir[0], grav_dir[1] = 0, -1
    if keys[pygame.K_s]:
        grav_dir[0], grav_dir[1] = 0, 1
    if keys[pygame.K_a]:
        grav_dir[0], grav_dir[1] = -1, 0
    if keys[pygame.K_d]:
        grav_dir[0], grav_dir[1] = 1, 0

    x_vel += grav_dir[0] * gravity
    y_vel += grav_dir[1] * gravity

    x_vel *= (1 - air_res)
    y_vel *= (1 - air_res)

    x_vel = max(-max_speed, min(max_speed, x_vel))
    y_vel = max(-max_speed, min(max_speed, y_vel))

    position[0] += x_vel
    position[1] += y_vel

    on_ground = False
    
    if position[1] + cube_size > HEIGHT:
        position[1] = HEIGHT - cube_size
        y_vel = y_vel/bounce
        on_ground = True
    elif position[1] < 0:
        position[1] = 0
        y_vel = y_vel/bounce
        on_ground = True
        
    if position[0] + cube_size > WIDTH:
        position[0] = WIDTH - cube_size
        x_vel = y_vel/bounce
        on_ground = True
    elif position[0] < 0:
        position[0] = 0
        x_vel = y_vel/bounce
        on_ground = True

    if on_ground:
        if grav_dir[1] != 0:
            if x_vel > 0: x_vel = max(0, x_vel - friction)
            elif x_vel < 0: x_vel = min(0, x_vel + friction)
        if grav_dir[0] != 0:
            if y_vel > 0: y_vel = max(0, y_vel - friction)
            elif y_vel < 0: y_vel = min(0, y_vel + friction)

    screen.fill(WHITE)
    cube = pygame.Rect(int(position[0]), int(position[1]), cube_size, cube_size)
    pygame.draw.rect(screen, BLUE, cube)
    pygame.display.flip()
    clock.tick(60)
