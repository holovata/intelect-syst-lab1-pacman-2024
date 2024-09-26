import pygame
import random
import os


class Maze:
    def __init__(self, width, height, wall_density=0.3):
        """
        width, height: розміри лабіринту (мають бути непарними числами)
        wall_density: щільність стін (від 0 до 1), визначає ймовірність появи стіни
        """
        # Переконуємось, що розміри лабіринту непарні
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.wall_density = wall_density
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]  # 1 - стіна, 0 - шлях
        self.start_position = (1, 1)  # Стартова позиція Пакмена
        self.ghost_start_position = (self.width - 2, self.height - 2)  # Стартова позиція привидів
        self.dots = []  # Список позицій точок (їжі)
        self.ghosts = []  # Список привидів

    def generate_maze(self):
        """
        Генерація лабіринту за допомогою рекурсивного алгоритму зворотного ходу.
        Додаються додаткові шляхи для створення циклів.
        """
        # Початкова позиція для генерації
        stack = [self.start_position]
        self.grid[self.start_position[1]][self.start_position[0]] = 0

        while stack:
            current = stack[-1]
            x, y = current
            neighbors = []

            # Можливі напрямки: вгору, вниз, вліво, вправо
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            random.shuffle(directions)  # Перемішуємо напрямки для випадковості

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if self.grid[ny][nx] == 1:
                        neighbors.append((nx, ny))

            if neighbors:
                # Обираємо випадкового сусіда
                next_cell = random.choice(neighbors)
                nx, ny = next_cell

                # Видаляємо стіну між поточною та сусідньою клітинкою
                wall_x, wall_y = x + (nx - x) // 2, y + (ny - y) // 2
                self.grid[wall_y][wall_x] = 0
                self.grid[ny][nx] = 0

                # Додаємо сусідню клітинку в стек
                stack.append(next_cell)
            else:
                # Якщо немає сусідів, видаляємо поточну клітинку зі стека
                stack.pop()

        # Забезпечуємо, що позиція привидів вільна
        self.grid[self.ghost_start_position[1]][self.ghost_start_position[0]] = 0

        # Додаємо додаткові шляхи для створення циклів
        self.add_loops()

    def add_loops(self):
        """
        Додає додаткові шляхи в лабіринт, видаляючи деякі стіни випадковим чином.
        Це створює цикли та додаткові шляхи, роблячи лабіринт менш лінійним.
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 1:
                    # Перевіряємо, чи є поточна клітинка стіною і чи знаходиться вона між двома шляхами
                    if x % 2 == 1 and y % 2 == 1:
                        # Пропускаємо клітинки, розташовані на перехрестях шляхів
                        continue
                    # Перевіряємо, чи не є стінка горизонтальною або вертикальною
                    if (self.grid[y][x - 1] == 0 and self.grid[y][x + 1] == 0) or \
                            (self.grid[y - 1][x] == 0 and self.grid[y + 1][x] == 0):
                        # З ймовірністю wall_density видаляємо стіну
                        if random.random() < self.wall_density:
                            self.grid[y][x] = 0

    def place_dots(self):
        """
        Розміщення точок (їжі) на всіх прохідних клітинках, крім стартових позицій.
        """
        self.dots = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 0 and (x, y) != self.start_position and (x, y) != self.ghost_start_position:
                    self.dots.append((x, y))

    def draw(self, screen, scale=1):
        """
        Відтворення лабіринту на екрані з урахуванням масштабу.
        """
        tile_size = self.TILE_SIZE = 30 * scale  # Масштабуємо розмір плитки
        base_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(base_path, '..', 'assets', 'images')

        # Завантаження зображення стіни
        maze_tile_image_path = os.path.join(assets_path, 'maze_tiles.png')
        try:
            maze_tile = pygame.image.load(maze_tile_image_path).convert_alpha()
            maze_tile = pygame.transform.scale(maze_tile, (int(tile_size), int(tile_size)))
        except pygame.error as e:
            print(f"Помилка завантаження maze_tiles.png: {e}")
            maze_tile = pygame.Surface((int(tile_size), int(tile_size)))
            maze_tile.fill((0, 0, 255))  # Синій колір для стін

        # Відтворення лабіринту
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    screen.blit(maze_tile, (x * tile_size, y * tile_size))

    def get_pixel_position(self, position, scale=1):
        """
        Отримання піксельної позиції на екрані для даної позиції в сітці.
        """
        tile_size = self.TILE_SIZE = 30 * scale
        return (position[0] * tile_size, position[1] * tile_size)

    def is_path(self, position):
        """
        Перевірка, чи є дана позиція прохідною.
        """
        try:
            x, y = position
            if 0 <= x < self.width and 0 <= y < self.height:
                return self.grid[y][x] == 0
            return False
        except Exception as e:
            print(f"Помилка при перевірці шляху: {e}")
            return False

    def remove_dot(self, position):
        """
        Видалення точки (їжі) з даної позиції.
        """
        if position in self.dots:
            self.dots.remove(position)
