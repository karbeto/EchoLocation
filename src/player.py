import pygame
from .settings import PLAYER_SPEED, PULSE_MAX_RADIUS
from .utils import Pulse

class Player:
    
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.pulses = []
        self.rect = pygame.Rect(x-10, y-10, 20, 20)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED

        if keys[pygame.K_SPACE]:
            self.emit_pulse()


    def emit_pulse(self):
        if len(self.pulses) < 5:
            self.pulses.append(Pulse(self.pos.x, self.pos.y, PULSE_MAX_RADIUS))


    def update(self):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        for pulse in self.pulses:
            pulse.update()
        self.pulses = [p for p in self.pulses if p.active]


    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 255), self.rect, 2)