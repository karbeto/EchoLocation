import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.topleft)
        return entity.rect.move(self.camera.topleft)


    def apply_pos(self, pos):
        return pos + pygame.math.Vector2(self.camera.topleft)


    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.width - SCREEN_WIDTH), x)  
        y = max(-(self.height - SCREEN_HEIGHT), y) 

        self.camera = pygame.Rect(x, y, self.width, self.height)