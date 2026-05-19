import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera.x, self.camera.y)
        return entity.rect.move(self.camera.x, self.camera.y)


    def apply_pos(self, pos):
        return pos + pygame.math.Vector2(self.camera.x, self.camera.y)


    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        if self.width > SCREEN_WIDTH:
            x = min(0, x)  
            x = max(-(self.width - SCREEN_WIDTH), x)  
        else:
            x = (SCREEN_WIDTH - self.width) // 2

        if self.height > SCREEN_HEIGHT:
            y = min(0, y)  
            y = max(-(self.height - SCREEN_HEIGHT), y) 
        else:
            y = (SCREEN_HEIGHT - self.height) // 2

        self.camera = pygame.Rect(x, y, self.width, self.height)