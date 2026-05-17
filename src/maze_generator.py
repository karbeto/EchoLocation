import random

class MazeGenerator:
    
    def __init__(self, width=25, height=13):
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1


    def generate(self, level_num):
        grid = [['W' for _ in range(self.width)] for _ in range(self.height)]
        visited = set()


        def carve_paths(cx, cy):
            visited.add((cx, cy))
            grid[cy][cx] = '.'

            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if (nx, ny) not in visited:
                        grid[cy + dy//2][cx + dx//2] = '.'
                        grid[ny][nx] = '.'
                        carve_paths(nx, ny)

        carve_paths(1, 1)

        # Braiding Step (Breaking extra inner walls)
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if grid[y][x] == 'W':
                    if (grid[y][x-1] == '.' and grid[y][x+1] == '.') or (grid[y-1][x] == '.' and grid[y+1][x] == '.'):
                        if random.random() < 0.25:
                            grid[y][x] = '.'

        open_cells = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if grid[y][x] == '.':
                    open_cells.append((x, y))

        player_x, player_y = 1, 1
        grid[player_y][player_x] = 'P'
        if (player_x, player_y) in open_cells:
            open_cells.remove((player_x, player_y))

        open_cells.sort(key=lambda cell: (cell[0] - player_x)**2 + (cell[1] - player_y)**2)
        goal_x, goal_y = open_cells.pop() 
        grid[goal_y][goal_x] = 'G'

        key_x, key_y = open_cells.pop(int(len(open_cells) * 0.75))
        grid[key_y][key_x] = 'K'

        safe_zone_radius = 5
        eligible_enemy_cells = [
            (x, y) for (x, y) in open_cells 
            if (abs(x - player_x) + abs(y - player_y)) > safe_zone_radius
        ]

        if not eligible_enemy_cells:
            eligible_enemy_cells = open_cells

        num_enemies = min(5, 2 + (level_num - 4) // 2)
        random.shuffle(eligible_enemy_cells)
        
        for _ in range(min(num_enemies, len(eligible_enemy_cells))):
            ex, ey = eligible_enemy_cells.pop()
            grid[ey][ex] = 'E'

        return ["".join(row) for row in grid]
