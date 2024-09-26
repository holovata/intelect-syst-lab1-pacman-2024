import json
import os
from src.maze import Maze


class LevelGenerator:
    def __init__(self, level_number):
        self.level_number = level_number
        self.config = self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'levels', 'level_config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            print("Файл конфігурації рівнів не знайдено.")
            return {}

    def get_level_params(self):
        predefined_levels = self.config.get('levels', [])
        if self.level_number <= len(predefined_levels):
            return predefined_levels[self.level_number - 1]
        else:
            # Генеруємо параметри для вищих рівнів
            maze_size = 10 + self.level_number * 2  # Розмір лабіринту збільшується з рівнем
            wall_density = min(0.1 + 0.05 * self.level_number, 0.6)  # Щільність стін збільшується до 0.6
            number_of_ghosts = min(4 + (self.level_number - 1) // 2, 10)  # Кількість привидів пропорційна рівню, максимум 10
            return {
                "maze_size": [maze_size, maze_size],
                "wall_density": wall_density,
                "ghost_speed": 0.5 + 0.05 * self.level_number,
                "ghost_behaviour": "coordinated_attack",
                "number_of_ghosts": number_of_ghosts
            }

    def generate_level(self):
        level_params = self.get_level_params()
        width, height = level_params.get('maze_size', [15, 15])
        wall_density = level_params.get('wall_density', 0.3)
        maze = Maze(width, height, wall_density)
        maze.generate_maze()
        ghost_speed = level_params.get('ghost_speed', 0.5)
        ghost_behaviour = level_params.get('ghost_behaviour', 'simple_chase')
        number_of_ghosts = level_params.get('number_of_ghosts', 4)
        return maze, ghost_speed, ghost_behaviour, number_of_ghosts
