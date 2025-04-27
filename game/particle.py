import pygame
import random

class Particle:
    def __init__(self, x, y, color, size=6, lifetime=30, speed=3):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, surface, camera_offset=(0, 0)):
        if self.lifetime > 0:
            offset_x = self.x - camera_offset[0]
            offset_y = self.y - camera_offset[1]
            pygame.draw.circle(surface, self.color, (int(offset_x), int(offset_y)), int(self.size))