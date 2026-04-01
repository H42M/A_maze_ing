"""Maze class management."""


from .Cell import Cell
from Logs import Log
from config.Config import Config


class Maze:
    """Maze class."""

    def __init__(self, logs: Log, config: Config) -> None:
        """Initialize a Maze class instance.

        Args:
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
            for _ in range(self._height):
                row = []
                for _ in range(self._width):
                    row.append(Cell())
                maze.append(row)
        return maze

# Getters / Setters
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
