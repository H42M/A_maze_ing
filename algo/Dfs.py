"""DFS management algorithm."""


from maze import Maze, Cell
from Logs import Log
from Errors import DFSError


from typing import Optional, Any
import random
from enum import Enum


class Dfs:
    """Dfs algorithm class."""

    def __init__(self, logs: Log, entry: Cell, maze: Maze,
                 seed: int) -> None:
        """Initialize a DFS class instance.

        Args:
            logs (Log): Log manager

            seed (int): Seed to generate random maze

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        random.seed(seed)
        self.__seed = seed
        self.__logs = logs
        self.__maze = maze
        self.__traveled: list[Cell] = []
        self.__current_cell: Cell = entry

    def get_instruct(self) -> Optional[dict[Enum, Any]]:
        """Build the maze.

        Args:
            maze (Maze): Current maze to build

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        self.__current_cell.visited = True

        if (self.__current_cell not in self.__traveled and
                self.__current_cell != self.__maze.exit):
            self.__traveled.append(self.__current_cell)

        if self.__current_cell == self.__maze.exit:
            self.__current_cell = self.get_first_pos_av(self.__maze)

        i = 1
        count = 0
        while (i >= 0):
            count += 1
            av_options = self.get_available_options(self.__maze,
                                                    self.__current_cell)
            if len(av_options) > 0:
                rand_neigh = random.randint(0, len(av_options) - 1)
                selected = av_options[rand_neigh]
                return selected
            else:
                i = self.__traveled.index(self.__current_cell)
                if i == 0:
                    return None
                self.__current_cell = self.__traveled[i - 1]
            if count > 5000:
                raise DFSError(f"Loop detected: index = {i}")
        return None

    def get_available_options(self, maze_obj: Maze, cell: Cell
                              ) -> list[dict[Enum, Any]]:
        """Choose a cell amoung the 4 neighbors.

        Args:
            maze_obj (Maze): Current maze
            curx (int): Current position X
            cury (int): Current positoin y

        Return:
            list[dict[str, any]]: list of available options amoug neighbors.

        Example:
            >>> self.get_available_options(...)
            [<option1>, <option2>, ...]
        """
        options = [
                {
                    Instruct.NEIGH_CELL: maze_obj.get_cell(cell.x - 1, cell.y),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "w",
                    Instruct.NEIGH_WALL: "e"
                 },
                {
                    Instruct.NEIGH_CELL: maze_obj.get_cell(cell.x + 1, cell.y),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "e",
                    Instruct.NEIGH_WALL: "w"
                 },
                {
                    Instruct.NEIGH_CELL: maze_obj.get_cell(cell.x, cell.y - 1),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "n",
                    Instruct.NEIGH_WALL: "s"
                 },
                {
                    Instruct.NEIGH_CELL: maze_obj.get_cell(cell.x, cell.y + 1),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "s",
                    Instruct.NEIGH_WALL: "n"
                 },
            ]
        av_options = []
        for option in options:
            if isinstance(option[Instruct.NEIGH_CELL], Cell):
                if not option[Instruct.NEIGH_CELL].visited:
                    av_options.append(option)
        return av_options

    def get_first_pos_av(self, maze_obj: Maze) -> Cell:
        """Get the first availbale position back.

        Args:
            maze_obj (Maze): Current maze

        Return:
            Cell: available Cell

        Example:
            >>> self.get_first_pos_av(...)
            Cell
        """
        # current_cell = self.__traveled[0]
        # i = 0
        # while  len(self.get_available_options(maze_obj, current_cell.x,
        # current_cell.y)) < 1:
        #     i += 1
        #     current_cell = self.__traveled[i]
        # return current_cell

        i = len(self.__traveled) - 2
        current_cell = self.__traveled[i]
        while len(self.get_available_options(maze_obj, current_cell)) < 1:
            i -= 1
            current_cell = self.__traveled[i]
        return current_cell

    def set_current_cell(self, cell: Cell) -> None:
        """Set the dfs current cell.

        Args:
            cell: Cell: new current cell

        Example:
            >>> self.set_current_cell(cell)
        """
        if cell:
            self.__current_cell = cell


class Instruct(Enum):
    """List diffrents instructions types."""

    NEIGH_CELL = "NEIGHTBOR_CELL"
    CUR_CELL = "CURRENT_CELL"

    CUR_WALL = "CURRENT_WALL"
    NEIGH_WALL = "NEIGHBOR_WALL"
