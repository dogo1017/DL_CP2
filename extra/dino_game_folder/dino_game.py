import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dino Game")
screen_width, screen_height = 800, 600
player = pygame.Rect(150, 500, 50, 50)
player_color = (0, 255, 0)

def load_image(name, scale=None):
    try:
        image = pygame.image.load(os.path.join(name)).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        surf = pygame.Surface((30, 50))
        surf.fill((255, 0, 0))
        return surf

small_cacti = [load_image(f'small{i}.png') for i in range(1, 7)]
large_cacti = [load_image(f'large{i}.png') for i in range(1, 7)]
ground = load_image('ground.png')
font_imgs = [load_image(f'{i}.png') for i in range(0, 10)]
hi_img = load_image('hi.png')

use_image = False
image_surface_standing = None
image_surface_run1 = None
image_surface_run2 = None
current_image = None

try:
    image_surface_standing = load_image('standing_dino.jpg', (player.width, player.height))
    image_surface_run1 = load_image('running1.png', (player.width, player.height))
    image_surface_run2 = load_image('running2.png', (player.width, player.height))
    current_image = image_surface_run1
    use_image = True
except:
    use_image = False

velocity_y = 0
gravity = 0.5
ground_y = 500
obstacles = []
speed = 4

SPAWN_CACTUS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CACTUS_EVENT, 1500)
ANIMATION_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ANIMATION_EVENT, 100)

start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()
running = True

def spawn_cactus_group():
    count = random.randint(1, 3)
    sizes = {"small": (30, 40), "large": (40, 60)}
    for i in range(count):
        is_large = random.choice([True, False])
        if is_large:
            size = sizes["large"]
            img = random.choice(large_cacti)
        else:
            size = sizes["small"]
            img = random.choice(small_cacti)
        img = pygame.transform.scale(img, size)
        new_rect = pygame.Rect(800 + (i * 50), ground_y + (50 - size[1]), size[0], size[1])
        obstacles.append({'rect': new_rect, 'image': img})

spawn_cactus_group()

ground_scaled = pygame.transform.scale(ground, (2400, 20))
ground_width = ground_scaled.get_width()
ground_x1 = 0
ground_x2 = ground_width


while running:
    dig1, dig2, dig3, dig4, dig5 = 0, 0, 0, 0, 0
    score_time = (pygame.time.get_ticks() - start_ticks) // 100

    speed *= 1.001

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_CACTUS_EVENT:
            spawn_cactus_group()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.y >= ground_y:
                velocity_y = -13
                if use_image:
                    current_image = image_surface_standing
        elif event.type == ANIMATION_EVENT:
            if use_image and player.y >= ground_y:
                if current_image == image_surface_run1:
                    current_image = image_surface_run2
                else:
                    current_image = image_surface_run1

    player.y += velocity_y
    velocity_y += gravity
    if player.y >= ground_y + 5:
        player.y = ground_y + 5
        velocity_y = 0

    ground_x1 -= speed
    ground_x2 -= speed

    if ground_x1 + ground_width < 0:
        ground_x1 = ground_x2 + ground_width

    if ground_x2 + ground_width < 0:
        ground_x2 = ground_x1 + ground_width


    for obs in obstacles[:]:
        obs['rect'].x -= speed
        if obs['rect'].x + obs['rect'].width < 0:
            obstacles.remove(obs)
        if player.colliderect(obs['rect']):
            running = False

    screen.fill((255, 255, 255))

    screen.blit(ground_scaled, (ground_x1, 548))
    screen.blit(ground_scaled, (ground_x2, 548))
  
    score_str = str(score_time).zfill(5)
    for i, num in enumerate(score_str):
        exec(f"dig{i+1} = int(num)")
    screen.blit(pygame.transform.scale(font_imgs[dig1], (20, 20)), (700, 20))
    screen.blit(pygame.transform.scale(font_imgs[dig2], (20, 20)), (720, 20))
    screen.blit(pygame.transform.scale(font_imgs[dig3], (20, 20)), (740, 20))
    screen.blit(pygame.transform.scale(font_imgs[dig4], (20, 20)), (760, 20))
    screen.blit(pygame.transform.scale(font_imgs[dig5], (20, 20)), (780, 20))
    screen.blit(pygame.transform.scale(hi_img, (20, 20)), (680, 20))

    if use_image:
        screen.blit(current_image, player.topleft)
    else:
        pygame.draw.rect(screen, (0, 255, 0), player)

    for obs in obstacles:
        screen.blit(obs['image'], obs['rect'].topleft)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
