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
from src.ui_renderer import UIRenderer
from src.game_renderer import GameRenderer

class EchoLocation:
    
    def __init__(self):
        pygame.init()
        self.audio_manager = AudioManager() 
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.level_files = ['levels/level1.txt', 'levels/level2.txt', 'levels/level3.txt']
        self.current_level_idx = 0
        self.state = STATE_MENU
        self.current_xp = 0
        
        self.generator = MazeGenerator(width=25, height=13) 
        self.shop_manager = ShopManager()
        self.ui_renderer = UIRenderer()
        self.game_renderer = GameRenderer()
        
        self.level = Level(self.level_files[self.current_level_idx])
        self.camera = Camera(self.level.width, self.level.height)
        
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
        self.game_renderer.clear_mask()
        self.player.has_key = False
        self.camera.update(self.player)


    def _next_level(self):
        self.current_level_idx += 1
        self.current_xp += 10
        self.audio_manager.play_effect('level_finish') 
        
        if self.current_level_idx < len(self.level_files):
            self.level = Level(self.level_files[self.current_level_idx])
        else:
            procedural_layout = self.generator.generate(self.current_level_idx + 1)
            self.level = Level(procedural_layout)
            
        self.camera = Camera(self.level.width, self.level.height)
        self._reset_game()
        self.state = STATE_PLAYING


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU and event.key == pygame.K_SPACE:
                    self.state = STATE_PLAYING
                elif self.state == STATE_GAMEOVER and event.key == pygame.K_SPACE:
                    self._reset_game()
                    self.state = STATE_PLAYING
                elif self.state == STATE_WIN and event.key == pygame.K_SPACE:
                    self.current_level_idx = 0
                    self.current_xp = 0 
                    self.level = Level(self.level_files[self.current_level_idx])
                    self.camera = Camera(self.level.width, self.level.height)
                    self._reset_game()
                    self.state = STATE_PLAYING

                elif self.state == STATE_PLAYING and event.key == pygame.K_e:
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

        for enemy in self.enemies:
            enemy.listen(self.player.pulses)
            enemy.update(self.level.walls, self.player.pos)
            if self.player.rect.colliderect(enemy.rect):
                self.state = STATE_GAMEOVER
        
        if self.level.goal_rect and self.player.rect.colliderect(self.level.goal_rect):
            if self.player.has_key:
                self._next_level()


    def run(self):
        while True:
            self._handle_events()
            
            if self.state == STATE_PLAYING:
                self._update_game()
                self.game_renderer.render_scene(self.screen, self.level, self.player, self.enemies, self.camera)
                self.ui_renderer.draw_hud(self.screen, self.current_level_idx, self.current_xp, self.player)
            elif self.state == STATE_SHOP:
                self.game_renderer.render_scene(self.screen, self.level, self.player, self.enemies, self.camera)
                self.ui_renderer.draw_shop_overlay(self.screen, self.shop_manager, self.current_xp)
            elif self.state == STATE_MENU:
                self.ui_renderer.draw_menu(self.screen)
            elif self.state == STATE_GAMEOVER:
                self.ui_renderer.draw_gameover(self.screen)
            elif self.state == STATE_WIN:
                self.ui_renderer.draw_win(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = EchoLocation()
    game.run()
