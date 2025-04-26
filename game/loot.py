import pygame
import random

class Loot:
    def __init__(self, x, y, loot_type="health"):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.type = loot_type
        self.collected = False

    def draw(self, surface, camera_offset=(0, 0)):
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        if self.type == "health":
            pygame.draw.rect(surface, (0, 255, 0), offset_rect)