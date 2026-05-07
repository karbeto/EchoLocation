import pygame
import sys
from src.settings import *
from src.player import Player
from src.enemy import Enemy
from src.level import Level
from src.audio_manager import AudioManager 
from src.camera import Camera

class EchoLocation:
    
    def __init__(self):
        pygame.init()
        self.audio_manager = AudioManager() 
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        
        self.level_files = ['levels/level1.txt', 'levels/level2.txt', 'levels/level3.txt']
        self.current_level_idx = 0
        self.state = STATE_MENU
        
        self.level = Level(self.level_files[self.current_level_idx])
        self.camera = Camera(self.level.width, self.level.height)
        
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self._reset_game()


    def _reset_game(self):
        self.player = Player(*self.level.player_spawn_pos, self.audio_manager)
        self.enemies = [
            Enemy(pos[0], pos[1], self.audio_manager) 
            for pos in self.level.enemies_spawn_pos
        ]
        self.mask_surface.fill(BLACK)
        self.player.has_key = False
        self.camera.update(self.player)


    def _next_level(self):
        self.current_level_idx += 1
        
        if self.current_level_idx < len(self.level_files):
            self.audio_manager.play_effect('level_finish') 
            self.level = Level(self.level_files[self.current_level_idx])
            self.camera = Camera(self.level.width, self.level.height)
            self._reset_game()
            self.state = STATE_PLAYING
            print(f"Advancing to Level {self.current_level_idx + 1}")
        else:
            self.audio_manager.play_effect('level_finish')
            self.state = STATE_WIN


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                
                elif self.state == STATE_GAMEOVER:
                    if event.key == pygame.K_SPACE:
                        self._reset_game()
                        self.state = STATE_PLAYING
                
                elif self.state == STATE_WIN:
                    if event.key == pygame.K_SPACE:
                        self.current_level_idx = 0
                        self.level = Level(self.level_files[self.current_level_idx])
                        self.camera = Camera(self.level.width, self.level.height)
                        self._reset_game()
                        self.state = STATE_PLAYING


    def _update_game(self):
        self.player.handle_input()
        self.player.update(self.level.walls)
        self.camera.update(self.player)
        
        if not self.player.has_key and self.level.key_rect:
            if self.player.rect.colliderect(self.level.key_rect):
                self.player.has_key = True
                self.audio_manager.play_effect('key_found') 
                print("KEY COLLECTED!")

        for enemy in self.enemies:
            enemy.listen(self.player.pulses)
            enemy.update(self.level.walls, self.player.pos)
            
            if self.player.rect.colliderect(enemy.rect):
                self.state = STATE_GAMEOVER
        
        if self.level.goal_rect and self.player.rect.colliderect(self.level.goal_rect):
            if self.player.has_key:
                self._next_level()


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
        text = self.font.render("ALL LEVELS CLEAR. PRESS SPACE TO RESTART", True, NEON_GOLD)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, rect)


    def _draw_playing_screen(self):
        self.world_surface.fill(BLACK)
        
        for wall in self.level.walls:
            pygame.draw.rect(self.world_surface, NEON_CYAN, self.camera.apply(wall), 1)
        
        if not self.player.has_key and self.level.key_rect:
            pygame.draw.rect(self.world_surface, NEON_GOLD, self.camera.apply(self.level.key_rect), 3)
        
        if self.level.goal_rect:
            pygame.draw.rect(self.world_surface, (0, 255, 0), self.camera.apply(self.level.goal_rect), 2)
            
        for enemy in self.enemies:
            enemy.draw(self.world_surface, self.camera)
        
        self.player.draw(self.world_surface, self.camera)
        
        fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_overlay.set_alpha(VISION_PERSISTENCE) 
        fade_overlay.fill(BLACK)
        self.mask_surface.blit(fade_overlay, (0, 0))
        
        for pulse in self.player.pulses:
            shifted_pos = self.camera.apply_pos(pulse.pos)
            pygame.draw.circle(self.mask_surface, (255, 255, 255), 
                             (int(shifted_pos.x), int(shifted_pos.y)), 
                             int(pulse.radius))
            
        self.screen.blit(self.world_surface, (0, 0))
        self.screen.blit(self.mask_surface, (0, 0), special_flags=pygame.BLEND_MULT)
        
        self._draw_ui()


    def _draw_ui(self):
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - self.player.last_pulse_time) / PULSE_COOLDOWN)
        bar_width = 200
        
        pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width, 10))
        pygame.draw.rect(self.screen, NEON_CYAN, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width * progress, 10))
        
        lvl_text = self.font.render(f"Level {self.current_level_idx + 1}", True, WHITE)
        self.screen.blit(lvl_text, (20, SCREEN_HEIGHT - 50))
        
        if self.player.has_key:
            key_text = self.font.render("KEY: ACQUIRED", True, NEON_GOLD)
            self.screen.blit(key_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 50))
        else:
            key_text = self.font.render("KEY: REQUIRED", True, (100, 100, 100))
            self.screen.blit(key_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 50))


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