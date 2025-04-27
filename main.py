import pygame 
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAY
from game.player import Player, Projectile
from game.dungeon import Dungeon
from game.enemy import Enemy
from game.loot import Loot
from game.boss import Boss
from game.particle import Particle
from game.trap import Trap

# Game states
GAME_TITLE = "title"
GAME_CLASS_SELECT = "class_select"
GAME_RUNNING = "running"
GAME_OVER = "game_over"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ROGUELIKE DUNG")
    clock = pygame.time.Clock()

    darkness_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    game_state = GAME_TITLE
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)
    knight_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 220, 200, 50)
    ranger_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 290, 200, 50)
    wizard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 360, 200, 50)

    dungeon = None
    player = None
    enemies = []
    loot_drops = []
    projectiles = []
    particles = []
    traps = []
    boss = None
    wave_number = 1
    selected_class = "knight"

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == GAME_TITLE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.collidepoint(event.pos):
                        game_state = GAME_CLASS_SELECT

            elif game_state == GAME_CLASS_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if knight_button.collidepoint(event.pos):
                        selected_class = "knight"
                    elif ranger_button.collidepoint(event.pos):
                        selected_class = "ranger"
                    elif wizard_button.collidepoint(event.pos):
                        selected_class = "wizard"

                    dungeon = Dungeon()
                    player = Player(*dungeon.rooms[0].center(), player_class=selected_class)
                    wave_number = 1
                    enemies = []
                    loot_drops = []
                    projectiles = []
                    particles = []
                    traps = []
                    boss = None
                    enemy_types = ["normal", "fast", "tough"]
                    for room in random.sample(dungeon.rooms[1:], min(3 + wave_number, len(dungeon.rooms) - 1)):
                        x, y = room.rect.center
                        chosen_type = random.choice(enemy_types)
                        enemies.append(Enemy(x, y, enemy_type=chosen_type))
                    for room in dungeon.rooms[1:]:
                        if random.random() < 0.2:
                            traps.append(Trap(room.rect.centerx - 20, room.rect.centery - 20))
                    game_state = GAME_RUNNING

            elif game_state == GAME_RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player.class_type == "knight":
                            player.attack(enemies, projectiles, direction=None)
                            if boss and boss.alive:
                                attack_range = player.rect.inflate(40, 40)
                                if attack_range.colliderect(boss.rect):
                                    boss.take_damage(1)
                        else:
                            keys = pygame.key.get_pressed()
                            direction = None
                            if keys[pygame.K_LEFT]: direction = "left"
                            if keys[pygame.K_RIGHT]: direction = "right"
                            if keys[pygame.K_UP]: direction = "up"
                            if keys[pygame.K_DOWN]: direction = "down"

                            if direction:
                                player.attack(enemies, projectiles, direction)

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    game_state = GAME_CLASS_SELECT

        if game_state == GAME_RUNNING:
            walkable_areas = dungeon.get_walkable_rects()
            player.update(walkable_areas)

            for enemy in enemies:
                if enemy.alive:
                    enemy.update(player.rect.center, walkable_areas)
                    if enemy.rect.colliderect(player.rect):
                        player.take_damage(1)

            for loot in loot_drops:
                if not loot.collected and player.rect.colliderect(loot.rect):
                    loot.collected = True
                    if loot.type == "health":
                        player.health = min(player.max_health, player.health + 2)

            for projectile in projectiles[:]:
                projectile.update()
                for enemy in enemies:
                    if enemy.alive and projectile.rect.colliderect(enemy.rect):
                        enemy.take_damage(projectile.damage)
                        projectiles.remove(projectile)
                        for _ in range(10):
                            particles.append(Particle(enemy.rect.centerx, enemy.rect.centery, (200, 50, 50), size=5))
                        break
                if boss and boss.alive and projectile.rect.colliderect(boss.rect):
                    boss.take_damage(projectile.damage)
                    projectiles.remove(projectile)
                    for _ in range(20):
                        particles.append(Particle(boss.rect.centerx, boss.rect.centery, (255, 100, 0), size=7))

            if boss and boss.alive:
                boss.update(player.rect.center, walkable_areas)
                if boss.rect.colliderect(player.rect):
                    player.take_damage(2)

            for trap in traps[:]:
                if player.rect.colliderect(trap.rect):
                    player.take_damage(3)
                    traps.remove(trap)
                    break

            for particle in particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    particles.remove(particle)

            if player.health <= 0:
                game_state = GAME_OVER

            if all(not enemy.alive for enemy in enemies) and (not boss or not boss.alive):
                wave_number += 1
                dungeon = Dungeon()
                player.rect.center = dungeon.rooms[0].center()
                loot_drops = []
                projectiles = []
                particles = []
                traps = []
                if wave_number % 5 == 0:
                    boss = Boss(*dungeon.rooms[1].center())
                    enemies = []
                else:
                    enemies = []
                    enemy_types = ["normal", "fast", "tough"]
                    for room in random.sample(dungeon.rooms[1:], min(3 + wave_number, len(dungeon.rooms) - 1)):
                        x, y = room.rect.center
                        chosen_type = random.choice(enemy_types)
                        enemies.append(Enemy(x, y, enemy_type=chosen_type))
                for room in dungeon.rooms[1:]:
                    if random.random() < 0.2:
                        traps.append(Trap(room.rect.centerx - 20, room.rect.centery - 20))

            camera_x = player.rect.centerx - SCREEN_WIDTH // 2
            camera_y = player.rect.centery - SCREEN_HEIGHT // 2
            camera_offset = (camera_x, camera_y)

            screen.fill(GRAY)
            dungeon.draw(screen, camera_offset)

            for enemy in enemies:
                if enemy.alive:
                    enemy.draw(screen, camera_offset)
            if boss and boss.alive:
                boss.draw(screen, camera_offset)
            for loot in loot_drops:
                if not loot.collected:
                    loot.draw(screen, camera_offset)
            for projectile in projectiles:
                projectile.draw(screen, camera_offset)
            for trap in traps:
                trap.draw(screen, camera_offset)
            for particle in particles:
                particle.draw(screen, camera_offset)

            player.draw(screen, camera_offset)

            # DARKNESS EFFECT BEFORE HUD
            darkness_surface.fill((0, 0, 0, 220))
            light_radius = 250
            pygame.draw.circle(darkness_surface, (0, 0, 0, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), light_radius)
            screen.blit(darkness_surface, (0, 0))

            player.draw_health_bar(screen)

            font = pygame.font.SysFont(None, 36)
            wave_text = font.render(f"Wave: {wave_number}", True, (255, 255, 255))
            screen.blit(wave_text, (10, 40))

            minimap_size = 200
            minimap_surface = pygame.Surface((minimap_size, minimap_size))
            minimap_surface.fill((20, 20, 20))

            minimap_scale = 0.1
            mini_camera_offset = (player.rect.centerx - minimap_size // 2 / minimap_scale,
                                  player.rect.centery - minimap_size // 2 / minimap_scale)

            for room in dungeon.rooms:
                mini_rect = pygame.Rect(
                    int((room.rect.x - mini_camera_offset[0]) * minimap_scale),
                    int((room.rect.y - mini_camera_offset[1]) * minimap_scale),
                    int(room.rect.width * minimap_scale),
                    int(room.rect.height * minimap_scale)
                )
                if mini_rect.colliderect(minimap_surface.get_rect()):
                    pygame.draw.rect(minimap_surface, (80, 80, 80), mini_rect)

            player_dot = pygame.Rect(
                minimap_size // 2 - 2,
                minimap_size // 2 - 2,
                4, 4
            )
            pygame.draw.rect(minimap_surface, (0, 255, 0), player_dot)

            frame_rect = pygame.Rect(SCREEN_WIDTH - minimap_size - 12, 8, minimap_size + 4, minimap_size + 4)
            pygame.draw.rect(screen, (100, 100, 100), frame_rect)
            screen.blit(minimap_surface, (SCREEN_WIDTH - minimap_size - 10, 10))

        elif game_state == GAME_TITLE:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 72)
            title_text = font.render("ROGUELIKE DUNG", True, (200, 200, 200))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))

            mouse_pos = pygame.mouse.get_pos()
            button_color = (120, 120, 120) if start_button.collidepoint(mouse_pos) else (80, 80, 80)
            pygame.draw.rect(screen, button_color, start_button, border_radius=12)

            font_small = pygame.font.SysFont(None, 40)
            button_text = font_small.render("Start Game", True, (255, 255, 255))
            screen.blit(button_text, (start_button.centerx - button_text.get_width() // 2,
                                      start_button.centery - button_text.get_height() // 2))

        elif game_state == GAME_CLASS_SELECT:
            screen.fill((20, 20, 20))
            font = pygame.font.SysFont(None, 60)
            title_text = font.render("Choose Your Class", True, (255, 255, 255))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            mouse_pos = pygame.mouse.get_pos()

            knight_color = (140, 140, 255) if knight_button.collidepoint(mouse_pos) else (100, 100, 255)
            ranger_color = (140, 255, 140) if ranger_button.collidepoint(mouse_pos) else (100, 255, 100)
            wizard_color = (255, 140, 140) if wizard_button.collidepoint(mouse_pos) else (255, 100, 100)

            pygame.draw.rect(screen, knight_color, knight_button, border_radius=12)
            pygame.draw.rect(screen, ranger_color, ranger_button, border_radius=12)
            pygame.draw.rect(screen, wizard_color, wizard_button, border_radius=12)

            font_small = pygame.font.SysFont(None, 40)

            knight_text = font_small.render("Knight", True, (0, 0, 0))
            ranger_text = font_small.render("Ranger", True, (0, 0, 0))
            wizard_text = font_small.render("Wizard", True, (0, 0, 0))

            screen.blit(knight_text, (knight_button.centerx - knight_text.get_width() // 2,
                                      knight_button.centery - knight_text.get_height() // 2))
            screen.blit(ranger_text, (ranger_button.centerx - ranger_text.get_width() // 2,
                                      ranger_button.centery - ranger_text.get_height() // 2))
            screen.blit(wizard_text, (wizard_button.centerx - wizard_text.get_width() // 2,
                                      wizard_button.centery - wizard_text.get_height() // 2))

        elif game_state == GAME_OVER:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 60)
            text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
