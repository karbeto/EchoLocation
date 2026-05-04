import pygame
import sys
from src.settings import *
from src.player import Player
from src.enemy import Enemy
from src.level import Level

class EchoLocation:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.level = Level('levels/level1.txt')
        
        self._reset_game()
        
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface.fill(BLACK)


    def _reset_game(self):
        self.player = Player(*self.level.player_spawn_pos)
        self.enemies = [Enemy(pos[0], pos[1]) for pos in self.level.enemies_spawn_pos]
        
        if hasattr(self, 'mask_surface'):
            self.mask_surface.fill(BLACK)


    def _draw_world(self):
        self.world_surface.fill(BLACK)
        
        self.level.draw(self.world_surface)
        
        for enemy in self.enemies:
            enemy.draw(self.world_surface)
            
        self.player.draw(self.world_surface)
        
    def _draw_ui(self):
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - self.player.last_pulse_time) / PULSE_COOLDOWN)
        
        bar_width = 200
        pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width, 10))
        pygame.draw.rect(self.screen, NEON_CYAN, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width * progress, 10))


    def _apply_mask(self):
        fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_overlay.set_alpha(VISION_PERSISTENCE) 
        fade_overlay.fill(BLACK)
        self.mask_surface.blit(fade_overlay, (0, 0))
        
        for pulse in self.player.pulses:
            pulse.draw(self.mask_surface)
            
        self.screen.blit(self.world_surface, (0, 0))
        self.screen.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_MULT)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.handle_input()
            
            self.player.update(self.level.walls)
            
            for enemy in self.enemies:
                enemy.listen(self.player.pulses)
                enemy.update(self.level.walls, self.player.pos)
                
                if self.player.rect.colliderect(enemy.rect):
                    print("CAUGHT! Respawning...")
                    self._reset_game()
                    
                if self.level.goal_rect and self.player.rect.colliderect(self.level.goal_rect):
                    print("LEVEL COMPLETE!")
                    self._reset_game()
            
            self._draw_world()
            self._apply_mask()
            self._draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = EchoLocation()
    game.run()
