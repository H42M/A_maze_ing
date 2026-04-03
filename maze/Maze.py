"""Maze class management."""


from .Cell import Cell
from Logs import Log
from config.Config import Config
from Errors import MazeError

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
        if not config.exit:
            raise MazeError("Exit config not set")
        if not config.width:
            raise MazeError("Width config not set")
        if not config.height:
            raise MazeError("Height config not set")
        if not config.entry:
            raise MazeError("Entry config not set")

        self.__logs = logs
        self._width: int = config.width
        self._height: int = config.height
        self._entry: tuple[int, int] = config.entry
        self._exit: tuple[int, int] = config.exit
        self._perfect: bool = config.perfect
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

    def generate_42(self, starting_cell: Cell) -> None:
        """Generate 42 logo in maze.

        Args:
            cell (Cell): 42 logo Start.

        Example:
            >>> maze.genrate_42()
        """
        starting_cell.visited = True
        cell: Optional[Cell] = starting_cell
        # Number 4:
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x, cell.y + 1)
                if cell:
                    cell.visited = True
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x + 1, cell.y)
                if cell:
                    cell.visited = True
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x, cell.y + 1)
                if cell:
                    cell.visited = True

        # Number 2:
        cell = self.get_cell(starting_cell.x + 4, starting_cell.y)
        if cell:
            cell.visited = True

            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x + 1, cell.y)
                    if cell:
                        cell.visited = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x, cell.y + 1)
                    if cell:
                        cell.visited = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x - 1, cell.y)
                    if cell:
                        cell.visited = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x, cell.y + 1)
                    if cell:
                        cell.visited = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x + 1, cell.y)
                    if cell:
                        cell.visited = True

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
        return self._width

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
    def exit(self) -> Cell:
        """Gets the exit coordinates.

        Returns:
            tuple[int, int]: Exit coordinates.

        Example:
            >>> print(maze.exit)
            (2, 2)
        """

        cell_exit = self.get_cell(self._exit[0], self._exit[1])
        if cell_exit:
            return cell_exit
        else:
            raise MazeError("Exit cell has not found")

    @property
    def entry(self) -> Cell:
        """Gets the maze entry coordinates.

        Returns:
            tuple[int, int]: Maze entry coordinates.

        Example:
            >>> print(maze.width)
            5
        """
        cell_entry = self.get_cell(self._entry[0], self._entry[1])
        if cell_entry:
            return cell_entry
        else:
            raise MazeError("Entry Cell has not found")

    @property
    def perfect(self) -> bool:
        """Gets the perfect maze status.

        Returns:
            bool: Is  maze must be perfect.

        Example:
            >>> print(maze.perfect)
            True
        """
        if self._perfect:
            return self._perfect
        return (False)

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
