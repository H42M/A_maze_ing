from collections import deque
from maze_config import Coordinate
from maze_generator import Grid, Wall
from typing import List


def is_within_bounds(grid: Grid, x: int, y: int) -> bool:
    height = len(grid)
    width = len(grid[0])
    return 0 <= x < width and 0 <= y < height


def find_open_cells(grid: Grid, x: int, y: int) -> List[Coordinate]:
    cell = grid[y][x]
    neighbours = [
        (Wall.NORTH, (x, y - 1)),
        (Wall.EAST, (x + 1, y)),
        (Wall.SOUTH, (x, y + 1)),
        (Wall.WEST, (x - 1, y)),
    ]
    open_cells = []
    for wall, (nx, ny) in neighbours:
        if is_within_bounds(grid, nx, ny) and not (cell & wall):
            open_cells.append((nx, ny))
    return open_cells


def solve_shortest_path(
        grid: Grid, entry: Coordinate, exit: Coordinate,
) -> List[Coordinate]:
    queue = deque([entry])
    visited = {entry}
    parents = {}

    while queue:
        current = queue.popleft()
        if current == exit:
            break
        neighbours = find_open_cells(grid, current[0], current[1])

        for n in neighbours:
            if n not in visited:
                visited.add(n)
                parents[n] = current
                queue.append(n)

    if exit not in visited:
        return []
    path = []
    current = exit
    while current != entry:
        path.append(current)
        current = parents[current]
    path.append(entry)
    path.reverse()
    return path
