import pygame
import os

def create_bird_frame(wing_position):
    # Create a larger surface to ensure wing animations fit
    surface = pygame.Surface((34, 24), pygame.SRCALPHA)
    
    # Main body - classic Flappy Bird orange-red color
    pygame.draw.ellipse(surface, (241, 85, 51), (6, 4, 24, 16))  # Main body, slightly smaller and centered
    
    # White chest/belly area
    pygame.draw.ellipse(surface, (255, 255, 255), (12, 12, 14, 8))
    
    # Simple black eye - slightly larger and fully black
    pygame.draw.ellipse(surface, (0, 0, 0), (24, 8, 5, 5))  # Made the eye a bit larger
    
    # Wing colors
    wing_color = (241, 85, 51)  # Same as body
    wing_highlight = (251, 105, 71)  # Slightly lighter
    wing_shadow = (221, 65, 31)  # Slightly darker
    
    # Wing positions
    if wing_position == 'up':
        # Wing up position
        pygame.draw.ellipse(surface, wing_shadow, (4, 4, 10, 8))  # Wing base
        pygame.draw.ellipse(surface, wing_color, (5, 5, 8, 6))  # Middle layer
        pygame.draw.ellipse(surface, wing_highlight, (6, 6, 6, 4))  # Top highlight
        points = [(4, 8), (2, 6), (4, 4)]  # Wing tip feathers
    elif wing_position == 'middle':
        # Wing middle position
        pygame.draw.ellipse(surface, wing_shadow, (4, 8, 10, 8))  # Wing base
        pygame.draw.ellipse(surface, wing_color, (5, 9, 8, 6))  # Middle layer
        pygame.draw.ellipse(surface, wing_highlight, (6, 10, 6, 4))  # Top highlight
        points = [(4, 12), (2, 10), (4, 8)]  # Wing tip feathers
    else:  # down
        # Wing down position
        pygame.draw.ellipse(surface, wing_shadow, (4, 12, 10, 8))  # Wing base
        pygame.draw.ellipse(surface, wing_color, (5, 13, 8, 6))  # Middle layer
        pygame.draw.ellipse(surface, wing_highlight, (6, 14, 6, 4))  # Top highlight
        points = [(4, 16), (2, 14), (4, 12)]  # Wing tip feathers
    
    pygame.draw.polygon(surface, wing_shadow, points)  # Draw wing tip feathers
    return surface

def create_bird():
    # Create three frames of animation
    bird_up = create_bird_frame('up')
    bird_middle = create_bird_frame('middle')
    bird_down = create_bird_frame('down')
    
    return [bird_up, bird_middle, bird_down]  # Return all frames
    
    return surface

def create_pipe():
    surface = pygame.Surface((52, 320), pygame.SRCALPHA)
    
    # Classic Flappy Bird green color
    pipe_color = (96, 176, 72)  # Bright green
    cap_color = (76, 156, 52)   # Darker green for the cap
    
    # Main pipe body
    pygame.draw.rect(surface, pipe_color, (0, 0, 52, 320))
    
    # Pipe cap (top and bottom)
    pygame.draw.rect(surface, cap_color, (0, 0, 52, 20))    # Top cap
    pygame.draw.rect(surface, cap_color, (0, 300, 52, 20))  # Bottom cap
    
    return surface

def create_background():
    surface = pygame.Surface((288, 512))
    
    # Classic light blue sky
    surface.fill((99, 185, 255))
    
    # Ground
    pygame.draw.rect(surface, (221, 216, 148), (0, 400, 288, 112))  # Tan ground
    
    return surface

def main():
    pygame.init()
    
    # Ensure assets directory exists
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Create and save assets
    bird_frames = create_bird()
    pygame.image.save(bird_frames[0], os.path.join(assets_dir, 'bird_up.png'))
    pygame.image.save(bird_frames[1], os.path.join(assets_dir, 'bird_middle.png'))
    pygame.image.save(bird_frames[2], os.path.join(assets_dir, 'bird_down.png'))
    
    pipe = create_pipe()
    pygame.image.save(pipe, os.path.join(assets_dir, 'pipe.png'))
    
    background = create_background()
    pygame.image.save(background, os.path.join(assets_dir, 'background.png'))
    
    pygame.quit()

if __name__ == '__main__':
    main()