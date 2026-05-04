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
        self.font = pygame.font.SysFont("Arial", 32)
        
        self.state = STATE_MENU
        
        self.level = Level('levels/level1.txt')
        
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self._reset_game()

    def _reset_game(self):
        self.player = Player(*self.level.player_spawn_pos)
        self.enemies = [Enemy(pos[0], pos[1]) for pos in self.level.enemies_spawn_pos]
        self.mask_surface.fill(BLACK)


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                
                elif self.state in [STATE_GAMEOVER, STATE_WIN]:
                    if event.key == pygame.K_SPACE:
                        self._reset_game()
                        self.state = STATE_PLAYING


    def _update_game(self):
        self.player.handle_input()
        self.player.update(self.level.walls)
        
        for enemy in self.enemies:
            enemy.listen(self.player.pulses)
            enemy.update(self.level.walls, self.player.pos)
            
            if self.player.rect.colliderect(enemy.rect):
                self.state = STATE_GAMEOVER
                
        if self.level.goal_rect and self.player.rect.colliderect(self.level.goal_rect):
            self.state = STATE_WIN


    def _draw_menu_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("ECHO LOCATION: PRESS SPACE TO START", True, NEON_CYAN)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)


    def _draw_gameover_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("CAUGHT IN THE DARK. PRESS SPACE TO RETRY", True, NEON_RED)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)


    def _draw_win_screen(self):
        self.screen.fill(BLACK)
        text = self.font.render("YOU FOUND THE LIGHT! PRESS SPACE TO PLAY AGAIN", True, NEON_GOLD)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)


    def _draw_playing_screen(self):
        self.world_surface.fill(BLACK)
        self.level.draw(self.world_surface)
        for enemy in self.enemies:
            enemy.draw(self.world_surface)
        self.player.draw(self.world_surface)
        
        fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_overlay.set_alpha(VISION_PERSISTENCE) 
        fade_overlay.fill(BLACK)
        self.mask_surface.blit(fade_overlay, (0, 0))
        
        for pulse in self.player.pulses:
            pulse.draw(self.mask_surface)
            
        self.screen.blit(self.world_surface, (0, 0))
        self.screen.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_MULT)
        
        self._draw_ui()


    def _draw_ui(self):
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - self.player.last_pulse_time) / PULSE_COOLDOWN)
        bar_width = 200
        pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width, 10))
        pygame.draw.rect(self.screen, NEON_CYAN, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width * progress, 10))


    def run(self):
        while True:
            self._handle_events()
            
            if self.state == STATE_PLAYING:
                self._update_game()
                self._draw_playing_screen()
            elif self.state == STATE_MENU:
                self._draw_menu_screen()
            elif self.state == STATE_GAMEOVER:
                self._draw_gameover_screen()
            elif self.state == STATE_WIN:
                self._draw_win_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = EchoLocation()
    game.run()
