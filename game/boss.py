import pygame

class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 96, 96)  # Boss is BIG
        self.health = 30
        self.max_health = 30
        self.speed = 2
        self.alive = True

    def update(self, target_pos, walkable_areas):
        if not self.alive:
            return

        dx = dy = 0
        if self.rect.centerx < target_pos[0]:
            dx = self.speed
        elif self.rect.centerx > target_pos[0]:
            dx = -self.speed

        if self.rect.centery < target_pos[1]:
            dy = self.speed
        elif self.rect.centery > target_pos[1]:
            dy = -self.speed

        new_rect_x = self.rect.move(dx, 0)
        if any(new_rect_x.colliderect(area) for area in walkable_areas):
            self.rect.x += dx
        new_rect_y = self.rect.move(0, dy)
        if any(new_rect_y.colliderect(area) for area in walkable_areas):
            self.rect.y += dy

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def draw(self, surface, camera_offset=(0, 0)):
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, (255, 0, 0), offset_rect)

        # Draw Boss Health Bar above boss
        health_bar_width = 150
        health_bar_height = 10
        bar_x = offset_rect.centerx - health_bar_width // 2
        bar_y = offset_rect.top - 20

        pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, health_bar_width, health_bar_height))  # Background
        health_ratio = max(self.health / self.max_health, 0)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, int(health_bar_width * health_ratio), health_bar_height))  # Health
