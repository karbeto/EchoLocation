import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, NEON_CYAN, NEON_GOLD, NEON_RED

class UIRenderer:
    
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)
        self.shop_font = pygame.font.SysFont("Arial", 24)


    def draw_menu(self, screen):
        screen.fill(BLACK)
        text = self.font.render("ECHO LOCATION: PRESS SPACE TO START", True, NEON_CYAN)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)


    def draw_gameover(self, screen):
        screen.fill(BLACK)
        text = self.font.render("CAUGHT IN THE DARK. PRESS SPACE TO RETRY", True, NEON_RED)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)


    def draw_win(self, screen):
        screen.fill(BLACK)
        text = self.font.render("ALL LEVELS CLEAR. PRESS SPACE TO RESTART", True, NEON_GOLD)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)


    def draw_hud(self, screen, current_level_idx, current_xp, player):
        current_time = pygame.time.get_ticks()
        progress = min(1.0, (current_time - player.last_pulse_time) / player.cooldown)
        bar_width = 200
        
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40, bar_width, 10))
        pygame.draw.rect(screen, NEON_CYAN, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 40, int(bar_width * progress), 10))
        
        lvl_text = self.font.render(f"Level {current_level_idx + 1}", True, WHITE)
        xp_text = self.font.render(f"XP: {current_xp}", True, WHITE)
        shop_hint = self.shop_font.render("[E] Upgrades", True, (150, 150, 150))
        
        screen.blit(lvl_text, (20, SCREEN_HEIGHT - 50))
        screen.blit(xp_text, (20, SCREEN_HEIGHT - 90))
        screen.blit(shop_hint, (20, 20))
        
        if player.has_key:
            key_text = self.font.render("KEY: ACQUIRED", True, NEON_GOLD)
            screen.blit(key_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 50))
        else:
            key_text = self.font.render("KEY: REQUIRED", True, (100, 100, 100))
            screen.blit(key_text, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 50))


    def draw_shop_overlay(self, screen, shop_manager, current_xp):
        panel_w, panel_h = 460, 310
        shop_panel = pygame.Surface((panel_w, panel_h))
        shop_panel.fill((10, 15, 20))
        pygame.draw.rect(shop_panel, NEON_CYAN, (0, 0, panel_w, panel_h), 2)
        
        cost_r = shop_manager.get_upgrade_cost(shop_manager.radius_level)
        cost_c = shop_manager.get_upgrade_cost(shop_manager.cooldown_level)
        cost_s = shop_manager.get_upgrade_cost(shop_manager.speed_level, is_speed=True)
        
        lvl_r = f"Lvl {shop_manager.radius_level}/5" if shop_manager.radius_level < 5 else "MAX"
        lvl_c = f"Lvl {shop_manager.cooldown_level}/5" if shop_manager.cooldown_level < 5 else "MAX"
        lvl_s = f"Lvl {shop_manager.speed_level}/5" if shop_manager.speed_level < 5 else "MAX"
        
        title_txt = self.font.render("ECHO MODIFICATIONS", True, NEON_CYAN)
        xp_txt = self.shop_font.render(f"Available XP Balance: {current_xp}", True, WHITE)
        
        opt1_txt = self.shop_font.render(f"[1] Sonar Amplifier ({lvl_r}) - Cost: {cost_r} XP", True, NEON_GOLD if shop_manager.radius_level < 5 else (100, 100, 100))
        opt2_txt = self.shop_font.render(f"[2] Frequency Booster ({lvl_c}) - Cost: {cost_c} XP", True, NEON_GOLD if shop_manager.cooldown_level < 5 else (100, 100, 100))
        opt3_txt = self.shop_font.render(f"[3] Kinetic Thrusters ({lvl_s}) - Cost: {cost_s} XP", True, NEON_GOLD if shop_manager.speed_level < 5 else (100, 100, 100))
        exit_txt = self.shop_font.render("[E] Resume Mission Tracker", True, WHITE)
        
        shop_panel.blit(title_txt, (30, 20))
        shop_panel.blit(xp_txt, (30, 70))
        shop_panel.blit(opt1_txt, (30, 120))
        shop_panel.blit(opt2_txt, (30, 160))
        shop_panel.blit(opt3_txt, (30, 200)) 
        shop_panel.blit(exit_txt, (30, 255))
        
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        screen.blit(shop_panel, (panel_x, panel_y))