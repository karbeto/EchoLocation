import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, NEON_CYAN, NEON_GOLD, VISION_PERSISTENCE, NEON_ORANGE

class GameRenderer:
    
    def __init__(self):
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface.fill(BLACK)


    def clear_mask(self):
        self.mask_surface.fill(BLACK)


    def render_scene(self, screen, level, player, enemies, camera):
        self.world_surface.fill(BLACK)
        
        for wall in level.walls:
            pygame.draw.rect(self.world_surface, NEON_CYAN, camera.apply(wall), 1)
        
        for chime_wall in level.chime_walls:
            pygame.draw.rect(self.world_surface, NEON_ORANGE, camera.apply(chime_wall), 1)
        
        if not player.has_key and level.key_rect:
            pygame.draw.rect(self.world_surface, NEON_GOLD, camera.apply(level.key_rect), 3)
        
        if level.goal_rect:
            pygame.draw.rect(self.world_surface, (0, 255, 0), camera.apply(level.goal_rect), 2)
            
        for enemy in enemies:
            enemy.draw(self.world_surface, camera)
        
        player.draw(self.world_surface, camera)
        
        fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        decay_rate = max(2, min(VISION_PERSISTENCE, 6))
        fade_overlay.set_alpha(decay_rate) 
        fade_overlay.fill(BLACK)
        self.mask_surface.blit(fade_overlay, (0, 0))
        
        for pulse in player.pulses:
            shifted_pos = camera.apply_pos(pulse.pos)
            pygame.draw.circle(
                self.mask_surface, 
                (255, 255, 255), 
                (int(shifted_pos.x), int(shifted_pos.y)), 
                int(pulse.radius)
            )
            
        screen.blit(self.world_surface, (0, 0))
        screen.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_MULT)