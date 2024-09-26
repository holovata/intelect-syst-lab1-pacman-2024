# ai/heuristics.py


class GhostHeuristic:
    def __init__(self, level_number):
        self.level_number = level_number
        # self.algorithm = algorithm  # Функція алгоритму пошуку шляху

    def get_target(self, maze, ghost, pacman):
        # Для складних рівнів використовуємо стратегію оточення
        if self.level_number >= 5:
            return self.coordinate_attack(maze, ghost, pacman)
        elif self.level_number >= 3:
            return self.predict_pacman_position(pacman)
        else:
            return pacman.position

    def predict_pacman_position(self, pacman):
        # Прогнозування на основі поточного напрямку руху Пакмена
        dx, dy = pacman.direction
        predicted_position = (pacman.position[0] + dx * 2, pacman.position[1] + dy * 2)
        # Переконаємось, що передбачена позиція знаходиться всередині лабіринту
        predicted_position = (
            max(0, min(predicted_position[0], len(pacman.maze.grid[0]) - 1)),
            max(0, min(predicted_position[1], len(pacman.maze.grid) - 1))
        )
        return predicted_position

    def coordinate_attack(self, maze, ghost, pacman):
        # Привидіння розподіляються навколо Пакмена на основі свого індексу
        index = maze.ghosts.index(ghost)
        num_ghosts = len(maze.ghosts)
        angle = (360 / num_ghosts) * index
        dx, dy = self.get_offset_from_angle(angle)

        # Ціль — позиція навколо Пакмена, зсунута на dx, dy
        target = (pacman.position[0] + dx, pacman.position[1] + dy)
        # Перевіряємо, що ціль знаходиться всередині лабіринту і є шляхом
        if 0 <= target[0] < maze.width and 0 <= target[1] < maze.height and maze.is_path(target):
            return target
        else:
            # Якщо ціль недоступна, повертаємо позицію Пакмена
            return pacman.position

    def get_offset_from_angle(self, angle):
        # Конвертуємо кут у зсув по x та y
        import math
        radians = math.radians(angle)
        dx = round(math.cos(radians))
        dy = round(math.sin(radians))
        return dx, dy


class PacManHeuristic:
    def __init__(self, level_number):
        self.level_number = level_number
        # self.algorithm = algorithm  # Функція алгоритму пошуку шляху

    def get_target(self, maze, pacman):
        # Визначити цільову позицію для Пакмена
        if not maze.dots:
            return pacman.position  # Немає їжі, залишаємося на місці
        closest_safe_food = None
        min_distance = float('inf')
        for dot in maze.dots:
            distance_to_pacman = self.manhattan_distance(pacman.position, dot)
            distance_to_ghost = pacman.distance_to_ghosts(dot)
            if distance_to_ghost >= pacman.safe_distance:
                if distance_to_pacman < min_distance:
                    min_distance = distance_to_pacman
                    closest_safe_food = dot
        if closest_safe_food:
            return closest_safe_food
        else:
            # Якщо немає безпечних точок, вибрати найближчу точку
            return min(maze.dots, key=lambda pos: self.manhattan_distance(pacman.position, pos))

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
