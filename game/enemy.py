import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_COLOR

class Enemy:
    def __init__(self, x, y, size=28, speed=2):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def update(self, player_pos, walkable_areas):
        px, py = player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        dist = (dx**2 + dy**2)**0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            move_x = int(dx * self.speed)
            move_y= int(dy * self.speed)

        new_rect_x = self.rect.move(move_x, 0)
        if any(new_rect_x.colliderect(area) for area in walkable_areas):
            self.rect.x += move_x
        
        new_rect_y = self.rect.move(0, move_y)
        if any(new_rect_y.colliderect(area) for area in walkable_areas):
            self.rect.y += move_y

    def draw(self, surface):
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)