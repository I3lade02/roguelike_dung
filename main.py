import pygame 
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAY
from game.player import Player
from game.dungeon import Dungeon
from game.enemy import Enemy

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

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.attack(enemies)

        #update
        walkable_areas = dungeon.get_walkable_rects()
        player.update(walkable_areas)
        for enemy in enemies:
            if enemy.alive:
                enemy.update(player.rect.center, walkable_areas)
            
        #draw
        screen.fill(GRAY)
        for room in dungeon.rooms:
            room.draw(screen)
        for hall in dungeon.halls:
            pygame.draw.rect(screen, (40, 40, 40), hall)
        
        player.draw(screen)
        player.draw_health_bar(screen)
        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()