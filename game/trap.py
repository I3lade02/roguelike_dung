import pygame

class Trap:
    def __init__(self, x, y, width=40, height=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False

    def draw(self, surface, camera_offset=(0, 0)):
        if self.visible:
            offset_x = self.rect.x - camera_offset[0]
            offset_y = self.rect.y - camera_offset[1]
            pygame.draw.rect(surface, (150, 0, 0), (offset_x, offset_y, self.rect.width, self.rect.height))