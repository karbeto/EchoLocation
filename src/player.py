import pygame
from .settings import PLAYER_SPEED, PULSE_COOLDOWN, PULSE_MAX_RADIUS, NEON_GOLD
from .utils import Pulse

class Player:
    
    def __init__(self, x, y, audio_manager):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.pulses = []
        self.rect = pygame.Rect(x-10, y-10, 20, 20)
        self.last_pulse_time = 0
        self.has_key = False
        
        # Audio integration
        self.audio_manager = audio_manager
        self.footstep_delay = 350  # milliseconds between footstep sounds
        self.last_footstep_time = 0


    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        self.vel.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.vel.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
            
            # Play footstep sound if moving
            current_time = pygame.time.get_ticks()
            if current_time - self.last_footstep_time > self.footstep_delay:
                self.audio_manager.play_effect('footsteps', volume=0.3)
                self.last_footstep_time = current_time
        
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.last_pulse_time > PULSE_COOLDOWN:
            self.emit_pulse()
            self.last_pulse_time = current_time


    def emit_pulse(self):
        if len(self.pulses) < 3: 
            self.pulses.append(Pulse(self.pos.x, self.pos.y, PULSE_MAX_RADIUS))
            # Trigger the pulse sound
            self.audio_manager.play_pulse(0)
          
          
    def _handle_collision(self, walls, direction):
        for wall in walls:
            if self.rect.colliderect(wall):
                if direction == 'x':
                    if self.vel.x > 0: self.rect.right = wall.left
                    if self.vel.x < 0: self.rect.left = wall.right
                    self.pos.x = self.rect.centerx
                if direction == 'y':
                    if self.vel.y > 0: self.rect.bottom = wall.top
                    if self.vel.y < 0: self.rect.top = wall.bottom
                    self.pos.y = self.rect.centery


    def update(self, walls):
        self.pos.x += self.vel.x
        self.rect.centerx = int(self.pos.x)
        self._handle_collision(walls, 'x')

        self.pos.y += self.vel.y
        self.rect.centery = int(self.pos.y)
        self._handle_collision(walls, 'y')
        
        for pulse in self.pulses:
            pulse.update()
        self.pulses = [p for p in self.pulses if p.active]


    def draw(self, surface):
        if self.has_key:
            pygame.draw.circle(surface, NEON_GOLD, self.rect.center, 5)
            
        pygame.draw.rect(surface, (0, 255, 255), self.rect, 2)