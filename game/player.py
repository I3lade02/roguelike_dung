import pygame
from config import PLAYER_COLOR

class Player:
    def __init__(self, x, y, size=32, speed=5):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def update(self, walkable_areas):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]: dy -= self.speed
        if keys[pygame.K_DOWN]: dy += self.speed

        new_rect = self.rect.move(dx, dy)
        if any(new_rect.colliderect(area) for area in walkable_areas):
            self.rect = new_rect
    
    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)