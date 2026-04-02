"""DFS management algorithm."""


from maze import Maze, Cell
from Logs import Log
from Errors import DFSError
from display.Display import Display

from typing import Optional, Any
import random
from time import sleep
import os


class Dfs:
    """Dfs algorithm class."""

    def __init__(self, logs: Log,
                 seed: Optional[int] = None) -> None:
        """Initialize a DFS class instance.

        Args:
            logs (Log): Log manager

            seed (int): Seed to generate random maze

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        if not seed:
            seed = random.randint(1000, 1000000)
        self.__seed = seed
        self.__logs = logs
        self.__traveled: list[Cell] = []
        self.__current_cell: Cell

    def build(self, maze_obj: Maze) -> None:
        """Build the maze.

        Args:
            maze (Maze): Current maze to build

        Example:
            >>> maze = Maze(5, 5, (2,2), (5,5))
        """
        startx, starty = maze_obj.entry
        current_cell = maze_obj.get_cell(startx, starty)
        if current_cell:
            self.__current_cell = current_cell
        else:
            raise DFSError("Starting Cell doesn't exist")
        random.seed(self.__seed)
        os.system("clear")
        Display.print_maze_v2(maze_obj)

        while (len(maze_obj.available_cells()) > 0):
            self.__current_cell.visited = True
            cur_cell_pos = (self.__current_cell.x, self.__current_cell.y)
            if self.__current_cell not in self.__traveled:
                if not maze_obj.perfect:
                    self.__traveled.append(self.__current_cell)
                elif maze_obj.perfect and cur_cell_pos != maze_obj.exit:
                    self.__traveled.append(self.__current_cell)

            if cur_cell_pos == maze_obj.exit and maze_obj.perfect:
                self.__current_cell = self.get_first_pos_av(maze_obj)
                sleep(5)

            # print("Travel: ")
            # [print(f" ({travel.x}, {travel.y})")
            # for travel in self.__traveled]

            av_options = self.get_available_options(
                maze_obj, self.__current_cell.x, self.__current_cell.y)
            if len(av_options) > 0:
                print(f"Available neighbors: {len(av_options)}")
                rand_neigh = random.randint(0, len(av_options) - 1)
                selected = av_options[rand_neigh]

                setattr(self.__current_cell, selected['wall'], False)
                self.__current_cell = selected["neight"]
                setattr(self.__current_cell, selected['neigh_wall'], False)

                os.system("clear")
                Display.print_maze_v2(maze_obj)
                print(f"Cell remaining: {len(maze_obj.available_cells())}")
                sleep(0.1)
            else:
                current_index = self.__traveled.index(self.__current_cell)
                self.__current_cell = self.__traveled[current_index - 1]

    def get_available_options(self, maze_obj: Maze, curx: int, cury: int
                              ) -> list[dict[str, Any]]:
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
                {"neight": maze_obj.get_cell(curx - 1, cury),
                 "wall": "w", "neigh_wall": "e"},
                {"neight": maze_obj.get_cell(curx + 1, cury),
                 "wall": "e", "neigh_wall": "w"},
                {"neight": maze_obj.get_cell(curx, cury - 1),
                 "wall": "n", "neigh_wall": "s"},
                {"neight": maze_obj.get_cell(curx, cury + 1),
                 "wall": "s", "neigh_wall": "n"},
            ]
        av_options = []
        for option in options:
            if isinstance(option["neight"], Cell):
                if not option['neight'].visited:
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

        i = len(self.__traveled) - 5
        current_cell = self.__traveled[i]
        while len(self.get_available_options(maze_obj, current_cell.x,
                                             current_cell.y)) < 1:
            i -= 1
            current_cell = self.__traveled[i]
        return current_cell
