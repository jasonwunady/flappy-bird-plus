import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game States
from enum import Enum
class GameState(Enum):
    HOME = 1
    PLAYING = 2
    GAME_OVER = 3
    SHOP = 4
    CONFIRM_RESET = 5
    BACKGROUND_SHOP = 6
    POWER_SHOP = 7
    PARTICLES_SHOP = 8

# Difficulty Settings
class Difficulty:
    EASY = {
        'gap': 150,
        'speed': 2,
        'name': 'EASY'
    }
    NORMAL = {
        'gap': 120,
        'speed': 2.5,
        'name': 'NORMAL'
    }
    HARD = {
        'gap': 90,
        'speed': 3,
        'name': 'HARD'
    }

# Game Constants
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 0.25
FLAP_POWER = -5
PIPE_SPACING = 200  # Horizontal distance between pipes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.images = []  # Will store all animation frames
        self.rect = pygame.Rect(x, y, 34, 24)  # Default size, will update with actual image
        self.animation_timer = 0
        self.animation_speed = 0.2  # Seconds per frame
        self.current_frame = 1  # Start with middle frame
        self.animation_sequence = [0, 1, 2, 1]  # Up, middle, down, middle
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()

    def flap(self):
        self.velocity = FLAP_POWER

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y
        
        # Update wing animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:  # Convert to milliseconds
            self.animation_index = (self.animation_index + 1) % len(self.animation_sequence)
            self.current_frame = self.animation_sequence[self.animation_index]
            self.last_update = current_time

    def draw(self, screen):
        if self.images:
            screen.blit(self.images[self.current_frame], self.rect)
        else:
            # Temporary rectangle for testing
            pygame.draw.rect(screen, (255, 255, 0), self.rect)

class Particle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.life = 1.0  # Life from 1.0 to 0.0
        self.age = 0.0

        # Set particle properties based on type
        if particle_type == 'stars':
            self.velocity_x = random.uniform(-1, 1)
            self.velocity_y = random.uniform(-1, 1)
            self.size = random.randint(2, 4)
            self.color = (255, 255, random.randint(150, 255))  # White to yellow stars
            self.decay_rate = 0.02
        elif particle_type == 'fire':
            self.velocity_x = random.uniform(-0.5, 0.5)
            self.velocity_y = random.uniform(-2, 0)
            self.size = random.randint(3, 6)
            self.color = (255, random.randint(100, 150), 0)  # Orange to red fire
            self.decay_rate = 0.03
        elif particle_type == 'sparkles':
            self.velocity_x = random.uniform(-1.5, 1.5)
            self.velocity_y = random.uniform(-1.5, 1.5)
            self.size = random.randint(1, 3)
            colors = [(255, 192, 203), (138, 43, 226), (0, 255, 255), (255, 255, 0)]  # Pink, purple, cyan, yellow
            self.color = random.choice(colors)
            self.decay_rate = 0.025
        elif particle_type == 'rainbow':
            self.velocity_x = random.uniform(-0.8, 0.8)
            self.velocity_y = random.uniform(-0.8, 0.8)
            self.size = random.randint(2, 5)
            # Rainbow colors based on age
            self.base_hue = random.uniform(0, 360)
            self.decay_rate = 0.015

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.age += 0.016  # Approximately 60 FPS
        self.life -= self.decay_rate

        # Update rainbow color
        if self.particle_type == 'rainbow':
            import colorsys
            hue = (self.base_hue + self.age * 100) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

        return self.life > 0

    def draw(self, screen):
        if self.life > 0:
            # Apply alpha based on life remaining
            alpha = max(0, min(255, int(self.life * 255)))
            color_with_alpha = (*self.color, alpha)

            # Create a surface for the particle with alpha
            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))

class Pipe:
    def __init__(self, x, difficulty, pipe_height=320):  # Default height if image not loaded
        self.x = x
        self.pipe_height = pipe_height
        self.set_difficulty(difficulty)
        self.passed = False
        self.image_top = None
        self.image_bottom = None
    
    def set_difficulty(self, difficulty):
        """Update pipe properties based on difficulty"""
        self.difficulty = difficulty
        self.speed = difficulty['speed']
        self.gap = difficulty['gap']
        # Calculate positions for pipes
        self.gap_y = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        
        # Store positions for collision detection
        self.top_pipe = pygame.Rect(self.x, self.gap_y - self.pipe_height, 52, self.pipe_height)
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + self.gap, 52, self.pipe_height)

    def update(self):
        self.x -= self.speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self, screen):
        if self.image_top and self.image_bottom:
            # Draw top pipe
            screen.blit(self.image_top, (self.x, self.gap_y - self.pipe_height))
            # Draw bottom pipe
            screen.blit(self.image_bottom, (self.x, self.gap_y + self.gap))
        else:
            # Temporary rectangles for testing
            pygame.draw.rect(screen, (0, 255, 0), self.top_pipe)
            pygame.draw.rect(screen, (0, 255, 0), self.bottom_pipe)

