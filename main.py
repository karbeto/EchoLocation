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
        
        # Load Level first to get spawn positions
        self.level = Level('levels/level1.txt')
        
        # Initial setup
        self._reset_game()
        
        # Surfaces for the vision system
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface.fill(BLACK)

    def _reset_game(self):
        """Resets the state of the game without reloading the whole script."""
        # Initialize entities using level data
        self.player = Player(*self.level.player_spawn_pos)
        self.enemies = [Enemy(pos[0], pos[1]) for pos in self.level.enemies_spawn_pos]
        
        # Clear the mask so previous vision doesn't carry over
        if hasattr(self, 'mask_surface'):
            self.mask_surface.fill(BLACK)

    def _draw_world(self):
        """Draws the absolute truth of the game world."""
        self.world_surface.fill(BLACK)
        
        # Draw static level geometry
        self.level.draw(self.world_surface)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.world_surface)
            
        # Draw player
        self.player.draw(self.world_surface)

    def _apply_mask(self):
        """Filters the world through the player's 'memory' and pulses."""
        # Create the fading effect (Memory)
        fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_overlay.set_alpha(VISION_PERSISTENCE) 
        fade_overlay.fill(BLACK)
        self.mask_surface.blit(fade_overlay, (0, 0))
        
        # Punch holes in the mask for every active pulse
        for pulse in self.player.pulses:
            pulse.draw(self.mask_surface)
            
        # Blit truth to screen
        self.screen.blit(self.world_surface, (0, 0))
        # Multiply screen by mask (Black = hidden, White = visible)
        self.screen.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_MULT)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 1. Input handling
            self.player.handle_input()
            
            # 2. Update Logic
            self.player.update(self.level.walls)
            
            for enemy in self.enemies:
                enemy.listen(self.player.pulses)
                enemy.update(self.level.walls)
                
                # COLLISION CHECK: Did the enemy catch the player?
                if self.player.rect.colliderect(enemy.rect):
                    print("CAUGHT! Respawning...")
                    self._reset_game()
            
            # 3. Rendering
            self._draw_world()
            self._apply_mask()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = EchoLocation()
    game.run()
