import pygame
from .settings import NEON_CYAN, NEON_GOLD
from src.audio_manager import resource_path

class Level:
    
    def __init__(self, path_or_layout):
        self.walls = []
        self.chime_walls = []
        self.enemies_spawn_pos = []
        self.player_spawn_pos = [100, 100]
        self.tile_size = 64
        self.key_rect = None 
        self.goal_rect = None 
        
        self.width = 0
        self.height = 0
        
        if isinstance(path_or_layout, list):
            self.parse_layout(path_or_layout)
        else:
            self.load_level(path_or_layout)


    def load_level(self, path):
        try:
            with open(resource_path(path), 'r') as f:
                lines = f.readlines()
                if not lines:
                    return
                self.parse_layout(lines)
                            
        except FileNotFoundError:
            print(f"Error: {path} not found.")
            self.width = 1280
            self.height = 720
            self.walls.append(pygame.Rect(300, 200, 50, 300))


    def parse_layout(self, lines):
        self.walls.clear()
        self.chime_walls.clear()
        self.enemies_spawn_pos.clear()
        
        self.height = len(lines) * self.tile_size
        max_cols = 0
        
        for row_index, line in enumerate(lines):
            clean_line = line.strip()
            max_cols = max(max_cols, len(clean_line))
            
            for col_index, char in enumerate(clean_line):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                
                if char == 'W':
                    self.walls.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
                elif char == 'C':
                    self.chime_walls.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
                elif char == 'P':
                    self.player_spawn_pos = [x + self.tile_size // 2, y + self.tile_size // 2]
                elif char == 'E':
                    self.enemies_spawn_pos.append((x + self.tile_size // 2, y + self.tile_size // 2))
                elif char == 'G':
                    self.goal_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                elif char == 'K':
                    self.key_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
        
        self.width = max_cols * self.tile_size


    def draw(self, surface):
        for wall in self.walls:
            pygame.draw.rect(surface, NEON_CYAN, wall, 2)
            
        if self.goal_rect:
            pygame.draw.rect(surface, NEON_GOLD, self.goal_rect, 2)