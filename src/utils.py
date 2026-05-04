import pygame
from .settings import PULSE_EXPANSION_SPEED, PULSE_FADE_RATE, WHITE

class Pulse:
    
    def __init__(self, x, y, max_radius):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = 0
        self.max_radius = max_radius
        self.alpha = 255
        self.active = True


    def update(self):
        # Expand the radius
        self.radius += PULSE_EXPANSION_SPEED
        
        # Fade out as it expands
        self.alpha -= PULSE_FADE_RATE
        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.alpha = 0
            self.active = False


    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, (self.alpha, self.alpha, self.alpha), 
                               self.pos, self.radius, width=2)