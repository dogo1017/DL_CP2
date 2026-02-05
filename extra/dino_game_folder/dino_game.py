import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
# Create a player rectangle (x, y, width, height)
player = pygame.Rect(350, 500, 50, 50) 
# Create an obstacle
obstacle = pygame.Rect(900, 500, 50, 50)

clock = pygame.time.Clock()
"""
image_surface = pygame.image.load('DL_CP2/extra/dino_game_folder/unnamed.png').convert_alpha()
image_rect = image_surface.get_rect()
image_rect.center = (800 // 2, 600 // 2) # Position the image
screen.blit(image_surface, image_rect)
"""

velocity = 0
running = True
touching_ground = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    obstacle.x -= 5
    
    keys = pygame.key.get_pressed()
    if touching_ground:
        if keys[pygame.K_SPACE]: 
            velocity = -12  # Use = to assign, and negative to go UP

    player.y += velocity    # Apply velocity to the player's position

    # Collision Detection
    if player.y >= 500:
        player.y = 500
        velocity = 0        # Stop moving when hitting the ground
        touching_ground = True
    else:
        touching_ground = False
        velocity += 0.5
    # Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), player) # Draw player
    pygame.draw.rect(screen, (255, 0, 0), obstacle) # Draw obstacle
    pygame.display.flip()
    clock.tick(60) # 60 FPS

pygame.quit()
