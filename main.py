import pygame 
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAY
from game.player import Player
from game.dungeon import Dungeon
from game.enemy import Enemy

GAME_RUNNING = "running"
GAME_OVER = "game_over"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ROGUELIKE DUNG")
    clock = pygame.time.Clock()

    dungeon = Dungeon()
    start_x, start_y = dungeon.rooms[0].center()
    player = Player(x=start_x, y=start_y)

    enemies = []

    for room in random.sample(dungeon.rooms[1:], 3):
        x, y = room.rect.center
        enemies.append(Enemy(x, y))

    game_state = GAME_RUNNING
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == GAME_RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.attack(enemies)
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    #RESTART
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
            
            #Draw gameplay
            screen.fill(GRAY)
            dungeon.draw(screen)
            for enemy in enemies:
                if enemy.alive:
                    enemy.draw(screen)
            player.draw(screen)
            player.draw_health_bar(screen)

        elif game_state == GAME_OVER:
            screen.fill((10, 10, 10))
            font = pygame.font.SysFont(None, 60)
            text = font.render("GAME OVER - Press any key to restart", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()