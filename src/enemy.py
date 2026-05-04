import pygame
from .settings import ENEMY_SPEED, NEON_RED

class Enemy:
    
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(x-15, y-15, 30, 30)
        self.target_pos = None 
        
        
    def listen(self, player_pulses):
        for pulse in player_pulses:
            distance = self.pos.distance_to(pulse.pos)
            if distance < pulse.radius:
                self.target_pos = pygame.math.Vector2(pulse.pos.x, pulse.pos.y)


    def update(self, walls):
        if self.target_pos:
            direction = (self.target_pos - self.pos)
            
            if direction.length() > 5: 
                direction = direction.normalize()
                self.pos += direction * ENEMY_SPEED
                self.rect.center = (int(self.pos.x), int(self.pos.y))
                
                for wall in walls:
                    if self.rect.colliderect(wall):
                        self.target_pos = None 
            else:
                self.target_pos = None 


    def draw(self, surface):
        pygame.draw.rect(surface, NEON_RED, self.rect, 2)