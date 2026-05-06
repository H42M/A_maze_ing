from typing import TYPE_CHECKING, Optional

from Maze.Cell import Cell

if TYPE_CHECKING:
    from Maze.Maze import Maze


def clear_42_logo(maze: "Maze") -> None:
    """Remove the 42 marker from all cells."""
    for row in maze.maze_lst:
        for cell in row:
            cell.is42 = False


def non_42_cells_are_connected(maze: "Maze") -> bool:
    """Return True if all non-42 cells form one connected area."""
    start: Optional[Cell] = None
    total = 0

    for row in maze.maze_lst:
        for cell in row:
            if not cell.is42:
                total += 1
                if start is None:
                    start = cell

    if start is None:
        return False

    visited: set[Cell] = {start}
    stack = [start]

    while stack:
        cell = stack.pop()

        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            neighbor = maze.get_cell((cell.x + dx, cell.y + dy))

            if neighbor and not neighbor.is42 and neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return len(visited) == total