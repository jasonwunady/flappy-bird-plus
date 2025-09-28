import pygame
from constants import GRAVITY, FLAP_POWER

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.images = []
        self.rect = pygame.Rect(x, y, 34, 24)
        self.animation_timer = 0
        self.animation_speed = 0.2
        self.current_frame = 1
        self.animation_sequence = [0, 1, 2, 1]
        self.animation_index = 0
        self.last_update = pygame.time.get_ticks()

    def flap(self):
        self.velocity = FLAP_POWER

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.animation_speed * 1000:
            self.animation_index = (self.animation_index + 1) % len(self.animation_sequence)
            self.current_frame = self.animation_sequence[self.animation_index]
            self.last_update = current_time

    def draw(self, screen):
        if self.images:
            screen.blit(self.images[self.current_frame], self.rect)
        else:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)