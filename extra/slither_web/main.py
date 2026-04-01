import asyncio
import pygame

async def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    while True:
        screen.fill((0, 255, 0)) # Should show a green screen
        pygame.display.update()
        await asyncio.sleep(0) # Mandatory!

asyncio.run(main())
