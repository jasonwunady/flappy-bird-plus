import pygame
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

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
GRAVITY = 0.25
FLAP_POWER = -5
PIPE_SPACING = 200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)