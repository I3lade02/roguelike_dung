import pygame
import time
from config import PLAYER_COLOR

class Player:
    def __init__(self, x, y, size=32, speed=5):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.attack_cooldown = 0.5
        self.last_attack = 0
        self.health = 5
        self.max_health = 5
        self.last_hit_time = 0
        self.hit_cooldown = 1.0

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

    def attack(self, enemies):
        now = time.time()
        if now - self.last_attack < self.attack_cooldown:
            return
        
        self.last_attack = now
        attack_range = self.rect.inflate(40, 40)

        for enemy in enemies:
            if enemy.alive and attack_range.colliderect(enemy.rect):
                enemy.take_damage(1)

    def take_damage(self, amount):
        now = time.time()
        if now - self.last_hit_time >= self.hit_cooldown:
            self.health -= amount
            self.last_hit_time = now
            print(f"Player took {amount} damage! Health: {self.health}")
    
    def draw_health_bar(self, surface):
        bar_width = 200
        bar_height = 20
        x, y = 10, 10
        health_ratio = max(self.health / self.max_health, 0)
        current_bar = pygame.Rect(x, y, int(bar_width * health_ratio), bar_height)
        back_bar = pygame.Rect(x, y, bar_width, bar_height)

        pygame.draw.rect(surface, (100, 0, 0), back_bar)
        pygame.draw.rect(surface, (0, 255, 0), current_bar)
    
    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)