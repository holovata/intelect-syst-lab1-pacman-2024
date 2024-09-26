# src/ghost.py

import pygame
from ai.heuristics import GhostHeuristic
from pathfinding.a_star import a_star_search
from pathfinding.bfs import bfs_search
from pathfinding.dfs import dfs_search
import random


class Ghost:
    def __init__(self, maze, image, speed, level_number, position):
        self.maze = maze
        self.image = image
        self.position = position  # Позиція в сітці лабіринту
        self.speed = speed
        self.level_number = level_number
        self.move_counter = 0
        self.previous_positions = []  # Історія останніх позицій
        self.heuristic = GhostHeuristic(level_number)

    def update(self, pacman):
        self.move_counter += self.speed
        if self.move_counter >= 1:
            self.move_counter = 0
            try:
                # Використовуємо евристику для отримання цільової позиції
                target = self.heuristic.get_target(self.maze, self, pacman)
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

                if path and len(path) > 1:
                    next_position = path[1]
                    # Перевіряємо, чи не зациклився привид на двох клітинках
                    if next_position not in self.previous_positions[-2:]:  # Уникаємо останніх двох позицій
                        if not self.is_occupied(next_position):
                            self.position = next_position
                            self.previous_positions.append(self.position)
                            if len(self.previous_positions) > 5:
                                self.previous_positions.pop(0)
                        else:
                            # Якщо позиція зайнята, рухаємось випадково
                            self.random_move()
                    else:
                        # Якщо привид зациклився, рухаємось випадково
                        self.random_move()
                else:
                    # Якщо немає шляху, рухаємось випадково
                    self.random_move()
            except Exception as e:
                print(f"Помилка при оновленні привида: {e}")
                self.random_move()

    def random_move(self):
        # Рухаємося у випадковому доступному напрямку
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_position = (self.position[0] + dx, self.position[1] + dy)
            if self.maze.is_path(new_position) and not self.is_occupied(new_position):
                self.position = new_position
                self.previous_positions.append(self.position)
                if len(self.previous_positions) > 5:
                    self.previous_positions.pop(0)
                break  # Виходимо з циклу після успішного руху

    def is_occupied(self, position):
        # Перевіряємо, чи зайнята позиція іншим привидом
        for ghost in self.maze.ghosts:
            if ghost.position == position and ghost != self:
                return True
        return False

    def draw(self, screen, scale=1):
        tile_size = 30 * scale
        x_pixel = self.position[0] * tile_size
        y_pixel = self.position[1] * tile_size
        scaled_image = pygame.transform.scale(self.image, (int(tile_size), int(tile_size)))
        screen.blit(scaled_image, (x_pixel, y_pixel))
