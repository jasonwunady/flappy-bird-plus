import pygame
import os

def create_bird():
    surface = pygame.Surface((34, 24), pygame.SRCALPHA)
    
    # Softer yellow for the body
    pygame.draw.ellipse(surface, (255, 223, 128), (0, 0, 34, 24))  # Main body
    
    # Rosy cheeks (slight pink circles)
    pygame.draw.circle(surface, (255, 200, 200), (8, 14), 4)  # Left cheek
    pygame.draw.circle(surface, (255, 200, 200), (22, 14), 4)  # Right cheek
    
    # Bigger, cuter eyes with white reflection
    pygame.draw.circle(surface, (0, 0, 0), (10, 10), 4)        # Left eye outline
    pygame.draw.circle(surface, (0, 0, 0), (20, 10), 4)        # Right eye outline
    pygame.draw.circle(surface, (255, 255, 255), (10, 10), 3)  # Left eye
    pygame.draw.circle(surface, (255, 255, 255), (20, 10), 3)  # Right eye
    pygame.draw.circle(surface, (0, 0, 0), (10, 10), 2)        # Left pupil
    pygame.draw.circle(surface, (0, 0, 0), (20, 10), 2)        # Right pupil
    pygame.draw.circle(surface, (255, 255, 255), (11, 9), 1)   # Left eye highlight
    pygame.draw.circle(surface, (255, 255, 255), (21, 9), 1)   # Right eye highlight
    
    # Small orange beak
    pygame.draw.polygon(surface, (255, 165, 0), [(15, 14), (19, 14), (17, 18)])
    
    # Add a little wing
    pygame.draw.ellipse(surface, (255, 200, 100), (5, 12, 10, 8))
    
    return surface

def create_pipe():
    surface = pygame.Surface((52, 320), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 255, 0), (0, 0, 52, 320))      # Green pipe
    pygame.draw.rect(surface, (0, 200, 0), (0, 0, 52, 20))       # Darker top
    pygame.draw.rect(surface, (0, 200, 0), (0, 300, 52, 20))     # Darker bottom
    return surface

def create_background():
    surface = pygame.Surface((288, 512))
    # Sky gradient
    for y in range(512):
        color = (135 - y//10, 206 - y//10, 235 - y//10)
        pygame.draw.line(surface, color, (0, y), (288, y))
    # Ground
    pygame.draw.rect(surface, (150, 75, 0), (0, 400, 288, 112))
    pygame.draw.rect(surface, (0, 154, 0), (0, 400, 288, 20))
    return surface

def main():
    pygame.init()
    
    # Ensure assets directory exists
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Create and save assets
    bird = create_bird()
    pygame.image.save(bird, os.path.join(assets_dir, 'bird.png'))
    
    pipe = create_pipe()
    pygame.image.save(pipe, os.path.join(assets_dir, 'pipe.png'))
    
    background = create_background()
    pygame.image.save(background, os.path.join(assets_dir, 'background.png'))
    
    pygame.quit()

if __name__ == '__main__':
    main()