class Game:
    def __init__(self):
        self.bird = Bird(50, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.coins = 0
        self.total_coins = 0  # Total coins across all games
        self.state = GameState.HOME
        self.difficulty = Difficulty.NORMAL  # Default difficulty
        self.background = None  # Will be loaded later
        self.current_skin = 'default'  # Current bird skin
        self.owned_skins = {'default': True}  # Skins the player owns
        
        # Define available skins and their prices
        self.available_skins = {
            'default': {'price': 0, 'name': 'Default'},
            'blue': {'price': 50, 'name': 'Blue Bird'},
            'red': {'price': 100, 'name': 'Red Bird'},
            'golden': {'price': 200, 'name': 'Golden Bird'}
        }

        # Background system
        self.current_background = 'default'
        self.owned_backgrounds = {'default': True}
        self.available_backgrounds = {
            'default': {'price': 0, 'name': 'Sky Blue', 'color': (135, 206, 235)},
            'sunset': {'price': 75, 'name': 'Sunset', 'color': (255, 140, 0)},
            'night': {'price': 100, 'name': 'Night Sky', 'color': (25, 25, 112)},
            'forest': {'price': 150, 'name': 'Forest', 'color': (34, 139, 34)},
            'ocean': {'price': 125, 'name': 'Ocean', 'color': (0, 100, 140)}
        }

        # Superpower system
        self.owned_powers = set()
        self.available_powers = {
            'pipe_destroyer': {
                'price': 200,
                'name': 'Pipe Destroyer',
                'description': 'Press X to destroy all pipes!',
                'cooldown': 10.0,  # 10 seconds
                'key': pygame.K_x
            },
            'shield': {
                'price': 300,
                'name': 'Shield',
                'description': 'Press Z for 3 seconds of invincibility!',
                'cooldown': 15.0,  # 15 seconds
                'key': pygame.K_z,
                'duration': 3.0
            }
        }

        # Particle system
        self.current_particle = 'none'
        self.owned_particles = {'none': True}
        self.available_particles = {
            'none': {'price': 0, 'name': 'None'},
            'stars': {'price': 80, 'name': 'Starry Trail'},
            'fire': {'price': 120, 'name': 'Fire Trail'},
            'sparkles': {'price': 150, 'name': 'Magic Sparkles'},
            'rainbow': {'price': 200, 'name': 'Rainbow Trail'}
        }
        self.particles = []  # Active particles list
        self.power_cooldowns = {}  # Track cooldown timers for each power
        self.shield_active = False
        self.shield_timer = 0.0

        # Pixel font assets
        self.number_sprites = {}
        self.game_over_text = None
        self.press_space_text = None
        
                # Initialize sound system
        pygame.mixer.init()
        self.wing_sound = None
        self.background_music = None
        
        # Cloud animation system
        self.clouds = []
        self.cloud_timer = 0
        self.cloud_sprites = {}  # Pre-created cloud sprites
        self.create_cloud_sprites()
        self.init_clouds()

        # Load save data from file
        self.load_save_data()

        self.load_assets()
        self.reset_game()
    
    def load_save_data(self):
        import json
        try:
            with open('save_data.json', 'r') as f:
                data = json.load(f)
                self.high_score = data.get('high_scores', {
                    'EASY': 0,
                    'NORMAL': 0,
                    'HARD': 0
                })
                self.total_coins = data.get('coins', 0)
                self.owned_skins = data.get('owned_skins', {'default': True})
                self.current_skin = data.get('current_skin', 'default')
                self.owned_backgrounds = data.get('owned_backgrounds', {'default': True})
                self.current_background = data.get('current_background', 'default')
                self.owned_powers = set(data.get('owned_powers', []))
                self.owned_particles = data.get('owned_particles', {'none': True})
                self.current_particle = data.get('current_particle', 'none')
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = {
                'EASY': 0,
                'NORMAL': 0,
                'HARD': 0
            }
            self.total_coins = 0
            self.owned_skins = {'default': True}
            self.current_skin = 'default'
            self.owned_backgrounds = {'default': True}
            self.current_background = 'default'
            self.owned_powers = set()
            self.owned_particles = {'none': True}
            self.current_particle = 'none'
    
    def save_game_data(self):
        import json
        with open('save_data.json', 'w') as f:
            json.dump({
                'high_scores': self.high_score,
                'coins': self.total_coins,
                'owned_skins': self.owned_skins,
                'current_skin': self.current_skin,
                'owned_backgrounds': self.owned_backgrounds,
                'current_background': self.current_background,
                'owned_powers': list(self.owned_powers),
                'owned_particles': self.owned_particles,
                'current_particle': self.current_particle
            }, f)

    def reset_all_data(self):
        """Reset all game data to initial state"""
        self.high_score = {
            'EASY': 0,
            'NORMAL': 0,
            'HARD': 0
        }
        self.total_coins = 0
        self.owned_skins = {'default': True}
        self.current_skin = 'default'
        self.owned_backgrounds = {'default': True}
        self.current_background = 'default'
        self.owned_powers = set()
        self.owned_particles = {'none': True}
        self.current_particle = 'none'
        self.score = 0
        # Reload default bird skin
        self.load_bird_skin()
        # Save the reset data
        self.save_game_data()

    def load_bird_skin(self):
        """Load bird images based on current skin"""
        try:
            if self.current_skin == 'default':
                self.bird.images = [
                    pygame.image.load('assets/bird_up.png').convert_alpha(),
                    pygame.image.load('assets/bird_middle.png').convert_alpha(),
                    pygame.image.load('assets/bird_down.png').convert_alpha()
                ]
            else:
                self.bird.images = [
                    pygame.image.load(f'assets/skins/bird_{self.current_skin}_up.png').convert_alpha(),
                    pygame.image.load(f'assets/skins/bird_{self.current_skin}_middle.png').convert_alpha(),
                    pygame.image.load(f'assets/skins/bird_{self.current_skin}_down.png').convert_alpha()
                ]
        except Exception as e:
            print(f"Could not load bird skin {self.current_skin}: {e}")
            # Fallback to default skin
            self.bird.images = [
                pygame.image.load('assets/bird_up.png').convert_alpha(),
                pygame.image.load('assets/bird_middle.png').convert_alpha(),
                pygame.image.load('assets/bird_down.png').convert_alpha()
            ]

    def generate_particles(self):
        """Generate particles behind the bird when flapping"""
        if self.current_particle != 'none':
            # Add particles behind the bird
            for _ in range(3):  # Generate 3 particles per flap
                particle_x = self.bird.x + random.randint(-10, 5)
                particle_y = self.bird.y + random.randint(-10, 10) + 12  # Center on bird
                self.particles.append(Particle(particle_x, particle_y, self.current_particle))

    def update_particles(self):
        """Update all particles and remove dead ones"""
        self.particles = [p for p in self.particles if p.update()]

    def draw_particles(self, screen):
        """Draw all active particles"""
        for particle in self.particles:
            particle.draw(screen)

    def render_pixelated_text(self, text, size, color=(0, 0, 0)):
        """Render pixelated text with improved readability"""
        # Create a smaller font and scale up by 20% for subtle pixelation
        small_font = pygame.font.Font(None, max(int(size * 0.8), 8))  # 20% smaller
        small_text = small_font.render(text, False, color)  # No antialiasing

        # Scale up by 20% to create subtle pixelation effect
        scale_factor = 1.2
        scaled_size = (int(small_text.get_width() * scale_factor), int(small_text.get_height() * scale_factor))
        pixelated_text = pygame.transform.scale(small_text, scaled_size)

        return pixelated_text

    def render_number_with_sprites(self, number, x_pos, y_pos, screen, spacing=4):
        """Render a number using pixel number sprites"""
        number_str = str(number)
        current_x = x_pos

        for digit in number_str:
            if digit in self.number_sprites:
                sprite = self.number_sprites[digit]
                screen.blit(sprite, (current_x, y_pos))
                current_x += sprite.get_width() + spacing

        return current_x  # Return final x position

    def create_cloud_sprites(self):
        """Pre-create cloud sprites for better performance"""
        import random

        # Define cloud sizes and create sprites
        sizes = {
            'small': {'width': 40, 'height': 20, 'circles': 3},
            'medium': {'width': 60, 'height': 30, 'circles': 4},
            'large': {'width': 80, 'height': 35, 'circles': 5}
        }

        for size_name, size_info in sizes.items():
            # Create multiple variations of each size
            for variant in range(3):
                # Create surface for this cloud sprite
                cloud_surface = pygame.Surface((size_info['width'], size_info['height']), pygame.SRCALPHA)

                # Generate consistent random positions for this variant
                random.seed(hash(size_name + str(variant)))  # Consistent randomness

                # Draw overlapping circles
                for i in range(size_info['circles']):
                    x = i * (size_info['width'] // max(1, size_info['circles'] - 1))
                    y = size_info['height'] // 2 + random.randint(-3, 3)
                    radius = random.randint(8, 12)
                    pygame.draw.circle(cloud_surface, (255, 255, 255), (x, y), radius)

                # Store the sprite
                sprite_key = f"{size_name}_{variant}"
                self.cloud_sprites[sprite_key] = cloud_surface

        # Reset random seed
        random.seed()

    def init_clouds(self):
        """Initialize clouds for animation"""
        import random
        # Create initial clouds with references to pre-made sprites
        for _ in range(5):
            size = random.choice(['small', 'medium', 'large'])
            variant = random.randint(0, 2)
            cloud = {
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(50, 200),
                'speed': random.uniform(0.3, 1.0),
                'sprite_key': f"{size}_{variant}",
                'opacity': random.randint(120, 180)
            }
            self.clouds.append(cloud)

    def update_clouds(self):
        """Update cloud positions and spawn new ones"""
        import random

        # Update existing clouds
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']

        # Remove clouds that have moved off screen
        self.clouds = [cloud for cloud in self.clouds if cloud['x'] < SCREEN_WIDTH + 100]

        # Add new clouds occasionally
        self.cloud_timer += 1
        if self.cloud_timer > random.randint(180, 360):  # Every 3-6 seconds at 60fps
            size = random.choice(['small', 'medium', 'large'])
            variant = random.randint(0, 2)
            new_cloud = {
                'x': -100,
                'y': random.randint(50, 200),
                'speed': random.uniform(0.3, 1.0),
                'sprite_key': f"{size}_{variant}",
                'opacity': random.randint(120, 180)
            }
            self.clouds.append(new_cloud)
            self.cloud_timer = 0

    def draw_cloud(self, screen, cloud):
        """Draw a single cloud using pre-created sprite"""
        sprite = self.cloud_sprites[cloud['sprite_key']].copy()
        sprite.set_alpha(cloud['opacity'])
        screen.blit(sprite, (int(cloud['x']), int(cloud['y'])))

    def use_power(self, power_id):
        """Activate a superpower"""
        power_data = self.available_powers[power_id]

        if power_id == 'pipe_destroyer':
            # Remove all pipes
            self.pipes = []
            # Add cooldown
            self.power_cooldowns[power_id] = power_data['cooldown']

        elif power_id == 'shield':
            # Activate shield
            self.shield_active = True
            self.shield_timer = power_data['duration']
            # Add cooldown
            self.power_cooldowns[power_id] = power_data['cooldown']

    def load_assets(self):
        try:
            # Load images
            self.background = pygame.image.load('assets/background.png').convert()
            
            # Load bird animation frames based on current skin
            self.load_bird_skin()
            pipe_img = pygame.image.load('assets/pipe.png').convert_alpha()
            # Store pipe dimensions for use in collision detection
            self.pipe_width = pipe_img.get_width()
            self.pipe_height = pipe_img.get_height()
            self.pipe_top = pygame.transform.flip(pipe_img, False, True)
            self.pipe_bottom = pipe_img
            
            # Load pixel font assets
            for i in range(10):
                self.number_sprites[str(i)] = pygame.image.load(f'fonts/number_{i}.png').convert_alpha()
            self.game_over_text = pygame.image.load('fonts/game_over.png').convert_alpha()
            self.press_space_text1 = pygame.image.load('fonts/press_space_1.png').convert_alpha()
            self.press_space_text2 = pygame.image.load('fonts/press_space_2.png').convert_alpha()
            self.press_space_text3 = pygame.image.load('fonts/press_space_3.png').convert_alpha()
            
            # Load sounds
            self.wing_sound = pygame.mixer.Sound('sounds/wing.wav')
            self.wing_sound.set_volume(0.5)  # Set to 50% volume
            
            # Load and play background music
            pygame.mixer.music.load('sounds/background-music.mp3')
            pygame.mixer.music.set_volume(0.7)  # Set to 20% volume
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            
        except Exception as e:
            print(f"Could not load assets. Error: {e}")
            self.pipe_width = 52
            self.pipe_height = 320  # Default height

    def reset_game(self, keep_difficulty=False):
        # Update high score and add coins before resetting
        if self.state == GameState.GAME_OVER:
            # Add coins equal to the score achieved
            self.total_coins += self.score
            
            if self.score > self.high_score.get(self.difficulty['name'], 0):
                self.high_score[self.difficulty['name']] = self.score
            
            # Save game data immediately
            self.save_game_data()
        
        self.bird = Bird(50, SCREEN_HEIGHT // 2)
        # Load all bird animation frames based on current skin
        self.load_bird_skin()
        # Create pipes with proper height from loaded image
        self.pipes = []
        for i in range(3):
            # Create new pipe and explicitly set its difficulty
            new_pipe = Pipe(SCREEN_WIDTH + i * PIPE_SPACING, self.difficulty, self.pipe_height)
            new_pipe.image_top = self.pipe_top
            new_pipe.image_bottom = self.pipe_bottom
            # Ensure difficulty settings are properly applied
            new_pipe.set_difficulty(self.difficulty)
            self.pipes.append(new_pipe)
        self.score = 0
        # If keep_difficulty is True, set state to PLAYING, otherwise go HOME
        self.state = GameState.PLAYING if keep_difficulty else GameState.HOME

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save game data before quitting
                self.save_game_data()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # ESC key always returns to home screen
                if event.key == pygame.K_ESCAPE and self.state != GameState.HOME:
                    self.reset_game()
                    return
                    
                if self.state == GameState.HOME:
                    if event.key == pygame.K_1:
                        self.difficulty = Difficulty.EASY
                        self.reset_game(keep_difficulty=True)
                    elif event.key == pygame.K_2:
                        self.difficulty = Difficulty.NORMAL
                        self.reset_game(keep_difficulty=True)
                    elif event.key == pygame.K_3:
                        self.difficulty = Difficulty.HARD
                        self.reset_game(keep_difficulty=True)
                elif self.state == GameState.PLAYING:
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        self.bird.flap()
                        self.generate_particles()
                        if self.wing_sound:
                            self.wing_sound.play()

                    # Handle superpower keys
                    for power_id, power_data in self.available_powers.items():
                        if power_id in self.owned_powers and event.key == power_data['key']:
                            if power_id not in self.power_cooldowns:
                                self.use_power(power_id)
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        # Just reset the game state but keep the same difficulty
                        self.reset_game(keep_difficulty=True)
                    elif event.key == pygame.K_h:  # 'H' key for home
                        self.reset_game(keep_difficulty=False)
            
            # Also handle mouse clicks for flapping and UI
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.state == GameState.HOME:
                        # Check if clicked shop button
                        shop_btn = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 30)
                        if shop_btn.collidepoint(mouse_pos):
                            self.state = GameState.SHOP

                        # Check if clicked new game button
                        new_game_btn = pygame.Rect(SCREEN_WIDTH - 110, 50, 100, 30)
                        if new_game_btn.collidepoint(mouse_pos):
                            self.state = GameState.CONFIRM_RESET
                            
                    elif self.state == GameState.SHOP:
                        # Handle shop item clicks
                        back_btn = pygame.Rect(10, 10, 100, 30)
                        if back_btn.collidepoint(mouse_pos):
                            self.state = GameState.HOME

                        # Check if clicked backgrounds button (bottom left)
                        bg_btn = pygame.Rect(10, SCREEN_HEIGHT - 40, 100, 30)
                        if bg_btn.collidepoint(mouse_pos):
                            self.state = GameState.BACKGROUND_SHOP

                        # Check if clicked powers button (bottom center)
                        power_btn = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - 40, 100, 30)
                        if power_btn.collidepoint(mouse_pos):
                            self.state = GameState.POWER_SHOP

                        # Check if clicked particles button (bottom right)
                        particles_btn = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 40, 100, 30)
                        if particles_btn.collidepoint(mouse_pos):
                            self.state = GameState.PARTICLES_SHOP

                        else:
                            # Check if clicked on any skin button
                            y_pos = 100
                            for skin, data in self.available_skins.items():
                                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)
                                if btn_rect.collidepoint(mouse_pos):
                                    if skin in self.owned_skins:
                                        # Select the skin
                                        self.current_skin = skin
                                        # Reload bird images with new skin
                                        self.load_bird_skin()
                                        self.save_game_data()
                                    elif self.total_coins >= data['price']:
                                        # Purchase the skin
                                        self.total_coins -= data['price']
                                        self.owned_skins[skin] = True
                                        self.current_skin = skin
                                        # Reload bird images with new skin
                                        self.load_bird_skin()
                                        self.save_game_data()
                                y_pos += 60

                    elif self.state == GameState.BACKGROUND_SHOP:
                        # Handle background shop clicks
                        back_btn = pygame.Rect(10, 10, 100, 30)
                        if back_btn.collidepoint(mouse_pos):
                            self.state = GameState.SHOP
                        else:
                            # Check if clicked on any background button
                            y_pos = 100
                            for bg_name, data in self.available_backgrounds.items():
                                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)
                                if btn_rect.collidepoint(mouse_pos):
                                    if bg_name in self.owned_backgrounds:
                                        # Select the background
                                        self.current_background = bg_name
                                        self.save_game_data()
                                    elif self.total_coins >= data['price']:
                                        # Purchase the background
                                        self.total_coins -= data['price']
                                        self.owned_backgrounds[bg_name] = True
                                        self.current_background = bg_name
                                        self.save_game_data()
                                y_pos += 60

                    elif self.state == GameState.POWER_SHOP:
                        # Handle power shop clicks
                        back_btn = pygame.Rect(10, 10, 100, 30)
                        if back_btn.collidepoint(mouse_pos):
                            self.state = GameState.SHOP
                        else:
                            # Check if clicked on any power button
                            y_pos = 100
                            for power_id, data in self.available_powers.items():
                                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos, 240, 60)
                                if btn_rect.collidepoint(mouse_pos):
                                    if power_id not in self.owned_powers and self.total_coins >= data['price']:
                                        # Purchase the power
                                        self.total_coins -= data['price']
                                        self.owned_powers.add(power_id)
                                        self.save_game_data()
                                y_pos += 80

                    elif self.state == GameState.PARTICLES_SHOP:
                        # Handle particles shop clicks
                        back_btn = pygame.Rect(10, 10, 100, 30)
                        if back_btn.collidepoint(mouse_pos):
                            self.state = GameState.SHOP
                        else:
                            # Check particle purchases and selections
                            y_pos = 100
                            for particle_id, data in self.available_particles.items():
                                if particle_id == 'none':
                                    continue  # Skip the none option for now
                                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)
                                if btn_rect.collidepoint(mouse_pos):
                                    if particle_id not in self.owned_particles and self.total_coins >= data['price']:
                                        # Purchase the particle
                                        self.total_coins -= data['price']
                                        self.owned_particles[particle_id] = True
                                        self.current_particle = particle_id
                                        self.save_game_data()
                                    elif particle_id in self.owned_particles:
                                        # Switch to this particle if already owned
                                        self.current_particle = particle_id
                                        self.save_game_data()
                                y_pos += 50

                            # Add "none" option at the end
                            none_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)
                            if none_btn_rect.collidepoint(mouse_pos):
                                self.current_particle = 'none'
                                self.save_game_data()

                    elif self.state == GameState.CONFIRM_RESET:
                        # Handle Yes/No button clicks
                        yes_btn = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 40, 60, 30)
                        no_btn = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 40, 60, 30)

                        if yes_btn.collidepoint(mouse_pos):
                            # Reset all data and return to home
                            self.reset_all_data()
                            self.state = GameState.HOME
                        elif no_btn.collidepoint(mouse_pos):
                            # Cancel and return to home
                            self.state = GameState.HOME

                    elif self.state == GameState.PLAYING:
                        self.bird.flap()
                        self.generate_particles()
                        if self.wing_sound:
                            self.wing_sound.play()
                            
                    elif self.state == GameState.GAME_OVER:
                        # Check if click is within the Home button area
                        button_y = SCREEN_HEIGHT - 150
                        home_btn_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - 50,  # x position
                            button_y + 30,  # y position (matches drawing position)
                            100,  # width
                            30   # height
                        )
                        if home_btn_rect.collidepoint(mouse_pos):
                            self.reset_game(keep_difficulty=False)
                        else:
                            # If not clicking home button, continue with same difficulty
                            self.reset_game(keep_difficulty=True)

    def update(self):
        # Always update clouds for animation on home screen
        if self.state == GameState.HOME:
            self.update_clouds()

        if self.state != GameState.PLAYING:
            return

        self.bird.update()

        # Update particles
        self.update_particles()

        # Update power cooldowns
        for power_id in list(self.power_cooldowns.keys()):
            self.power_cooldowns[power_id] -= 1/60  # Decrease by 1/60 second (assuming 60fps)
            if self.power_cooldowns[power_id] <= 0:
                del self.power_cooldowns[power_id]

        # Update shield timer
        if self.shield_active:
            self.shield_timer -= 1/60
            if self.shield_timer <= 0:
                self.shield_active = False

        # Update pipes and check for score
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                self.score += 1

        # Remove off-screen pipes and add new ones
        self.pipes = [pipe for pipe in self.pipes if pipe.x > -60]
        while len(self.pipes) < 3:
            if self.pipes:
                last_pipe = max(pipe.x for pipe in self.pipes)
            else:
                # If no pipes exist (e.g., after pipe destroyer), start from screen width
                last_pipe = SCREEN_WIDTH
            new_pipe = Pipe(last_pipe + PIPE_SPACING, self.difficulty, self.pipe_height)
            new_pipe.image_top = self.pipe_top
            new_pipe.image_bottom = self.pipe_bottom
            self.pipes.append(new_pipe)

        # Check for collisions (unless shield is active)
        if not self.shield_active and (
            self.bird.y < 0 or self.bird.y > SCREEN_HEIGHT - 24 or
            any(self.bird.rect.colliderect(pipe.top_pipe) or
                self.bird.rect.colliderect(pipe.bottom_pipe)
                for pipe in self.pipes)
        ):
            self.state = GameState.GAME_OVER

    def draw(self):
        # Draw background using selected background color
        if self.current_background in self.available_backgrounds:
            bg_color = self.available_backgrounds[self.current_background]['color']
            screen.fill(bg_color)
        else:
            screen.fill(WHITE)  # Fallback color

        if self.state == GameState.HOME:
            # Draw animated clouds
            for cloud in self.clouds:
                self.draw_cloud(screen, cloud)

            # Draw difficulty selection menu with pixelated text

            # Draw total coins at the top
            coins_text = self.render_pixelated_text(f"Coins: {self.total_coins}", 32, BLACK)
            screen.blit(coins_text, (10, 10))

            # Draw shop button
            shop_btn = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 30)
            pygame.draw.rect(screen, BLACK, shop_btn)
            shop_text = self.render_pixelated_text("SHOP", 24, WHITE)
            shop_text_rect = shop_text.get_rect(center=shop_btn.center)
            screen.blit(shop_text, shop_text_rect)

            # Draw new game button
            new_game_btn = pygame.Rect(SCREEN_WIDTH - 110, 50, 100, 30)
            pygame.draw.rect(screen, (200, 0, 0), new_game_btn)  # Red button
            new_game_text = self.render_pixelated_text("NEW GAME", 20, WHITE)
            new_game_text_rect = new_game_text.get_rect(center=new_game_btn.center)
            screen.blit(new_game_text, new_game_text_rect)

            # Draw title
            title = self.render_pixelated_text("Select Difficulty", 36, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(title, title_rect)
            
            # Draw options
            difficulties = [
                ("1. EASY", Difficulty.EASY),
                ("2. NORMAL", Difficulty.NORMAL),
                ("3. HARD", Difficulty.HARD)
            ]
            
            for i, (text, diff) in enumerate(difficulties):
                # Draw difficulty option with pixelated text
                diff_text = self.render_pixelated_text(text, 32, BLACK)
                diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH//2, 200 + i*50))
                screen.blit(diff_text, diff_rect)

                # Draw high score for this difficulty with pixelated text
                score = self.high_score.get(diff['name'], 0)
                score_text = self.render_pixelated_text(f"High Score: {score}", 24, BLACK)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 225 + i*50))
                screen.blit(score_text, score_rect)

        elif self.state == GameState.SHOP:
            # Draw shop interface with pixelated text

            # Draw back button
            back_btn = pygame.Rect(10, 10, 100, 30)
            pygame.draw.rect(screen, BLACK, back_btn)
            back_text = self.render_pixelated_text("BACK", 24, WHITE)
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)

            # Draw total coins
            coins_text = self.render_pixelated_text(f"Coins: {self.total_coins}", 32, BLACK)
            coins_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))
            screen.blit(coins_text, coins_rect)

            # Draw backgrounds button (bottom left)
            bg_btn = pygame.Rect(10, SCREEN_HEIGHT - 40, 100, 30)
            pygame.draw.rect(screen, (0, 100, 200), bg_btn)
            bg_text = self.render_pixelated_text("BACKGROUNDS", 16, WHITE)
            bg_text_rect = bg_text.get_rect(center=bg_btn.center)
            screen.blit(bg_text, bg_text_rect)

            # Draw powers button (bottom center)
            power_btn = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - 40, 100, 30)
            pygame.draw.rect(screen, (200, 100, 0), power_btn)
            power_text = self.render_pixelated_text("POWERS", 18, WHITE)
            power_text_rect = power_text.get_rect(center=power_btn.center)
            screen.blit(power_text, power_text_rect)

            # Draw particles button (bottom right)
            particles_btn = pygame.Rect(SCREEN_WIDTH - 110, SCREEN_HEIGHT - 40, 100, 30)
            pygame.draw.rect(screen, (150, 0, 200), particles_btn)
            particles_text = self.render_pixelated_text("PARTICLES", 16, WHITE)
            particles_text_rect = particles_text.get_rect(center=particles_btn.center)
            screen.blit(particles_text, particles_text_rect)

            # Draw title
            title = self.render_pixelated_text("Bird Skins", 36, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            screen.blit(title, title_rect)
            
            # Draw skin options
            y_pos = 100
            for skin, data in self.available_skins.items():
                # Draw item button
                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)

                # Different colors based on skin type and status
                skin_colors = {
                    'default': (255, 200, 0),    # Golden yellow for default
                    'blue': (66, 135, 245),      # Blue
                    'red': (245, 66, 66),        # Red
                    'golden': (255, 215, 0)      # Gold
                }

                base_color = skin_colors.get(skin, BLACK)

                if skin == self.current_skin:
                    # Brighten the color for selected skin
                    color = tuple(min(255, c + 50) for c in base_color)
                elif skin in self.owned_skins:
                    # Use the skin's base color for owned
                    color = base_color
                else:
                    # Darken the color for unowned skins
                    color = tuple(max(50, c - 100) for c in base_color)
                
                pygame.draw.rect(screen, color, btn_rect)
                
                # Draw skin name and price/status with pixelated text
                if skin in self.owned_skins:
                    if skin == self.current_skin:
                        status = "SELECTED"
                    else:
                        status = "OWNED"
                    text = f"{data['name']} - {status}"
                else:
                    text = f"{data['name']} - {data['price']} coins"

                item_text = self.render_pixelated_text(text, 24, WHITE)
                text_rect = item_text.get_rect(center=btn_rect.center)
                screen.blit(item_text, text_rect)
                
                y_pos += 60

        elif self.state == GameState.BACKGROUND_SHOP:
            # Draw background shop interface

            # Draw back button
            back_btn = pygame.Rect(10, 10, 100, 30)
            pygame.draw.rect(screen, BLACK, back_btn)
            back_text = self.render_pixelated_text("BACK", 24, WHITE)
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)

            # Draw total coins
            coins_text = self.render_pixelated_text(f"Coins: {self.total_coins}", 32, BLACK)
            coins_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))
            screen.blit(coins_text, coins_rect)

            # Draw title
            title = self.render_pixelated_text("Backgrounds", 36, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            screen.blit(title, title_rect)

            # Draw background options
            y_pos = 100
            for bg_name, data in self.available_backgrounds.items():
                # Draw background button
                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)

                # Use the background color for the button
                base_color = data['color']

                if bg_name == self.current_background:
                    # Brighten for selected background
                    color = tuple(min(255, c + 50) for c in base_color)
                elif bg_name in self.owned_backgrounds:
                    # Use base color for owned
                    color = base_color
                else:
                    # Darken for unowned backgrounds
                    color = tuple(max(30, c - 80) for c in base_color)

                pygame.draw.rect(screen, color, btn_rect)

                # Draw background name and price/status
                if bg_name in self.owned_backgrounds:
                    if bg_name == self.current_background:
                        status = "SELECTED"
                    else:
                        status = "OWNED"
                    text = f"{data['name']} - {status}"
                else:
                    text = f"{data['name']} - {data['price']} coins"

                # Choose text color based on background brightness
                brightness = sum(base_color) / 3
                text_color = WHITE if brightness < 128 else BLACK

                item_text = self.render_pixelated_text(text, 24, text_color)
                text_rect = item_text.get_rect(center=btn_rect.center)
                screen.blit(item_text, text_rect)

                y_pos += 60

        elif self.state == GameState.POWER_SHOP:
            # Draw power shop interface

            # Draw back button
            back_btn = pygame.Rect(10, 10, 100, 30)
            pygame.draw.rect(screen, BLACK, back_btn)
            back_text = self.render_pixelated_text("BACK", 24, WHITE)
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)

            # Draw total coins
            coins_text = self.render_pixelated_text(f"Coins: {self.total_coins}", 32, BLACK)
            coins_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))
            screen.blit(coins_text, coins_rect)

            # Draw title
            title = self.render_pixelated_text("Superpowers", 36, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            screen.blit(title, title_rect)

            # Draw power options
            y_pos = 100
            for power_id, data in self.available_powers.items():
                # Draw power button
                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, y_pos, 240, 60)

                # Different colors based on ownership
                if power_id in self.owned_powers:
                    color = (0, 150, 0)  # Green for owned
                else:
                    color = (150, 0, 0)  # Red for unowned

                pygame.draw.rect(screen, color, btn_rect)

                # Draw power name and description
                if power_id in self.owned_powers:
                    text = f"{data['name']} - OWNED"
                    desc_text = data['description']
                else:
                    text = f"{data['name']} - {data['price']} coins"
                    desc_text = data['description']

                name_text = self.render_pixelated_text(text, 24, WHITE)
                name_rect = name_text.get_rect(center=(SCREEN_WIDTH//2, y_pos + 15))
                screen.blit(name_text, name_rect)

                desc_text_render = self.render_pixelated_text(desc_text, 20, WHITE)
                desc_rect = desc_text_render.get_rect(center=(SCREEN_WIDTH//2, y_pos + 40))
                screen.blit(desc_text_render, desc_rect)

                y_pos += 80

        elif self.state == GameState.PARTICLES_SHOP:
            # Draw particles shop interface

            # Draw back button
            back_btn = pygame.Rect(10, 10, 100, 30)
            pygame.draw.rect(screen, BLACK, back_btn)
            back_text = self.render_pixelated_text("BACK", 24, WHITE)
            back_text_rect = back_text.get_rect(center=back_btn.center)
            screen.blit(back_text, back_text_rect)

            # Draw total coins
            coins_text = self.render_pixelated_text(f"Coins: {self.total_coins}", 32, BLACK)
            coins_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 20))
            screen.blit(coins_text, coins_rect)

            # Draw title
            title = self.render_pixelated_text("Particle Effects", 36, BLACK)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            screen.blit(title, title_rect)

            # Draw current selection indicator
            current_text = self.render_pixelated_text(f"Current: {self.available_particles[self.current_particle]['name']}", 24, BLACK)
            current_rect = current_text.get_rect(center=(SCREEN_WIDTH//2, 75))
            screen.blit(current_text, current_rect)

            # Draw particle options
            y_pos = 100
            for particle_id, data in self.available_particles.items():
                if particle_id == 'none':
                    continue  # Skip the none option for the main list

                # Draw particle button
                btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)

                # Different colors based on ownership and selection
                if particle_id in self.owned_particles:
                    if particle_id == self.current_particle:
                        color = (0, 200, 0)  # Bright green for current selection
                    else:
                        color = (0, 150, 0)  # Green for owned
                else:
                    color = (150, 0, 150)  # Purple for unowned

                pygame.draw.rect(screen, color, btn_rect)

                # Draw particle name and price/status
                if particle_id in self.owned_particles:
                    if particle_id == self.current_particle:
                        text = f"{data['name']} - SELECTED"
                    else:
                        text = f"{data['name']} - OWNED"
                else:
                    text = f"{data['name']} - {data['price']} coins"

                particle_text = self.render_pixelated_text(text, 18, WHITE)
                text_rect = particle_text.get_rect(center=btn_rect.center)
                screen.blit(particle_text, text_rect)

                y_pos += 50

            # Add "none" option at the end
            none_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, y_pos, 200, 40)
            if self.current_particle == 'none':
                none_color = (0, 200, 0)  # Bright green if selected
                none_text = "No Particles - SELECTED"
            else:
                none_color = (100, 100, 100)  # Gray
                none_text = "No Particles"

            pygame.draw.rect(screen, none_color, none_btn_rect)
            none_text_render = self.render_pixelated_text(none_text, 18, WHITE)
            none_text_rect = none_text_render.get_rect(center=none_btn_rect.center)
            screen.blit(none_text_render, none_text_rect)

        elif self.state == GameState.CONFIRM_RESET:
            # Draw confirmation dialog with overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(160)  # Semi-transparent
            overlay.fill((0, 0, 0))  # Dark overlay
            screen.blit(overlay, (0, 0))

            # Draw confirmation dialog
            dialog_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 80, 240, 160)
            pygame.draw.rect(screen, WHITE, dialog_rect)
            pygame.draw.rect(screen, BLACK, dialog_rect, 3)  # Border

            # Draw warning text
            warning_text = self.render_pixelated_text("Are you sure?", 32, BLACK)
            warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            screen.blit(warning_text, warning_rect)

            sub_text = self.render_pixelated_text("This will delete all", 24, BLACK)
            sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
            screen.blit(sub_text, sub_rect)

            sub_text2 = self.render_pixelated_text("progress and coins!", 24, BLACK)
            sub_rect2 = sub_text2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
            screen.blit(sub_text2, sub_rect2)

            # Draw Yes/No buttons
            yes_btn = pygame.Rect(SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 40, 60, 30)
            no_btn = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 40, 60, 30)

            pygame.draw.rect(screen, (200, 0, 0), yes_btn)  # Red for Yes
            pygame.draw.rect(screen, (0, 150, 0), no_btn)   # Green for No

            yes_text = self.render_pixelated_text("YES", 24, WHITE)
            yes_text_rect = yes_text.get_rect(center=yes_btn.center)
            screen.blit(yes_text, yes_text_rect)

            no_text = self.render_pixelated_text("NO", 24, WHITE)
            no_text_rect = no_text.get_rect(center=no_btn.center)
            screen.blit(no_text, no_text_rect)

        elif self.state in [GameState.PLAYING, GameState.GAME_OVER]:
            # Draw pipes and bird
            for pipe in self.pipes:
                pipe.draw(screen)

            # Draw particles behind bird
            self.draw_particles(screen)

            self.bird.draw(screen)
            
            if self.state == GameState.PLAYING:
                # Draw ESC instruction in top-left corner with pixelated text
                esc_text = self.render_pixelated_text("ESC: Return to Menu", 24, BLACK)
                screen.blit(esc_text, (10, 10))

                # Draw current score
                score_str = str(self.score)
                spacing = 4
                total_width = sum(self.number_sprites[d].get_width() for d in score_str)
                total_width += spacing * (len(score_str) - 1)
                x_pos = SCREEN_WIDTH // 2 - total_width // 2
                y_pos = 30
                
                # Draw "Score:" label with pixelated text
                score_label = self.render_pixelated_text("Score:", 24, BLACK)
                screen.blit(score_label, (x_pos - 70, y_pos + 5))
                
                for digit in score_str:
                    if digit in self.number_sprites:
                        sprite = self.number_sprites[digit]
                        screen.blit(sprite, (x_pos, y_pos))
                        x_pos += sprite.get_width() + spacing
                
                # Draw coins that will be earned
                coins_str = str(self.score)
                total_width = sum(self.number_sprites[d].get_width() for d in coins_str)
                total_width += spacing * (len(coins_str) - 1)
                x_pos = SCREEN_WIDTH // 2 - total_width // 2
                coins_y_pos = y_pos + 40
                
                # Draw "Coins:" label with pixelated text
                coins_label = self.render_pixelated_text("Coins:", 24, BLACK)
                screen.blit(coins_label, (x_pos - 70, coins_y_pos + 5))
                
                for digit in coins_str:
                    if digit in self.number_sprites:
                        sprite = self.number_sprites[digit]
                        screen.blit(sprite, (x_pos, coins_y_pos))
                        x_pos += sprite.get_width() + spacing
                
                # Draw current difficulty high score
                high_score_str = str(self.high_score.get(self.difficulty['name'], 0))
                total_width = sum(self.number_sprites[d].get_width() for d in high_score_str)
                total_width += spacing * (len(high_score_str) - 1)
                x_pos = SCREEN_WIDTH // 2 - total_width // 2
                high_score_y_pos = 110

                # Draw "High Score:" label with pixelated text
                high_score_label = self.render_pixelated_text("High Score:", 24, BLACK)
                screen.blit(high_score_label, (x_pos - 90, high_score_y_pos + 5))

                for digit in high_score_str:
                    if digit in self.number_sprites:
                        sprite = self.number_sprites[digit]
                        screen.blit(sprite, (x_pos, high_score_y_pos))
                        x_pos += sprite.get_width() + spacing

                # Draw power cooldown bars if player owns powers
                if self.owned_powers:
                    power_y = high_score_y_pos + 50
                    power_count = 0

                    for power_id in self.owned_powers:
                        if power_id in self.available_powers:
                            power_data = self.available_powers[power_id]

                            # Calculate position for this power
                            bar_width = 80
                            bar_height = 8
                            bar_x = 10 + power_count * (bar_width + 10)

                            # Draw power label
                            key_name = pygame.key.name(power_data['key']).upper()
                            power_label = self.render_pixelated_text(f"{key_name}:", 20, BLACK)
                            screen.blit(power_label, (bar_x, power_y - 15))

                            # Draw cooldown bar
                            bar_rect = pygame.Rect(bar_x, power_y, bar_width, bar_height)
                            pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Background

                            if power_id in self.power_cooldowns:
                                # Power is on cooldown
                                remaining = self.power_cooldowns[power_id]
                                total_cooldown = power_data['cooldown']
                                progress = 1 - (remaining / total_cooldown)
                                fill_width = int(bar_width * progress)

                                fill_rect = pygame.Rect(bar_x, power_y, fill_width, bar_height)
                                pygame.draw.rect(screen, (200, 100, 0), fill_rect)  # Orange progress

                                # Show remaining time
                                time_text = self.render_pixelated_text(f"{remaining:.1f}s", 16, BLACK)
                                screen.blit(time_text, (bar_x, power_y + 12))
                            else:
                                # Power is ready
                                pygame.draw.rect(screen, (0, 200, 0), bar_rect)  # Green ready
                                ready_text = self.render_pixelated_text("READY", 16, BLACK)
                                screen.blit(ready_text, (bar_x, power_y + 12))

                            power_count += 1

                # Draw shield effect if active
                if self.shield_active:
                    # Draw shield indicator
                    shield_text = self.render_pixelated_text(f"SHIELD: {self.shield_timer:.1f}s", 24, (0, 255, 255))
                    screen.blit(shield_text, (10, SCREEN_HEIGHT - 40))

            elif self.state == GameState.GAME_OVER and self.game_over_text:
                # Draw semi-transparent overlay for better text visibility
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)  # Semi-transparent
                overlay.fill((135, 206, 250))  # Light blue background
                screen.blit(overlay, (0, 0))

                # Draw "GAME OVER" at the top
                game_over_y = 80
                x_pos = SCREEN_WIDTH // 2 - self.game_over_text.get_width() // 2
                screen.blit(self.game_over_text, (x_pos, game_over_y))

                # Draw total coins earned this round with pixelated text
                coins_text = self.render_pixelated_text(f"Coins Earned: {self.score}", 32, BLACK)
                coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH//2, game_over_y + 50))
                screen.blit(coins_text, coins_rect)

                # Get current high score and check if new high score
                current_high_score = self.high_score.get(self.difficulty['name'], 0)
                is_new_high_score = self.score > current_high_score

                score_y = game_over_y + 90
                spacing = 4

                # Draw current score with pixelated text and number sprites
                score_label = self.render_pixelated_text("Score:", 28, BLACK)
                score_label_rect = score_label.get_rect(center=(SCREEN_WIDTH//2 - 30, score_y))
                screen.blit(score_label, score_label_rect)

                # Use number sprites for the score
                score_x = SCREEN_WIDTH//2 + 10
                self.render_number_with_sprites(self.score, score_x, score_y - 10, screen)

                # Draw high score with pixelated text and number sprites
                high_score_y = score_y + 50
                high_score_value = max(self.score, current_high_score)
                high_score_label = self.render_pixelated_text("High Score:", 28, BLACK)
                high_score_label_rect = high_score_label.get_rect(center=(SCREEN_WIDTH//2 - 40, high_score_y))
                screen.blit(high_score_label, high_score_label_rect)

                # Use number sprites for the high score
                high_score_x = SCREEN_WIDTH//2 + 20
                self.render_number_with_sprites(high_score_value, high_score_x, high_score_y - 10, screen)

                # Draw instructions and home button at bottom with pixelated text
                button_y = SCREEN_HEIGHT - 150

                retry_text = self.render_pixelated_text("Press SPACE to try again", 24, BLACK)
                retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH//2, button_y))
                screen.blit(retry_text, retry_rect)

                home_btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, button_y + 30, 100, 30)
                pygame.draw.rect(screen, BLACK, home_btn_rect)
                home_text = self.render_pixelated_text("HOME", 24, WHITE)
                home_text_rect = home_text.get_rect(center=home_btn_rect.center)
                screen.blit(home_text, home_text_rect)

                h_text = self.render_pixelated_text("or press H", 24, BLACK)
                h_rect = h_text.get_rect(center=(SCREEN_WIDTH//2, button_y + 80))
                screen.blit(h_text, h_rect)

        pygame.display.flip()

def main():
    game = Game()
    
    while True:
        game.handle_input()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()