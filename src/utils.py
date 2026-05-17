import pygame
from .settings import PULSE_EXPANSION_SPEED, PULSE_FADE_RATE, WHITE

class Pulse:
    
    def __init__(self, x, y, max_radius):
        self.pos = pygame.math.Vector2(x, y)
        self.radius = 0
        self.max_radius = max_radius
        self.alpha = 255
        self.active = True
        self.triggered_hazards = set() 


    def update(self, chime_walls, audio_manager):
        self.radius += PULSE_EXPANSION_SPEED
        self.alpha -= PULSE_FADE_RATE
        
        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.alpha = 0
            self.active = False
            return

        for hazard in chime_walls:
            hazard_id = (hazard.x, hazard.y)
            if hazard_id in self.triggered_hazards:
                continue

            closest_x = max(hazard.left, min(self.pos.x, hazard.right))
            closest_y = max(hazard.top, min(self.pos.y, hazard.bottom))

            dx = self.pos.x - closest_x
            dy = self.pos.y - closest_y
            distance_squared = (dx * dx) + (dy * dy)

            if distance_squared <= (self.radius * self.radius):
                self.triggered_hazards.add(hazard_id)
                
                audio_manager.play_effect('key_found', volume=0.5) 
            

    def draw(self, surface):
        if self.active:
            color = (self.alpha, self.alpha, self.alpha)
            pygame.draw.circle(surface, color, self.pos, self.radius, width=3)