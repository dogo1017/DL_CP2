import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dino Game") # Set a title for the window

# Create a player rectangle (x, y, width, height)
player = pygame.Rect(150, 500, 50, 50)
player_color = (0, 255, 0)

# Load the image
try:
    # IMPORTANT: Update this path to the actual location of your image file
    image_surface = pygame.image.load('DL_CP2/extra/dino_game_folder/standing_dino.jpg').convert_alpha()
    # Resize the image to fit the player rect size
    image_surface = pygame.transform.scale(image_surface, (player.width, player.height))
    use_image = True
except pygame.error:
    print("Warning: Could not load image. Using a colored rectangle instead.")
    use_image = False

# Game variables
velocity_y = 0 # Vertical velocity for jumping
gravity = 0.5
ground_y = 500
touching_ground = True
obstacles = []
obstacle_color = (255, 0, 0)
obstacle_speed = 5
SPAWN_CACTUS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_CACTUS_EVENT, 2000) # Spawn a cactus group every 2 seconds

clock = pygame.time.Clock()
running = True

def spawn_cactus_group():
    """Spawns a group of 1 to 3 cacti with random heights."""
    count = random.randint(1, 3) # Group size (1, 2, or 3 cacti)
    # Define possible cactus heights and widths
    cactus_configs = [(30, 40), (30, 60), (30, 80)]
    
    for i in range(count):
        width, height = random.choice(cactus_configs)
        # Spacing each cactus in the group by 35 pixels (width + padding)
        new_cactus = pygame.Rect(800 + (i * 35), ground_y + (50 - height), width, height)
        obstacles.append(new_cactus)

# Call the initial spawn function
spawn_cactus_group()
start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_CACTUS_EVENT:
            spawn_cactus_group()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and touching_ground:
                velocity_y = -12 # Jump velocity (negative goes up in Pygame)
                touching_ground = False
    
    

    # 1. Update Game Logic
    
    # Apply gravity and update player position
    player.y += velocity_y
    velocity_y += gravity

    # Ground collision detection
    if player.y >= ground_y:
        player.y = ground_y
        velocity_y = 0
        touching_ground = True

    # Update obstacle positions and remove off-screen obstacles
    for obstacle in obstacles[:]: # Iterate over a slice to safely remove elements
        obstacle.x -= obstacle_speed
        if obstacle.x + obstacle.width < 0:
            obstacles.remove(obstacle)

    # Collision Detection (Player vs Obstacles)
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            print("Game Over!")
            running = False # End the game loop

    # 2. Drawing
    screen.fill((255, 255, 255)) # Fill screen with white (standard dino game background)

    # Draw the player
    if use_image:
        # Update image position to match the rect's top-left corner
        screen.blit(image_surface, (player.x, player.y)) 
    else:
        pygame.draw.rect(screen, player_color, player)

    # Draw all obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle)

    # 3. Update the display
    pygame.display.flip()
    clock.tick(60) # 60 FPS
    

pygame.quit()
