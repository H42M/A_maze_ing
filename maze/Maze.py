"""Maze class management."""


from .Cell import Cell
from Logs import Log
from config.Config import Config

from typing import Optional


class Maze:
    """Maze class."""

    def __init__(self, logs: Log, config: Config) -> None:
        """Initialize a Maze class instance.

        Args:
            logs (Log): Log manager
            width (int): Maze width.
            height (int): Maze height.
            entry (tuple[int,int]): Entry coordinates.
            exit (tuple[int, int]): Exit coordinates.

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        self.__logs = logs
        self._width = config.width
        self._height = config.height
        self._entry = config.entry
        self._exit = config.exit
        self._maze = self.default_maze()

    def default_maze(self) -> list[list[Cell]]:
        """Generate a maze with default value (all walls closed).

        Returns:
            list[list[Cell]]: Cell list.

        Example:
            >>> maze.default_maze()
            [
                [Cell()], [Cell()], [Cell()]],
                [Cell()], [Cell()], [Cell()]
            ]
        """
        maze = []
        if self._height and self._width:
            for y in range(self._height):
                row = []
                for x in range(self._width):
                    row.append(Cell(x, y))
                maze.append(row)
        return maze

    def available_cells(self) -> list[Cell]:
        """Return a list of all available Cell.

        Returns:
            Cell: available Cell list.

        Example:
            >>> maze.available_cells()
            [Cell, Cell, ...]
        """
        available_cells = []
        for col in self.maze_list:
            for cell in col:
                if not cell.visited:
                    available_cells.append(cell)
        return available_cells

# Getters / Setters
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Return the corresponding Cell.

        Returns:
            Cell: corresponding Cell.

        Example:
            >>> maze.get_cell(3,4)
            Cell
        """
        if x < 0 or y < 0:
            return None
        try:
            return self.maze_list[y][x]
        except Exception:
            return None

    @property
    def width(self) -> int:
        """Gets the maze width.

        Returns:
            int: Maze width.

        Example:
            >>> print(maze.width)
            5
        """
        if self._width:
            return self._width
        return -1

    @property
    def height(self) -> int:
        """Gets the maze height.

        Returns:
            int: Maze height.

        Example:
            >>> print(maze.height)
            5
        """
        if self._height:
            return self._height
        return -1

    @property
    def exit(self) -> tuple[int, int]:
        """Gets the exit coordinates.

        Returns:
            tuple[int, int]: Exit coordinates.

        Example:
            >>> print(maze.exit)
            (2, 2)
        """
        if self._exit:
            return self._exit
        return (-1, -1)

    @property
    def entry(self) -> tuple[int, int]:
        """Gets the maze entry coordinates.

        Returns:
            tuple[int, int]: Maze entry coordinates.

        Example:
            >>> print(maze.width)
            5
        """
        if self._entry:
            return self._entry
        return (-1, -1)

# Getters / Setters
    @property
    def maze_list(self) -> list[list[Cell]]:
        """Gets the maze width.

        Returns:
            int: Maze width.

        Example:
            >>> print(maze.width)
            5
        """
        return self._maze
