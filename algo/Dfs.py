"""DFS management algorithm."""


from maze.Cell import Cell
from maze.Maze import Maze
from Errors import DFSError

from typing import Optional, Any
import random
from enum import Enum


class Dfs:
    """Dfs algorithm class."""

    def __init__(self, entry: Cell, maze: Maze,
                 seed: int) -> None:
        """Initialize a DFS class instance.

        Args:
            logs (Log): Log manager

            seed (int): Seed to generate random maze

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        random.seed(seed)

        self.__maze = maze
        self.__current_cell: Cell = entry
        self.__traveled: list[Cell] = []

    def get_build_instruct(self) -> Optional[dict[Enum, Any]]:
        """Return an instruction as dict.

        Return:
            dict[Instruct, Any]: Instruction containing current cell,
                                 current wall to break, neighbor cell and
                                 neighbor wall to break

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        self.__current_cell.visited = True

        if (self.__current_cell not in self.__traveled and
                self.__current_cell != self.__maze.exit):
            self.__traveled.append(self.__current_cell)

        if self.__current_cell == self.__maze.exit:
            self.__current_cell = self.get_first_pos_av()

        i = 1
        count = 0
        while (i >= 0):
            count += 1
            av_options = self.__get_av_options_build(self.__current_cell)
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

    def get_res_instruct(self) -> Optional[dict[Enum, Any]]:
        """Return an instruction as dict.

        Return:
            dict[Instruct, Any]: Instruction containing current cell,
                                 current wall open, neighbor cell and
                                 neighbor wall open

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        self.__current_cell.visited = True
        # if self.__current_cell == self.__maze.exit:
        #     return "Exit"

        if (self.__current_cell not in self.__traveled):
            self.__traveled.append(self.__current_cell)
        if self.__current_cell not in self.__maze.get_soluce():
            self.__maze.add_to_soluce(self.__current_cell)

        while (True):
            av_options = self.__get_av_options_res(self.__current_cell)
            if len(av_options) > 0:
                print(f"AV OPTIONS: {len(av_options)}")
                print(f"Cur CEll: {self.__current_cell.pos}")
                for opt in av_options:
                    if opt[Instruct.NEIGH_CELL] == self.__maze.exit:
                        return opt
                rand_neigh = random.randint(0, len(av_options) - 1)
                selected = av_options[rand_neigh]
                return selected
            else:
                self.__maze.remove_from_soluce(self.__current_cell)
                traveled_i = self.__traveled.index(self.__current_cell)
                if traveled_i == 0:
                    return None
                self.__current_cell = self.__traveled[traveled_i - 1]

    def __get_av_options_build(self, cell: Cell
                               ) -> list[dict[Enum, Any]]:
        options = self.__get_options(self.__maze, cell)
        av_options = []
        for option in options:
            if isinstance(option[Instruct.NEIGH_CELL], Cell):
                if not option[Instruct.NEIGH_CELL].visited:
                    av_options.append(option)
        return av_options

    def __get_av_options_res(self, cell: Cell
                             ) -> list[dict[Enum, Any]]:
        options = self.__get_options(self.__maze, cell)
        av_options = []
        for option in options:
            if isinstance(option[Instruct.NEIGH_CELL], Cell):
                neigh = option[Instruct.NEIGH_CELL]
                cur_cell = option[Instruct.CUR_CELL]
                cell_wall = option[Instruct.CUR_WALL]
                neigh_wall = option[Instruct.NEIGH_WALL]
                if (not neigh.visited and
                    not getattr(cur_cell, cell_wall) and
                        not getattr(neigh, neigh_wall)):
                    av_options.append(option)
        return av_options

    def __get_options(self, maze_obj: Maze, cell: Cell
                      ) -> list[dict[Enum, Any]]:
        return [
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

    def get_first_pos_av(self) -> Cell:
        """Get the first availbale position back.

        Return:
            Cell: available Cell

        Example:
            >>> self.get_first_pos_av(...)
            Cell
        """
        i = len(self.__traveled) - 2
        current_cell = self.__traveled[i]
        while len(self.__get_av_options_build(current_cell)) < 1:
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
        else:
            print("No Cell selected")


class Instruct(Enum):
    """List diffrents instructions types."""

    NEIGH_CELL = "NEIGHTBOR_CELL"
    CUR_CELL = "CURRENT_CELL"

    CUR_WALL = "CURRENT_WALL"
    NEIGH_WALL = "NEIGHBOR_WALL"
