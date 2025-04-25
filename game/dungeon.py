import pygame
import random
from config import LEVEL_WIDTH, LEVEL_HEIGHT

ROOM_MIN_SIZE = 400
ROOM_MAX_SIZE = 500
ROOM_COLOR = (30, 30, 30)
HALL_COLOR = (40, 40, 40)
NUM_ROOMS = 6

class Room:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def center(self):
        return (self.rect.centerx, self.rect.centery)

    def draw(self, surface, camera_offset=(0, 0)):
        offset_rect = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, ROOM_COLOR, offset_rect)

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.halls = []
        self.generate_rooms()

    def generate_rooms(self):
        for _ in range(NUM_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, LEVEL_WIDTH - w)
            y = random.randint(0, LEVEL_HEIGHT - h)
            new_room = Room(x, y, w, h)

            if self.rooms:
                prev_center = self.rooms[-1].center()
                new_center = new_room.center()
                self.create_hallway(prev_center, new_center)

            self.rooms.append(new_room)

    def create_hallway(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if random.choice([True, False]):
            self.halls.append(pygame.Rect(min(x1, x2), y1, abs(x2 - x1), 10))
            self.halls.append(pygame.Rect(x2, min(y1, y2), 10, abs(y2 - y1)))
        else:
            self.halls.append(pygame.Rect(x1, min(y1, y2), 10, abs(y2 - y1)))
            self.halls.append(pygame.Rect(min(x1, x2), y2, abs(x2 - x1), 10))

    def get_walkable_rects(self):
        return [room.rect for room in self.rooms] + self.halls

    def draw(self, surface, camera_offset=(0, 0)):
        for hall in self.halls:
            offset_rect = hall.move(-camera_offset[0], -camera_offset[1])
            pygame.draw.rect(surface, HALL_COLOR, offset_rect)
        for room in self.rooms:
            room.draw(surface, camera_offset)
