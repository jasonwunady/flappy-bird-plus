import pygame
import random
import colorsys

class Particle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.life = 1.0
        self.age = 0.0

        if particle_type == 'stars':
            self.velocity_x = random.uniform(-1, 1)
            self.velocity_y = random.uniform(-1, 1)
            self.size = random.randint(2, 4)
            self.color = (255, 255, random.randint(150, 255))
            self.decay_rate = 0.02
        elif particle_type == 'fire':
            self.velocity_x = random.uniform(-0.5, 0.5)
            self.velocity_y = random.uniform(-2, 0)
            self.size = random.randint(3, 6)
            self.color = (255, random.randint(100, 150), 0)
            self.decay_rate = 0.03
        elif particle_type == 'sparkles':
            self.velocity_x = random.uniform(-1.5, 1.5)
            self.velocity_y = random.uniform(-1.5, 1.5)
            self.size = random.randint(1, 3)
            colors = [(255, 192, 203), (138, 43, 226), (0, 255, 255), (255, 255, 0)]
            self.color = random.choice(colors)
            self.decay_rate = 0.025
        elif particle_type == 'rainbow':
            self.velocity_x = random.uniform(-0.8, 0.8)
            self.velocity_y = random.uniform(-0.8, 0.8)
            self.size = random.randint(2, 5)
            self.base_hue = random.uniform(0, 360)
            self.decay_rate = 0.015

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.age += 0.016
        self.life -= self.decay_rate

        if self.particle_type == 'rainbow':
            hue = (self.base_hue + self.age * 100) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            self.color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

        return self.life > 0

    def draw(self, screen):
        if self.life > 0:
            alpha = max(0, min(255, int(self.life * 255)))
            color_with_alpha = (*self.color, alpha)

            particle_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))