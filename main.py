import pygame 
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAY
from game.player import Player
from game.dungeon import Dungeon
from game.enemy import Enemy

# Game states
GAME_TITLE = "title"
GAME_RUNNING = "running"
GAME_OVER = "game_over"
GAME_WIN = "win"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ROGUELIKE DUNG")
    clock = pygame.time.Clock()

    game_state = GAME_TITLE
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 60)

    dungeon = None
    player = None
    enemies = []

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Title screen input
            if game_state == GAME_TITLE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.collidepoint(event.pos):
                        dungeon = Dungeon()
                        player = Player(*dungeon.rooms[0].center())
                        enemies = []
                        enemy_types = ["normal", "fast", "tough"]
                        for room in random.sample(dungeon.rooms[1:], min(6, len(dungeon.rooms) - 1)): #number of enemies on game start
                           x, y = room.rect.center
                           chosen_type = random.choice(enemy_types)
                           enemies.append(Enemy(x,y,enemy_type=chosen_type))
                        game_state = GAME_RUNNING

            # Running state input
            elif game_state == GAME_RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.attack(enemies)

            # Restart on Game Over or Win
            elif game_state in [GAME_OVER, GAME_WIN]:
                if event.type == pygame.KEYDOWN:
                    dungeon = Dungeon()
                    player = Player(*dungeon.rooms[0].center())
                    enemies = []
                    enemy_types = ["normal", "fast", "tough"]
                    for room in random.sample(dungeon.rooms[1:], min(6, len(dungeon.rooms) - 1)): #6 is number of enemies
                        x,y = room.rect.center
                        chosen_type = random.choice(enemy_types)
                        enemies.append(Enemy(x, y, enemy_type=chosen_type))
                    game_state = GAME_RUNNING

        # GAME RUNNING LOGIC
        if game_state == GAME_RUNNING:
            walkable_areas = dungeon.get_walkable_rects()
            player.update(walkable_areas)
            for enemy in enemies:
                if enemy.alive:
                    enemy.update(player.rect.center, walkable_areas)
                    if enemy.rect.colliderect(player.rect):
                        player.take_damage(1)

            if player.health <= 0:
                game_state = GAME_OVER

            if all(not enemy.alive for enemy in enemies):
                game_state = GAME_WIN

            # Camera follows player
            camera_x = player.rect.centerx - SCREEN_WIDTH // 2
            camera_y = player.rect.centery - SCREEN_HEIGHT // 2
            camera_offset = (camera_x, camera_y)

            # Draw gameplay
            screen.fill(GRAY)
            dungeon.draw(screen, camera_offset)
            for enemy in enemies:
                if enemy.alive:
                    enemy.draw(screen, camera_offset)
            player.draw(screen, camera_offset)
            player.draw_health_bar(screen)

        #Minimap
            minimap_scale = 0.15
            minimap_width = int(1920 * minimap_scale)
            minimap_height = int(1080 * minimap_scale)
            minimap_surface = pygame.Surface((minimap_width, minimap_height))
            minimap_surface.fill((20, 20, 20))

            for room in dungeon.rooms:
                scaled_rect = pygame.Rect(
                    int(room.rect.x * minimap_scale),
                    int(room.rect.y * minimap_scale),
                    int(room.rect.width * minimap_scale),
                    int(room.rect.height * minimap_scale)
                )
                pygame.draw.rect(minimap_surface, (80, 80, 80), scaled_rect)

            player_dot = pygame.Rect(
                int(player.rect.centerx * minimap_scale) - 2,
                int(player.rect.centery * minimap_scale) - 2,
                4, 4
            )
            pygame.draw.rect(minimap_surface, (0, 255, 0), player_dot)

            screen.blit(minimap_surface, (SCREEN_WIDTH - minimap_width - 10, 10))

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

        # GAME OVER SCREEN
        elif game_state == GAME_OVER:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 60)
            text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        # VICTORY SCREEN
        elif game_state == GAME_WIN:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 60)
            win_text = font.render("YOU WIN!", True, (0, 255, 0))
            prompt = pygame.font.SysFont(None, 40).render("Press any key to play again", True, (180, 180, 180))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 200))
            screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 280))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
