import pygame
import sys
from src.settings import *
from src.player import Player
from src.enemy import Enemy
from src.level import Level
from src.audio_manager import AudioManager 
from src.camera import Camera
from src.maze_generator import MazeGenerator
from src.shop import ShopManager

class EchoLocation:
    
    def __init__(self):
        pygame.init()
        self.audio_manager = AudioManager() 
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.shop_font = pygame.font.SysFont("Arial", 24)
        
        self.level_files = ['levels/level1.txt', 'levels/level2.txt', 'levels/level3.txt']
        self.current_level_idx = 0
        self.state = STATE_MENU
        
        self.current_xp = 0
        self.generator = MazeGenerator(width=25, height=13) 
        
        self.shop_manager = ShopManager()
        
        self.level = Level(self.level_files[self.current_level_idx])
        self.camera = Camera(self.level.width, self.level.height)
        
        self.world_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self._reset_game()


    def _reset_game(self):
        dynamic_radius = PULSE_MAX_RADIUS * self.shop_manager.get_radius_modifier()
        dynamic_cooldown = PULSE_COOLDOWN * self.shop_manager.get_cooldown_modifier()
        
        self.player = Player(*self.level.player_spawn_pos, self.audio_manager, dynamic_radius, dynamic_cooldown)
        self.player.xp = self.current_xp
        
        self.enemies = [
            Enemy(pos[0], pos[1], self.audio_manager) 
            for pos in self.level.enemies_spawn_pos
        ]
        self.mask_surface.fill(BLACK)
        self.player.has_key = False
        self.camera.update(self.player)


    def _next_level(self):
        self.current_level_idx += 1
        self.current_xp += 10
        
        self.audio_manager.play_effect('level_finish') 
        
        if self.current_level_idx < len(self.level_files):
            self.level = Level(self.level_files[self.current_level_idx])
            print(f"Advancing to Static Level {self.current_level_idx + 1}")
        else:
            procedural_layout = self.generator.generate(self.current_level_idx + 1)
            self.level = Level(procedural_layout)
            print(f"Advancing to Procedural Level {self.current_level_idx + 1}")
            
        self.camera = Camera(self.level.width, self.level.height)
        self._reset_game()
        self.state = STATE_PLAYING


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
                        self.current_xp = 0 
                        self.level = Level(self.level_files[self.current_level_idx])
                        self.camera = Camera(self.level.width, self.level.height)
                        self._reset_game()
                        self.state = STATE_PLAYING

                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_e:
                        self.state = STATE_SHOP
                        
                elif self.state == STATE_SHOP:
                    if event.key == pygame.K_e:
                        self.state = STATE_PLAYING
                    
                    elif event.key == pygame.K_1:
                        success, self.current_xp = self.shop_manager.try_upgrade_radius(self.current_xp)
                        if success:
                            self.player.xp = self.current_xp
                            self.player.max_radius = PULSE_MAX_RADIUS * self.shop_manager.get_radius_modifier()
                            
                    elif event.key == pygame.K_2:
                        success, self.current_xp = self.shop_manager.try_upgrade_cooldown(self.current_xp)
                        if success:
                            self.player.xp = self.current_xp
                            self.player.cooldown = PULSE_COOLDOWN * self.shop_manager.get_cooldown_modifier()


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

    def _draw_shop_overlay(self):
        self._draw_playing_screen()
        
        shop_panel = pygame.Surface((460, 260))
        shop_panel.fill((10, 15, 20))
        pygame.draw.rect(shop_panel, NEON_CYAN, (0, 0, 460, 260), 2)
        
        cost_r = self.shop_manager.get_upgrade_cost(self.shop_manager.radius_level)
        cost_c = self.shop_manager.get_upgrade_cost(self.shop_manager.cooldown_level)
        
        lvl_r = f"Lvl {self.shop_manager.radius_level}/5" if self.shop_manager.radius_level < 5 else "MAX"
        lvl_c = f"Lvl {self.shop_manager.cooldown_level}/5" if self.shop_manager.cooldown_level < 5 else "MAX"
        
        title_txt = self.font.render("ECHO MODIFICATIONS", True, NEON_CYAN)
        xp_txt = self.shop_font.render(f"Available XP Balance: {self.current_xp}", True, WHITE)
        
        opt1_txt = self.shop_font.render(f"[1] Sonar Amplifier ({lvl_r}) - Cost: {cost_r} XP", True, NEON_GOLD if self.shop_manager.radius_level < 5 else (100,100,100))
        opt2_txt = self.shop_font.render(f"[2] Frequency Booster ({lvl_c}) - Cost: {cost_c} XP", True, NEON_GOLD if self.shop_manager.cooldown_level < 5 else (100,100,100))
        exit_txt = self.shop_font.render("[E] Resume Mission Tracker", True, WHITE)
        
        shop_panel.blit(title_txt, (30, 20))
        shop_panel.blit(xp_txt, (30, 70))
        shop_panel.blit(opt1_txt, (30, 120))
        shop_panel.blit(opt2_txt, (30, 160))
        shop_panel.blit(exit_txt, (30, 210))
        
        panel_x = (SCREEN_WIDTH - 460) // 2
        panel_y = (SCREEN_HEIGHT - 260) // 2
        self.screen.blit(shop_panel, (panel_x, panel_y))


    def _draw_ui(self):
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - self.player.last_pulse_time) / self.player.cooldown)
        bar_width = 200
        
        pygame.draw.rect(self.screen, (50, 50, 50), (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width, 10))
        pygame.draw.rect(self.screen, NEON_CYAN, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 40, bar_width * progress, 10))
        
        lvl_text = self.font.render(f"Level {self.current_level_idx + 1}", True, WHITE)
        xp_text = self.font.render(f"XP: {self.current_xp}", True, WHITE)
        shop_hint = self.shop_font.render("[E] Upgrades", True, (150, 150, 150))
        
        self.screen.blit(lvl_text, (20, SCREEN_HEIGHT - 50))
        self.screen.blit(xp_text, (20, SCREEN_HEIGHT - 90))
        self.screen.blit(shop_hint, (20, 20))
        
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
            elif self.state == STATE_SHOP:
                self._draw_shop_overlay()
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
