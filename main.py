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
                        for room in random.sample(dungeon.rooms[1:], 3):
                            enemies.append(Enemy(*room.rect.center))
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
                    for room in random.sample(dungeon.rooms[1:], 6): #6 is number of enemies
                        enemies.append(Enemy(*room.rect.center))
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

        # TITLE SCREEN
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
