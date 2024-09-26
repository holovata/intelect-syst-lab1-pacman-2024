# pathfinding/a_star.py

import heapq


def a_star_search(grid, start, goal):
    """
    Реалізація алгоритму A*.
    grid: 2D список, де 0 - прохідна клітинка, 1 - стіна
    start: кортеж (x, y)
    goal: кортеж (x, y)
    """
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current_cost, current = heapq.heappop(open_set)

        if current == goal:
            # Відновлення шляху
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        neighbors = get_neighbors(grid, current)
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1  # Припускаємо, що вартість переходу 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return None  # Шлях не знайдено


def get_neighbors(grid, position):
    x, y = position
    neighbors = []
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] == 0:
                neighbors.append((nx, ny))
    return neighbors