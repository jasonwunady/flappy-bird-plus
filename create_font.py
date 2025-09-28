import pygame
import os

def create_pixel_font_surface(text, size, color):
    # Create a surface with doubled size and extra spacing between characters
    char_spacing = size // 3  # Add spacing between characters
    surface_width = (len(text) * (size + char_spacing))
    # Make the surface taller to accommodate the full character height
    surface_height = int(size * 1.2)  # Add 20% more height
    font_surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
    
    # Define pixel patterns for each character (improved visibility)
    pixels = {
        '0': [(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (4,3), (0,4), (4,4), (1,5), (2,5), (3,5)],
        '1': [(1,0), (2,0), (1,1), (2,1), (2,2), (2,3), (2,4), (1,5), (2,5), (3,5)],
        '2': [(1,0), (2,0), (3,0), (0,1), (4,1), (4,2), (3,3), (2,3), (1,4), (0,5), (1,5), (2,5), (3,5), (4,5)],
        '3': [(1,0), (2,0), (3,0), (4,1), (3,2), (2,2), (4,3), (4,4), (1,5), (2,5), (3,5)],
        '4': [(0,0), (4,0), (0,1), (4,1), (0,2), (4,2), (1,3), (2,3), (3,3), (4,3), (4,4), (4,5)],
        '5': [(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (0,2), (1,2), (2,2), (3,2), (4,3), (4,4), (0,5), (1,5), (2,5), (3,5)],
        '6': [(1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (3,2), (0,3), (4,3), (0,4), (4,4), (1,5), (2,5), (3,5)],
        '7': [(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (3,2), (2,3), (1,4), (1,5)],
        '8': [(1,0), (2,0), (3,0), (0,1), (4,1), (1,2), (2,2), (3,2), (0,3), (4,3), (0,4), (4,4), (1,5), (2,5), (3,5)],
        '9': [(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (1,3), (2,3), (3,3), (4,3), (4,4), (1,5), (2,5), (3,5)],
        'G': [(1,0), (2,0), (3,0), (0,1), (0,2), (0,3), (0,4), (1,5), (2,5), (3,5), (4,4), (4,3), (2,3), (3,3)],
        'A': [(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (1,3), (2,3), (3,3), (4,3), (0,4), (4,4), (0,5), (4,5)],
        'M': [(0,0), (4,0), (0,1), (1,1), (3,1), (4,1), (0,2), (2,2), (4,2), (0,3), (4,3), (0,4), (4,4), (0,5), (4,5)],
        'E': [(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5)],
        'O': [(1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (4,3), (0,4), (4,4), (1,5), (2,5), (3,5)],
        'V': [(0,0), (4,0), (0,1), (4,1), (0,2), (4,2), (1,3), (3,3), (1,4), (3,4), (2,5)],
        'R': [(0,0), (1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (1,3), (2,3), (3,3), (0,4), (2,4), (0,5), (3,5)],
        'S': [(1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (3,2), (4,3), (4,4), (1,5), (2,5), (3,5)],
        'P': [(0,0), (1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (1,3), (2,3), (3,3), (0,4), (0,5)],
        'C': [(1,0), (2,0), (3,0), (0,1), (0,2), (0,3), (0,4), (1,5), (2,5), (3,5)],
        'L': [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5)],
        'Y': [(0,0), (4,0), (0,1), (4,1), (1,2), (3,2), (2,3), (2,4), (2,5)],
        ' ': [],
        'T': [(0,0), (1,0), (2,0), (3,0), (4,0), (2,1), (2,2), (2,3), (2,4), (2,5)],
        'F': [(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4), (0,5)],
        'I': [(1,0), (2,0), (3,0), (2,1), (2,2), (2,3), (2,4), (1,5), (2,5), (3,5)],
        'U': [(0,0), (4,0), (0,1), (4,1), (0,2), (4,2), (0,3), (4,3), (0,4), (4,4), (1,5), (2,5), (3,5)],
        'K': [(0,0), (4,0), (0,1), (3,1), (0,2), (2,2), (0,3), (2,3), (0,4), (3,4), (0,5), (4,5)],
        'N': [(0,0), (4,0), (0,1), (1,1), (4,1), (0,2), (2,2), (4,2), (0,3), (3,3), (4,3), (0,4), (4,4), (0,5), (4,5)],
        'D': [(0,0), (1,0), (2,0), (3,0), (0,1), (4,1), (0,2), (4,2), (0,3), (4,3), (0,4), (4,4), (0,5), (1,5), (2,5), (3,5)]
    }
    
    # Draw each character
    x_offset = 0
    for char in text.upper():
        if char in pixels:
            for px, py in pixels[char]:
                # Draw each pixel as a 2x2 square for better visibility
                pygame.draw.rect(font_surface, color, (x_offset + px * 2, py * 2, 2, 2))
        x_offset += size + char_spacing  # Add spacing between characters
    
    return font_surface

def main():
    pygame.init()
    
    # Ensure fonts directory exists
    fonts_dir = 'fonts'
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    
    # Create number sprites (0-9) - bigger size for score
    number_size = 24  # Keep numbers big for score
    for i in range(10):
        number = create_pixel_font_surface(str(i), number_size, (255, 255, 255))
        # Scale up the surface to make pixels more visible
        scaled = pygame.transform.scale(number, (number_size * 2, number_size * 2))
        pygame.image.save(scaled, os.path.join(fonts_dir, f'number_{i}.png'))
    
    # Create text for "Game Over" and instructions - smaller size for better fit
    text_size = 10  # Smaller text size to fit screen
    game_over = create_pixel_font_surface("GAME OVER", text_size, (255, 255, 255))
    press_text1 = create_pixel_font_surface("PRESS UP OR", text_size, (255, 255, 255))
    press_text2 = create_pixel_font_surface("SPACE KEY", text_size, (255, 255, 255))
    press_text3 = create_pixel_font_surface("OR TAP", text_size, (255, 255, 255))
    
    # Scale up the text surfaces with smaller scaling factor
    game_over = pygame.transform.scale(game_over, (game_over.get_width() * 1.2, game_over.get_height() * 1.2))
    press_text1 = pygame.transform.scale(press_text1, (press_text1.get_width() * 1.2, press_text1.get_height() * 1.2))
    press_text2 = pygame.transform.scale(press_text2, (press_text2.get_width() * 1.2, press_text2.get_height() * 1.2))
    press_text3 = pygame.transform.scale(press_text3, (press_text3.get_width() * 1.2, press_text3.get_height() * 1.2))
    
    # Save all text images
    pygame.image.save(game_over, os.path.join(fonts_dir, 'game_over.png'))
    pygame.image.save(press_text1, os.path.join(fonts_dir, 'press_space_1.png'))
    pygame.image.save(press_text2, os.path.join(fonts_dir, 'press_space_2.png'))
    pygame.image.save(press_text3, os.path.join(fonts_dir, 'press_space_3.png'))
    
    # Save all text images
    pygame.image.save(game_over, os.path.join(fonts_dir, 'game_over.png'))
    pygame.image.save(press_text1, os.path.join(fonts_dir, 'press_space_1.png'))
    pygame.image.save(press_text2, os.path.join(fonts_dir, 'press_space_2.png'))
    
    pygame.quit()

if __name__ == '__main__':
    main()