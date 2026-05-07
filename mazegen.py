"""Standalone reusable maze generator for A-Maze-ing.

Basic usage:

    from mazegen import MazeGenerator

    generator = MazeGenerator(width=20, height=15, seed=42)
    generator.generate()

    grid = generator.structure
    solution = generator.solution
    moves = generator.solution_moves

Custom parameters:

    generator = MazeGenerator(
        width=30,
        height=20,
        entry=(0, 0),
        exit=(29, 19),
        seed=1234,
        perfect=True,
    )
    generator.generate()

Available generated data:
    - structure: 2D list of wall bitmasks.
    - solution: shortest path as a list of coordinates.
    - solution_moves: shortest path as N/E/S/W letters.
"""
from __future__ import annotations

from collections import deque
import random

Coordinate = tuple[int, int]


class MazeGenerator:
    """Generate a maze and expose its structure and solution.

    Args:
        width: Maze width in cells.
        height: Maze height in cells.
        entry: Entry cell coordinates as ``(x, y)``.
        exit: Exit cell coordinates as ``(x, y)``. Defaults to the bottom-right
            cell when omitted.
        seed: Optional random seed used for reproducible generation.
        perfect: If true, keep exactly one path between any two walkable cells.
        include_logo_42: If true, reserve fully closed cells shaped as ``42``
            when the maze is large enough.
        extra_open_probability: Probability used to open extra walls when
            ``perfect`` is false.

    Attributes:
        NORTH: Bit value for a closed north wall.
        EAST: Bit value for a closed east wall.
        SOUTH: Bit value for a closed south wall.
        WEST: Bit value for a closed west wall.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL_WALLS = NORTH | EAST | SOUTH | WEST

    _DIRECTIONS: dict[str, tuple[int, int, int, int]] = {
        "N": (0, -1, NORTH, SOUTH),
        "E": (1, 0, EAST, WEST),
        "S": (0, 1, SOUTH, NORTH),
        "W": (-1, 0, WEST, EAST),
    }

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coordinate = (0, 0),
        exit: Coordinate | None = None,
        seed: int | None = None,
        perfect: bool = True,
        include_logo_42: bool = True,
        extra_open_probability: float = 0.08,
    ) -> None:
        """Initialize the generator parameters."""
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit if exit is not None else (width - 1, height - 1)
        self._seed = seed
        self._perfect = perfect
        self._include_logo_42 = include_logo_42
        self._extra_open_probability = extra_open_probability
        self._random = random.Random(seed)

        self._grid: list[list[int]] = []
        self._logo_cells: set[Coordinate] = set()
        self._solution: list[Coordinate] = []
        self._warnings: list[str] = []
        self._generated = False

        self._validate_parameters()

    def generate(self) -> MazeGenerator:
        """Generate the maze and return the generator instance."""
        self._grid = [
            [self.ALL_WALLS for _ in range(self._width)]
            for _ in range(self._height)
        ]
        self._solution = []
        self._warnings = []
        self._generated = False

        if self._include_logo_42:
            self._set_logo_42_cells()

        self._generate_perfect_maze()
        if not self._perfect:
            self._open_extra_walls()

        self._solution = self._find_shortest_path()
        self._generated = True
        return self

    def to_hex_rows(self) -> list[str]:
        """Return the maze as hexadecimal rows."""
        self._require_generated()
        return ["".join(format(cell, "X") for cell in row)
                for row in self._grid]

    def to_output_text(self) -> str:
        """Return a subject-style output string for the generated maze."""
        self._require_generated()
        rows = "\n".join(self.to_hex_rows())
        entry = f"{self._entry[0]},{self._entry[1]}"
        exit_cell = f"{self._exit[0]},{self._exit[1]}"
        return f"{rows}\n\n{entry}\n{exit_cell}\n{self.solution_moves}\n"

    def _validate_parameters(self) -> None:
        """Validate constructor arguments."""
        if self._width <= 0 or self._height <= 0:
            raise ValueError("Maze width and height must be positive")
        if not self._is_inside(self._entry):
            raise ValueError(f"Entry is outside maze bounds: {self._entry}")
        if not self._is_inside(self._exit):
            raise ValueError(f"Exit is outside maze bounds: {self._exit}")
        if self._entry == self._exit:
            raise ValueError("Entry and exit must be different cells")
        if not 0.0 <= self._extra_open_probability <= 1.0:
            raise ValueError("extra_open_probability must be between 0 and 1")

    def _set_logo_42_cells(self) -> None:
        """Reserve fully closed cells forming a centered 42 pattern."""
        logo_width = 7
        logo_height = 5

        if self._width < logo_width or self._height < logo_height:
            self._warnings.append(
                "Maze is too small to display the 42 pattern "
                "(minimum size: 7x5)."
            )
            return

        start_x = (self._width - logo_width) // 2
        start_y = (self._height - logo_height) // 2
        candidates = self._build_logo_42_cells(start_x, start_y)

        if self._entry in candidates or self._exit in candidates:
            self._warnings.append(
                "Could not display the 42 pattern because it overlaps "
                "the entry or exit."
            )
            return

        if not self._walkable_cells_are_connected(candidates):
            self._warnings.append(
                "Maze is too small to display the 42 pattern without "
                "disconnecting the maze."
            )
            return

        self._logo_cells = candidates

    def _build_logo_42_cells(self, start_x: int,
                             start_y: int) -> set[Coordinate]:
        """Return coordinates for the 42 pattern."""
        relative_cells = {
            # Number 4.
            (0, 0), (0, 1), (0, 2),
            (1, 2), (2, 2),
            (2, 3), (2, 4),
            # Number 2.
            (4, 0), (5, 0), (6, 0),
            (6, 1), (6, 2),
            (5, 2), (4, 2),
            (4, 3), (4, 4),
            (5, 4), (6, 4),
        }
        return {(start_x + x, start_y + y) for x, y in relative_cells}

    def _walkable_cells_are_connected(self, blocked: set[Coordinate]) -> bool:
        """Return true if all non-blocked cells form one connected component"""
        total = self._width * self._height - len(blocked)
        if total <= 0:
            return False

        start = self._entry if self._entry not in blocked else None
        if start is None:
            return False

        visited = {start}
        stack = [start]

        while stack:
            x, y = stack.pop()
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                neighbor = (x + dx, y + dy)
                if not self._is_inside(neighbor):
                    continue
                if neighbor in blocked or neighbor in visited:
                    continue
                visited.add(neighbor)
                stack.append(neighbor)

        return len(visited) == total

    def _generate_perfect_maze(self) -> None:
        """Generate a depth-first-search maze over non-logo cells."""
        visited = {self._entry}
        stack = [self._entry]

        while stack:
            current = stack[-1]
            neighbors = self._unvisited_neighbors(current, visited)

            if not neighbors:
                stack.pop()
                continue

            direction, neighbor = self._random.choice(neighbors)
            self._open_wall(current, neighbor, direction)
            visited.add(neighbor)
            stack.append(neighbor)

    def _unvisited_neighbors(
        self,
        cell: Coordinate,
        visited: set[Coordinate],
    ) -> list[tuple[str, Coordinate]]:
        """Return unvisited walkable neighbors for generation."""
        x, y = cell
        neighbors: list[tuple[str, Coordinate]] = []

        for direction, (dx, dy, _, _) in self._DIRECTIONS.items():
            neighbor = (x + dx, y + dy)
            if not self._is_inside(neighbor):
                continue
            if neighbor in visited or neighbor in self._logo_cells:
                continue
            neighbors.append((direction, neighbor))

        return neighbors

    def _open_extra_walls(self) -> None:
        """Open additional coherent walls to create loops."""
        for y in range(self._height):
            for x in range(self._width):
                cell = (x, y)
                if cell in self._logo_cells:
                    continue

                for direction in ("E", "S"):
                    dx, dy, wall, _ = self._DIRECTIONS[direction]
                    neighbor = (x + dx, y + dy)
                    if not self._is_inside(neighbor):
                        continue
                    if neighbor in self._logo_cells:
                        continue
                    if not self._grid[y][x] & wall:
                        continue
                    if self._random.random() <= self._extra_open_probability:
                        self._open_wall(cell, neighbor, direction)

    def _open_wall(
        self,
        cell: Coordinate,
        neighbor: Coordinate,
        direction: str,
    ) -> None:
        """Open the wall between two neighboring cells."""
        _, _, cell_wall, neighbor_wall = self._DIRECTIONS[direction]
        x, y = cell
        nx, ny = neighbor
        self._grid[y][x] &= ~cell_wall
        self._grid[ny][nx] &= ~neighbor_wall

    def _find_shortest_path(self) -> list[Coordinate]:
        """Return the shortest path from entry to exit using BFS."""
        queue: deque[tuple[Coordinate, list[Coordinate]]] = deque()
        queue.append((self._entry, [self._entry]))
        visited = {self._entry}

        while queue:
            cell, path = queue.popleft()
            if cell == self._exit:
                return path

            for neighbor in self._open_neighbors(cell):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        return []

    def _open_neighbors(self, cell: Coordinate) -> list[Coordinate]:
        """Return cells reachable from a coordinate through open walls."""
        x, y = cell
        value = self._grid[y][x]
        neighbors: list[Coordinate] = []

        for _, (dx, dy, wall, _) in self._DIRECTIONS.items():
            neighbor = (x + dx, y + dy)
            if not self._is_inside(neighbor):
                continue
            if neighbor in self._logo_cells:
                continue
            if value & wall:
                continue
            neighbors.append(neighbor)

        return neighbors

    def _is_inside(self, cell: Coordinate) -> bool:
        """Return true if the coordinate is inside maze bounds."""
        x, y = cell
        return 0 <= x < self._width and 0 <= y < self._height

    def _require_generated(self) -> None:
        """Raise an error if the maze has not been generated yet."""
        if not self._generated:
            raise RuntimeError("Call generate() before accessing maze data")

    @property
    def width(self) -> int:
        """Return the maze width."""
        return self._width

    @property
    def height(self) -> int:
        """Return the maze height."""
        return self._height

    @property
    def entry(self) -> Coordinate:
        """Return the entry coordinate."""
        return self._entry

    @property
    def exit(self) -> Coordinate:
        """Return the exit coordinate."""
        return self._exit

    @property
    def seed(self) -> int | None:
        """Return the configured random seed."""
        return self._seed

    @property
    def perfect(self) -> bool:
        """Return whether the maze is configured as perfect."""
        return self._perfect

    @property
    def structure(self) -> list[list[int]]:
        """Return the generated maze as a copied 2D wall-bitmask grid."""
        self._require_generated()
        return [row[:] for row in self._grid]

    @property
    def solution(self) -> list[Coordinate]:
        """Return the shortest path as a list of coordinates."""
        self._require_generated()
        return self._solution[:]

    @property
    def solution_moves(self) -> str:
        """Return the shortest path as N/E/S/W movement letters."""
        self._require_generated()
        moves = []

        for current, next_cell in zip(self._solution, self._solution[1:]):
            cx, cy = current
            nx, ny = next_cell
            if nx == cx and ny == cy - 1:
                moves.append("N")
            elif nx == cx + 1 and ny == cy:
                moves.append("E")
            elif nx == cx and ny == cy + 1:
                moves.append("S")
            elif nx == cx - 1 and ny == cy:
                moves.append("W")

        return "".join(moves)

    @property
    def logo_cells(self) -> set[Coordinate]:
        """Return a copy of the coordinates reserved for the 42 pattern."""
        return set(self._logo_cells)

    @property
    def warnings(self) -> list[str]:
        """Return non-fatal generation warnings."""
        return self._warnings[:]
