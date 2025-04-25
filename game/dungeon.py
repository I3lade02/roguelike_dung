import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

ROOM_MIN_SIZE = 100
ROOM_MAX_SIZE = 200
ROOM_COLOR = (30, 30, 30)
HALL_COLOR = (40, 40, 40)
NUM_ROOMS = 12

class Room:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def center(self):
        return (self.rect.centerx, self.rect.centery)

    def draw(self, surface):
        pygame.draw.rect(surface, ROOM_COLOR, self.rect)

class Dungeon:
    def __init__(self):
        self.rooms = []
        self.halls = []
        self.generate_rooms()

    def generate_rooms(self):
        for _ in range(NUM_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, SCREEN_WIDTH - w)
            y = random.randint(0, SCREEN_HEIGHT - h)
            new_room = Room(x, y, w, h)

            # Connect to previous room
            if self.rooms:
                prev_center = self.rooms[-1].center()
                new_center = new_room.center()
                self.create_hallway(prev_center, new_center)

            self.rooms.append(new_room)

    def create_hallway(self, start, end):
        x1, y1 = start
        x2, y2 = end

        # Random L-shape connection
        if random.choice([True, False]):
            self.halls.append(pygame.Rect(min(x1, x2), y1, abs(x2 - x1), 10))  # horizontal
            self.halls.append(pygame.Rect(x2, min(y1, y2), 10, abs(y2 - y1)))  # vertical
        else:
            self.halls.append(pygame.Rect(x1, min(y1, y2), 10, abs(y2 - y1)))
            self.halls.append(pygame.Rect(min(x1, x2), y2, abs(x2 - x1), 10))

    def draw(self, surface):
        for hall in self.halls:
            pygame.draw.rect(surface, HALL_COLOR, hall)
        for room in self.rooms:
            room.draw(surface)

    def get_walkable_rects(self):
        return [room.rect for room in self.rooms] + self.halls
