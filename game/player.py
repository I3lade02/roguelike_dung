import pygame
import time
from config import PLAYER_COLOR

class Player:
    def __init__(self, x, y, size=32, speed=5, player_class="knight"):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.health = 5
        self.max_health = 5
        self.last_hit_time = 0
        self.hit_cooldown = 1.0
        self.attack_cooldown = 0.5
        self.last_attack = 0
        self.class_type = player_class

    def update(self, walkable_areas):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]: dx -= self.speed
        if keys[pygame.K_RIGHT]: dx += self.speed
        if keys[pygame.K_UP]: dy -= self.speed
        if keys[pygame.K_DOWN]: dy += self.speed

        new_rect = self.rect.move(dx, 0)
        if any(new_rect.colliderect(area) for area in walkable_areas):
            self.rect.x += dx
        new_rect = self.rect.move(0, dy)
        if any(new_rect.colliderect(area) for area in walkable_areas):
            self.rect.y += dy

    def take_damage(self, amount):
        now = time.time()
        if now - self.last_hit_time >= self.hit_cooldown:
            self.health -= amount
            self.last_hit_time = now

    def attack(self, enemies, projectiles, direction):
        now = time.time()
        if now - self.last_attack < self.attack_cooldown:
            return
        self.last_attack = now

        if self.class_type == "knight":
            # Melee attack
            attack_range = self.rect.inflate(40, 40)
            for enemy in enemies:
                if enemy.alive and attack_range.colliderect(enemy.rect):
                    enemy.take_damage(1)

        elif self.class_type == "ranger":
            # Shoot fast arrow
            projectiles.append(Projectile(self.rect.centerx, self.rect.centery, direction, speed=10, damage=1, color=(0, 255, 0)))

        elif self.class_type == "wizard":
            # Shoot slower fireball
            projectiles.append(Projectile(self.rect.centerx, self.rect.centery, direction, speed=6, damage=2, color=(255, 100, 0)))

    def draw(self, surface, camera_offset=(0, 0)):
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, PLAYER_COLOR, offset_rect)

    def draw_health_bar(self, surface):
        bar_width = 200
        bar_height = 20
        x, y = 10, 10
        health_ratio = max(self.health / self.max_health, 0)
        current_bar = pygame.Rect(x, y, int(bar_width * health_ratio), bar_height)
        back_bar = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(surface, (100, 0, 0), back_bar)
        pygame.draw.rect(surface, (0, 255, 0), current_bar)

class Projectile:
    def __init__(self, x, y, direction, speed, damage, color, size=8):
        self.rect = pygame.Rect(x, y, size, size)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.color = color

    def update(self):
        dx, dy = 0, 0
        if self.direction == "left": dx = -self.speed
        if self.direction == "right": dx = self.speed
        if self.direction == "up": dy = -self.speed
        if self.direction == "down": dy = self.speed

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface, camera_offset=(0, 0)):
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, self.color, offset_rect)
