# src/pacman.py


import pygame
from ai.heuristics import PacManHeuristic
from pathfinding.a_star import a_star_search
from pathfinding.bfs import bfs_search
from pathfinding.dfs import dfs_search
import random


class PacMan:
    def __init__(self, maze, image, level_number, ghosts):
        self.maze = maze
        self.image = image
        self.position = maze.start_position
        self.direction = (0, 0)  # Поточний напрямок руху
        self.level_number = level_number
        self.ghosts = ghosts
        self.safe_distance = 3  # Мінімальна безпечна відстань до привидів
        self.previous_positions = []  # Історія останніх позицій
        self.heuristic = PacManHeuristic(level_number)

    def handle_key_event(self, event):
        # Порожня реалізація, щоб ігнорувати всі натискання клавіш
        pass

    def update(self):
        # Автоматичний рух Пакмена
        target = self.get_target()
        if target:
            self.direction = self.calculate_direction(target)
            if self.direction != (0, 0):
                new_position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            else:
                # Якщо немає напрямку до цілі, вибираємо випадковий рух
                new_position = self.random_move()

            # Перевіряємо можливість руху
            if self.maze.is_path(new_position):
                self.position = new_position
                self.collect_dot()
                self.previous_positions.append(self.position)
                # Обмежуємо розмір історії позицій
                if len(self.previous_positions) > 5:
                    self.previous_positions.pop(0)
            else:
                # Якщо рух неможливий, намагаємося рухатися випадково
                new_position = self.random_move()
                if new_position != self.position:
                    self.position = new_position
                    self.collect_dot()
                    self.previous_positions.append(self.position)
                    if len(self.previous_positions) > 5:
                        self.previous_positions.pop(0)
        else:
            # Якщо немає цілі, стоїмо на місці або рухаємося випадково
            new_position = self.random_move()
            if new_position != self.position:
                self.position = new_position
                self.collect_dot()
                self.previous_positions.append(self.position)
                if len(self.previous_positions) > 5:
                    self.previous_positions.pop(0)

    def get_target(self):
        # Використовуємо евристику для отримання цільової позиції
        return self.heuristic.get_target(self.maze, self)

    '''def get_target(self):
        # Вибір найближчої безпечної точки
        if self.maze.dots:
            closest_safe_dot = None
            min_distance = float('inf')
            for dot in self.maze.dots:
                min_distance_to_ghost = self.distance_to_ghosts(dot)
                if min_distance_to_ghost >= self.safe_distance:
                    distance_to_pacman = self.manhattan_distance(self.position, dot)
                    if distance_to_pacman < min_distance:
                        min_distance = distance_to_pacman
                        closest_safe_dot = dot
            if closest_safe_dot:
                return closest_safe_dot
            else:
                # Якщо немає безпечних точок, вибрати найближчу точку
                closest_dot = min(self.maze.dots, key=lambda pos: self.manhattan_distance(self.position, pos))
                return closest_dot
        else:
            return None  # Немає точок для збору'''

    def calculate_direction(self, target):
        algorithm_choice = random.randint(1, 3)
        if algorithm_choice == 1:
            path = dfs_search(self.maze.grid, self.position, target)
            print("Алгоритм: DFS")
        elif algorithm_choice == 2:
            path = bfs_search(self.maze.grid, self.position, target)
            print("Алгоритм: BFS")
        else:
            path = a_star_search(self.maze.grid, self.position, target)
            print("Алгоритм: A*")

        # Перевіряємо шлях і повертаємо наступний крок
        if path and len(path) > 1:
            next_step = path[1]
            dx = next_step[0] - self.position[0]
            dy = next_step[1] - self.position[1]
            return (dx, dy)
        else:
            return (0, 0)

    def distance_to_ghosts(self, position):
        # Рахуємо мінімальну відстань до всіх привидів
        min_distance = float('inf')
        for ghost in self.ghosts:
            distance = abs(position[0] - ghost.position[0]) + abs(position[1] - ghost.position[1])
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def collect_dot(self):
        if self.position in self.maze.dots:
            self.maze.dots.remove(self.position)
            # Тут можна додати збільшення балів

    def draw(self, screen, scale=1):
        tile_size = 30 * scale
        x_pixel = self.position[0] * tile_size
        y_pixel = self.position[1] * tile_size
        scaled_image = pygame.transform.scale(self.image, (int(tile_size), int(tile_size)))
        screen.blit(scaled_image, (x_pixel, y_pixel))

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def random_move(self):
        # Рухаємось у випадковому доступному напрямку
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_position = (self.position[0] + dx, self.position[1] + dy)
            if self.maze.is_path(new_position):
                return new_position
        return self.position  # Якщо немає доступних напрямків, залишаємося на місці
