"""DFS management algorithm."""


from maze import Maze, Cell
from Logs import Log, LogType
from Errors import DFSError
from display.Display import Display

from typing import Optional
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

        while (len(maze_obj.available_cells()) > 0):
            os.system("clear")
            Display.print_maze(maze_obj)
            self.__current_cell.visited = True
            if self.__current_cell not in self.__traveled:
                self.__traveled.append(self.__current_cell)
            # print("Travel: ")
            # [print(f" ({travel.x}, {travel.y})") for travel in self.__traveled]

            curx = self.__current_cell.x
            cury = self.__current_cell.y
            self.__logs.add_log(f"Current pos: ({curx}, {cury})",
                                LogType.LOGINFO)
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

            av_options = [option for option in options
                          if option["neight"] and not option['neight'].visited]
            if len(av_options) > 0:
                print(f"Available neighbors: {len(av_options)}")
                rand_neigh = random.randint(0, len(av_options) - 1)
                selected = av_options[rand_neigh]
                
                setattr(self.__current_cell, selected['wall'], False)
                self.__current_cell = selected["neight"]
                setattr(self.__current_cell, selected['neigh_wall'], False)
            else:
                current_index = self.__traveled.index(self.__current_cell)
                self.__current_cell = self.__traveled[current_index - 1]
            
            print(f"Cell remaining: {len(maze_obj.available_cells())}")

            sleep(0.1)
