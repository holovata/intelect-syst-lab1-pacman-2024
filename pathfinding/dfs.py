# pathfinding/dfs.py
from pathfinding.a_star import get_neighbors


def dfs_search(grid, start, goal):
    """
    Реалізація алгоритму DFS.
    grid: 2D список, де 0 - прохідна клітинка, 1 - стіна
    start: кортеж (x, y)
    goal: кортеж (x, y)
    """
    stack = []
    stack.append(start)
    came_from = {start: None}
    visited = set()

    while stack:
        current = stack.pop()

        if current == goal:
            # Відновлення шляху
            path = [current]
            while came_from[current]:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(grid, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)

    return None  # Шлях не знайдено
