# pathfinding/bfs.py

from collections import deque
from pathfinding.a_star import get_neighbors


def bfs_search(grid, start, goal):
    """
    Реалізація алгоритму BFS.
    grid: 2D список, де 0 - прохідна клітинка, 1 - стіна
    start: кортеж (x, y)
    goal: кортеж (x, y)
    """
    queue = deque()
    queue.append(start)
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            # Відновлення шляху
            path = [current]
            while came_from[current]:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in get_neighbors(grid, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    return None  # Шлях не знайдено
