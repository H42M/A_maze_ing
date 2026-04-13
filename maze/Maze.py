"""Maze class management."""


from .Cell import Cell
from Logs import Log
from config.Config import Config
from Errors import MazeError

from typing import Optional, Union
import os
from time import sleep
import random


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
        self.__soluce: list[Cell] = []
        self._maze: list[list[Cell]] = []

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
        self._maze = maze

        # __ 42 Logo ______
        LOGO_42_W = 7
        LOGO_42_H = 5
        mid_cell = self.get_cell(
            int((self.width - LOGO_42_W) / 2),
            int((self.height - LOGO_42_H) / 2),
        )
        if mid_cell:
            self.generate_42(mid_cell)
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

    def generate_maze(self, seed: Optional[int] = None,
                      animate: Optional[float] = None) -> None:
        """Build comlplete random maze based on his seed.

        Returns:
            Cell: available Cell list.

        Example:
            >>> maze.available_cells()
            [Cell, Cell, ...]
        """
        from display.Display import Display
        from algo.Dfs import Dfs, Instruct
        if not seed:
            seed = random.randint(1000, 1000000)
        dfs = Dfs(self.__logs, self.entry, self, seed)
        instruct = dfs.get_build_instruct()

        while (instruct):
            setattr(instruct[Instruct.CUR_CELL],
                    instruct[Instruct.CUR_WALL], False)
            setattr(instruct[Instruct.NEIGH_CELL],
                    instruct[Instruct.NEIGH_WALL], False)

            dfs.set_current_cell(instruct[Instruct.NEIGH_CELL])
            instruct = dfs.get_build_instruct()
            if animate:
                os.system("clear")
                Display.print_maze(self)
                sleep(animate)
        if not self._perfect:
            self.__break_random_walls()
            if animate:
                sleep(2)
                os.system("clear")
                Display.print_maze(self)
                sleep(2)
        self.__reset_visited()

    def resolve_a_star(self, animate: Optional[float] = None) -> None:
        """Resolve current maze thanks to A* algo.

        Example:
            >>> maze.resolve()
        """
        from algo.A_Star import A_Star
        from display.Display import Display

        astar = A_Star(self)
        self.__soluce = astar.solve(animate)
        os.system("clear")
        Display.print_maze(self)

    def __reset_visited(self) -> None:
        for y in self._maze:
            for cell in y:
                cell.visited = False

    def generate_42(self, starting_cell: Cell) -> None:
        """Generate 42 logo in maze.

        Args:
            cell (Cell): 42 logo Start.

        Example:
            >>> maze.genrate_42()
        """
        starting_cell.visited = True
        starting_cell.is42 = True
        cell: Optional[Cell] = starting_cell
        # Number 4:
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x, cell.y + 1)
                if cell:
                    cell.visited = True
                    cell.is42 = True
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x + 1, cell.y)
                if cell:
                    cell.visited = True
                    cell.is42 = True
        for _ in range(2):
            if cell:
                cell = self.get_cell(cell.x, cell.y + 1)
                if cell:
                    cell.visited = True
                    cell.is42 = True

        # Number 2:
        cell = self.get_cell(starting_cell.x + 4, starting_cell.y)
        if cell:
            cell.visited = True
            cell.is42 = True

            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x + 1, cell.y)
                    if cell:
                        cell.visited = True
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x, cell.y + 1)
                    if cell:
                        cell.visited = True
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x - 1, cell.y)
                    if cell:
                        cell.visited = True
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x, cell.y + 1)
                    if cell:
                        cell.visited = True
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell(cell.x + 1, cell.y)
                    if cell:
                        cell.visited = True
                        cell.is42 = True

    def __break_random_walls(self) -> None:
        neigh_map = {
            'n': ('s', 0, -1),
            's': ('n', 0, +1),
            'e': ('w', +1, 0),
            'w': ('e', -1, 0)
        }

        end_points: list[Cell] = []
        for y in self._maze:
            for cell in y:
                if (sum([getattr(cell, w) for w in "nsew"]) >= 3 and
                        not cell.is42):
                    end_points.append(cell)

        for cell in end_points:
            walls_present = [w for w in "nsew" if getattr(cell, w)]
            wall = random.choice(walls_present)

            neigh_wall, dx, dy = neigh_map[wall]
            neigh = self.get_cell(cell.x + dx, cell.y + dy)

            if neigh and not neigh.is42:
                setattr(cell, wall, False)
                setattr(neigh, neigh_wall, False)

    def reset(self) -> None:
        """Reset the current maze.

        Example:
            >>> maze.reset()
        """
        self.__reset_visited()
        self._maze = self.default_maze()
        self.__soluce = []

    def get_soluce_as_str(self) -> str:
        """Get soluce path as str.

        Returns:
            str: Soluce path

        Example:
            >>> maze.get_soluce_as_str()
            "WSSENW..."
        """
        final_str = ''
        for i, cell in enumerate(self.__soluce):
            if i < len(self.__soluce) - 1:
                if self.__soluce[i + 1].x == cell.x + 1:
                    final_str += 'E'
                elif self.__soluce[i + 1].x == cell.x - 1:
                    final_str += 'W'
                elif self.__soluce[i + 1].y == cell.y - 1:
                    final_str += 'N'
                elif self.__soluce[i + 1].y == cell.y + 1:
                    final_str += 'S'
        return final_str

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

    def get_soluce(self) -> list[Cell]:
        """Return the soluce path.

        Returns:
            list[Cell]: solution path.

        Example:
            >>> maze.get_soluce()
            [...]
        """
        return self.__soluce

    def add_to_soluce(self, cell: Cell) -> None:
        """Add a cell to the soluce path.

        Example:
            >>> maze.add_to_soluce(Cell)
        """
        self.__soluce.append(cell)

    def remove_from_soluce(self, elm: Union[int, Cell]) -> None:
        """Remove a cell from the soluce path.

        Args:
            Union[int, Cell]: cell's index to remove or Cell to remove

        Example:
            >>> maze.get_soluce()
            [...]
        """
        if isinstance(elm, int):
            self.__soluce.pop(elm)
        elif isinstance(elm, Cell):
            if elm in self.__soluce:
                index = self.__soluce.index(elm)
                self.__soluce.pop(index)

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
