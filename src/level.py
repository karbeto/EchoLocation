import pygame
from .settings import NEON_CYAN

class Level:
    
    def __init__(self, path):
        self.walls = []
        self.enemies_spawn_pos = []
        self.player_spawn_pos = [100, 100]
        self.tile_size = 64
        self.load_level(path)


    def load_level(self, path):
        try:
            with open(path, 'r') as f:
                for row_index, line in enumerate(f):
                    for col_index, char in enumerate(line.strip()):
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        
                        if char == 'W':
                            self.walls.append(pygame.Rect(x, y, self.tile_size, self.tile_size))
                        elif char == 'P':
                            self.player_spawn_pos = [x + self.tile_size // 2, y + self.tile_size // 2]
                        elif char == 'E':
                            self.enemies_spawn_pos.append((x + self.tile_size // 2, y + self.tile_size // 2))
        except FileNotFoundError:
            print(f"Error: {path} not found. Create a 'levels' folder with 'level1.txt'")
            # Fallback wall so the game doesn't crash
            self.walls.append(pygame.Rect(300, 200, 50, 300))


    def draw(self, surface):
        for wall in self.walls:
            pygame.draw.rect(surface, NEON_CYAN, wall, 2)
