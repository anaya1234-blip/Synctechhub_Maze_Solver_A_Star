
import heapq
from itertools import count


def heuristic(node, goal):
    """
    Manhattan Distance Heuristic.
    Estimates the distance between current node and goal.
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def astar(maze, start, goal):
    """
    A* Search Algorithm.

    Returns:
        path: Shortest path from start to goal.
        explored_order: Nodes explored during search.
    """

    if not maze or not maze[0]:
        raise ValueError("Maze cannot be empty.")

    rows = len(maze)
    cols = len(maze[0])

    if any(len(row) != cols for row in maze):
        raise ValueError("Maze must be rectangular.")

    for name, position in [("Start", start), ("Goal", goal)]:
        if not (
            isinstance(position, tuple)
            and len(position) == 2
            and all(isinstance(v, int) for v in position)
        ):
            raise ValueError(f"{name} must be a tuple of two integers.")

        r, c = position
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{name} position is outside the maze.")

    if maze[start[0]][start[1]] != 0:
        raise ValueError("Start position must be an empty cell.")

    if maze[goal[0]][goal[1]] != 0:
        raise ValueError("Goal position must be an empty cell.")

    open_list = []
    tie_breaker = count()

    heapq.heappush(
        open_list,
        (heuristic(start, goal), next(tie_breaker), start)
    )

    g_score = {start: 0}
    came_from = {}

    closed_set = set()
    explored_order = []

    while open_list:

        _, _, current = heapq.heappop(open_list)

        if current in closed_set:
            continue

        closed_set.add(current)
        explored_order.append(current)

        if current == goal:

            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()

            return path, explored_order

        row, col = current

        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]

        for neighbor in neighbors:

            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue

            if maze[r][c] == 1:
                continue

            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = (
                    tentative_g + heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_list,
                    (f_score, next(tie_breaker), neighbor)
                )

    return None, explored_order
