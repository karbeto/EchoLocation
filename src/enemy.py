import pygame
import random
from .settings import *

class Enemy:
    
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        self.target_pos = None
        self.is_chasing = False
        self.chase_timer = 0 
        
        self.start_pos = pygame.math.Vector2(x, y)
        self.patrol_target = pygame.math.Vector2(x, y)
        self._pick_new_patrol()

    def _pick_new_patrol(self):
        angle = random.uniform(0, 360)
        distance = random.randint(150, 400)
        offset = pygame.math.Vector2()
        offset.from_polar((distance, angle))
        self.patrol_target = self.start_pos + offset

    def listen(self, pulses):
        for pulse in pulses:
            dist = self.pos.distance_to(pulse.pos)
            if dist < pulse.radius:
                self.target_pos = pygame.math.Vector2(pulse.pos.x, pulse.pos.y)
                self.is_chasing = True
                self.chase_timer = 180  


    def update(self, walls, player_pos):
        dist_to_player = self.pos.distance_to(player_pos)
        if dist_to_player < 120: 
            self.target_pos = pygame.math.Vector2(player_pos.x, player_pos.y)
            self.is_chasing = True
            self.chase_timer = 120 

        if self.chase_timer > 0:
            self.chase_timer -= 1
        elif self.is_chasing:
            self.is_chasing = False
            self.target_pos = None

        if self.is_chasing and self.target_pos:
            move_target = self.target_pos
            current_speed = ENEMY_SPEED 
        else:
            move_target = self.patrol_target
            current_speed = ENEMY_SPEED * 0.5 

        direction = (move_target - self.pos)
        if direction.length() > 5:
            direction = direction.normalize()
            new_pos = self.pos + direction * current_speed
            
            temp_rect = self.rect.copy()
            temp_rect.center = (int(new_pos.x), int(new_pos.y))
            
            if not any(temp_rect.colliderect(wall) for wall in walls):
                self.pos = new_pos
                self.rect.center = (int(self.pos.x), int(self.pos.y))
            else:
                if self.is_chasing:
                    self.target_pos = None
                    self.chase_timer = 0
                else:
                    self._pick_new_patrol()
        else:
            if not self.is_chasing:
                self._pick_new_patrol()
            else:
                self.target_pos = None


    def draw(self, surface):
        pygame.draw.rect(surface, NEON_RED, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)