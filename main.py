import pygame 
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAY
from game.player import Player
from game.dungeon import Dungeon
from game.enemy import Enemy

GAME_TITLE = "title"
GAME_RUNNING = "running"
GAME_OVER = "game_over"

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

            if game_state == GAME_TITLE:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button.collidepoint(event.pos):
                        # Initialize game
                        dungeon = Dungeon()
                        player = Player(*dungeon.rooms[0].center())
                        enemies = []
                        for room in random.sample(dungeon.rooms[1:], 6): #num 6 is the number of enemies
                            enemies.append(Enemy(*room.rect.center))
                        game_state = GAME_RUNNING

            elif game_state == GAME_RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.attack(enemies)

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    # Restart game
                    dungeon = Dungeon()
                    player = Player(*dungeon.rooms[0].center())
                    enemies = []
                    for room in random.sample(dungeon.rooms[1:], 3):
                        enemies.append(Enemy(*room.rect.center))
                    game_state = GAME_RUNNING

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

            screen.fill(GRAY)
            dungeon.draw(screen)
            for enemy in enemies:
                if enemy.alive:
                    enemy.draw(screen)
            player.draw(screen)
            player.draw_health_bar(screen)

        elif game_state == GAME_TITLE:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 72)
            title_text = font.render("ROGUELIKE DUNG", True, (200, 200, 200))
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 180))

            #Check hover
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                button_color = (120, 120, 120)
            else:
                button_color = (80, 80, 80)

            pygame.draw.rect(screen, button_color, start_button, border_radius=12)
            font_small = pygame.font.SysFont(None, 40)
            button_text = font_small.render("Start Game", True, (255, 255, 255))
            screen.blit(button_text, (start_button.centerx - button_text.get_width() // 2,
                                      start_button.centery - button_text.get_height() // 2))

        elif game_state == GAME_OVER:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 60)
            text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
