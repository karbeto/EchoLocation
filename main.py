import pygame
import sys
from src.settings import *
from src.player import Player

class EchoLocation:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


    def _draw_world(self):
        self.world_surface.fill(BLACK)
        pygame.draw.rect(self.world_surface, NEON_CYAN, (300, 200, 50, 300), 2)
        pygame.draw.circle(self.world_surface, NEON_RED, (900, 400), 40, 2)
        self.player.draw(self.world_surface)


    def _apply_mask(self):
        
        self.mask_surface.fill(BLACK)
        
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
            self.player.update()
            
            self._draw_world()
            self._apply_mask()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = EchoLocation()
    game.run()
