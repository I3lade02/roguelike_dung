import pygame
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_COLOR

class Enemy:
    def __init__(self, x, y, size=28, speed=2, health=3):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.health = health
        self.alive = True
        self.hit_flash_duration = 0.2
        self.last_hit_time = 0

    def update(self, player_pos, walkable_areas):
        px, py = player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        dist = (dx**2 + dy**2)**0.5

        if dist == 0:
            return  # Already on top of player, don't move

        dx, dy = dx / dist, dy / dist  # Normalize
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

    def draw(self, surface):
        current_time = time.time()
        if current_time - self.last_hit_time < self.hit_flash_duration:
            color = (255, 0, 0)
        else:
            color = (200, 50, 50)

        pygame.draw.rect(surface, color, self.rect)

        #Draw health bar for enemy
        bar_width = self.rect.width
        bar_height = 5
        health_ration = max(self.health / 3, 0)
        health_bar = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, int(bar_width * health_ration), bar_height)
        back_bar = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, bar_width, bar_height)

        pygame.draw.rect(surface, (100, 0, 0), back_bar)
        pygame.draw.rect(surface, (0, 255, 0), health_bar)