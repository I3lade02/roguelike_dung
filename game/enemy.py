import pygame
import time
from config import ENEMY_COLOR, FAST_ENEMY_COLOR, TOUGH_ENEMY_COLOR

class Enemy:
    def __init__(self, x, y, size=28, speed=2, health=3, enemy_type="normal"):
        self.rect = pygame.Rect(x, y, size, size)
        
        self.type = enemy_type
        if self.type == "normal":
            self.speed = 2
            self.health = 3
        elif self.type == "fast":
            self.speed = 4
            self.health = 2
        elif self.type == "tough":
            self.speed = 1
            self.health = 6

        self.alive = True
        self.hit_flash_duration = 0.2
        self.last_hit_time = 0

    def update(self, player_pos, walkable_areas):
        px, py = player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        dist = (dx**2 + dy**2)**0.5
        if dist == 0:
            return
        dx, dy = dx / dist, dy / dist
        move_x = int(dx * self.speed)
        move_y = int(dy * self.speed)

        new_rect_x = self.rect.move(move_x, 0)
        if any(new_rect_x.colliderect(area) for area in walkable_areas):
            self.rect.x += move_x
        new_rect_y = self.rect.move(0, move_y)
        if any(new_rect_y.colliderect(area) for area in walkable_areas):
            self.rect.y += move_y

    def take_damage(self, amount):
        self.health -= amount
        self.last_hit_time = time.time()
        if self.health <= 0:
            self.alive = False

    def draw(self, surface, camera_offset=(0, 0)):
        current_time = time.time()
       
        if self.type == "normal":
            base_color = ENEMY_COLOR
        elif self.type == "fast":
            base_color = FAST_ENEMY_COLOR
        elif self.type == "tough":
            base_color = TOUGH_ENEMY_COLOR

        color = (255, 0, 0) if current_time - self.last_hit_time < self.hit_flash_duration else base_color
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, color, offset_rect)

        bar_width = self.rect.width
        bar_height = 5
        health_ratio = max(self.health / 6, 0) if self.type == "tough" else max (self.health / 3, 0)
        bar_x = self.rect.x - camera_offset[0]
        bar_y = self.rect.y - bar_height - 2 - camera_offset[1]
        health_bar = pygame.Rect(bar_x, bar_y, int(bar_width * health_ratio), bar_height)
        back_bar = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (100, 0, 0), back_bar)
        pygame.draw.rect(surface, (0, 255, 0), health_bar)
