import pygame
import random
from constants import SCREEN_HEIGHT

class Pipe:
    def __init__(self, x, difficulty, pipe_height=320):
        self.x = x
        self.pipe_height = pipe_height
        self.set_difficulty(difficulty)
        self.passed = False
        self.image_top = None
        self.image_bottom = None

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.speed = difficulty['speed']
        self.gap = difficulty['gap']
        self.gap_y = random.randint(100, SCREEN_HEIGHT - self.gap - 100)

        self.top_pipe = pygame.Rect(self.x, self.gap_y - self.pipe_height, 52, self.pipe_height)
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + self.gap, 52, self.pipe_height)

    def update(self):
        self.x -= self.speed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self, screen):
        if self.image_top and self.image_bottom:
            screen.blit(self.image_top, (self.x, self.gap_y - self.pipe_height))
            screen.blit(self.image_bottom, (self.x, self.gap_y + self.gap))
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.top_pipe)
            pygame.draw.rect(screen, (0, 255, 0), self.bottom_pipe)