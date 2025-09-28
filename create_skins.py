
import pygame
import os

# Initialize Pygame
pygame.init()
pygame.display.set_mode((1, 1))  # Create a minimal display

# Define the skin colors (R,G,B)
SKIN_COLORS = {
    'blue': (66, 135, 245),   # Blue bird
    'red': (245, 66, 66),     # Red bird
    'golden': (255, 215, 0)   # Golden bird
}

def create_colored_skin(original_image, color):
    # Create a copy of the original image
    colored = original_image.copy()

    # Get the dimensions of the image
    width, height = colored.get_size()

    # Go through each pixel
    for x in range(width):
        for y in range(height):
            pixel = colored.get_at((x, y))
            # Skip fully transparent pixels
            if pixel[3] == 0:  # Fully transparent
                continue

            # Recolor any non-black, non-transparent pixels (bird body)
            # This includes yellow, orange, and other colored parts
            if pixel[0] > 50 and pixel[1] > 50 and pixel[2] > 50:  # Not too dark
                # Calculate brightness to maintain shading
                brightness = (pixel[0] + pixel[1] + pixel[2]) / 3 / 255

                # Apply the new color with brightness preserved
                new_color = (
                    int(color[0] * brightness),
                    int(color[1] * brightness),
                    int(color[2] * brightness),
                    pixel[3]  # Keep original alpha
                )
                colored.set_at((x, y), new_color)

    return colored

def main():
    # Load original bird images
    positions = ['up', 'middle', 'down']
    original_images = {
        pos: pygame.image.load(f'assets/bird_{pos}.png').convert_alpha()
        for pos in positions
    }
    
    # Create skins directory if it doesn't exist
    skins_dir = 'assets/skins'
    if not os.path.exists(skins_dir):
        os.makedirs(skins_dir)
    
    # Create colored versions for each skin
    for skin_name, color in SKIN_COLORS.items():
        for pos in positions:
            colored = create_colored_skin(original_images[pos], color)
            # Save the colored skin
            pygame.image.save(colored, f'{skins_dir}/bird_{skin_name}_{pos}.png')
            print(f'Created {skin_name} bird {pos} position')

if __name__ == '__main__':
    main()
    print("All skins created successfully!")