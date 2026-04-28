from maze_config import MazeConfig
from enum import IntFlag
from typing import List
import random
from maze_config import Coordinate


class Wall(IntFlag):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST


type Grid = List[List[Wall]]


class MazeGenerator:
    def __init__(self, config: MazeConfig) -> None:
        self.config = config
        self.grid = self.create_grid()
        self.visited = self.create_visited_grid()
        self.rng = random.Random(self.config.seed)

    def create_grid(self) -> Grid:
        grid: Grid = [[Wall.ALL for _ in range(self.config.width)]
                      for _ in range(self.config.height)]
        return grid

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.config.width and 0 <= y < self.config.height

    def is_adjacent(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        dx = x2 - x1
        dy = y2 - y1
        return (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1))

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        if (
            not self.is_within_bounds(x1, y1) or
            not self.is_within_bounds(x2, y2)
        ):
            raise ValueError("cells coordinates not within bounds")
        if not self.is_adjacent(x1, y1, x2, y2):
            raise ValueError("cells must be adjacent")
        grid = self.grid
        if x2 == x1 + 1:
            grid[y1][x1] &= ~Wall.EAST
            grid[y2][x2] &= ~Wall.WEST
        elif y2 == y1 + 1:
            grid[y1][x1] &= ~Wall.SOUTH
            grid[y2][x2] &= ~Wall.NORTH
        elif y1 == y2 + 1:
            grid[y1][x1] &= ~Wall.NORTH
            grid[y2][x2] &= ~Wall.SOUTH
        elif x1 == x2 + 1:
            grid[y1][x1] &= ~Wall.WEST
            grid[y2][x2] &= ~Wall.EAST

    def create_visited_grid(self) -> list[list[bool]]:
        return [[False for _ in range(self.config.width)]
                for _ in range(self.config.height)]

    def get_next_free_cells(self, x: int, y: int) -> list[Coordinate]:
        if not self.is_within_bounds(x, y):
            raise ValueError("not within bounds")

        not_visited: list[Coordinate] = []
        candidates = [
            (x, y + 1),
            (x + 1, y),
            (x, y - 1),
            (x - 1, y),
        ]

        for nx, ny in candidates:
            if self.is_within_bounds(nx, ny) and not self.visited[ny][nx]:
                not_visited.append((nx, ny))

        return not_visited

    def generate_perfect(self) -> None:
        self.grid = self.create_grid()
        self.visited = self.create_visited_grid()
        stack: list[Coordinate] = []
        current: Coordinate = self.config.entry
        self.visited[current[1]][current[0]] = True
        stack.append(current)

        while stack:
            top_cell = stack[-1]
            next_cells = self.get_next_free_cells(top_cell[0], top_cell[1])
            if next_cells:
                next_cell = self.rng.choice(next_cells)
                self.remove_wall(top_cell[0], top_cell[1], next_cell[0],
                                 next_cell[1])
                self.visited[next_cell[1]][next_cell[0]] = True
                stack.append(next_cell)
            else:
                stack.pop()
