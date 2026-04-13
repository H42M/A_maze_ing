"""A Star Algorythm module."""


from maze.Maze import Maze
from maze.Cell import Cell
from algo.Dfs import Instruct

from enum import Enum
from typing import Any
import heapq


class A_Star:
    """A_Star algo class."""

    def __init__(self, maze: Maze) -> None:
        """Initialize a A Star class instance.

        Args:
            maze (Maze): Current maze to solve

        Example:
            >>> astar = A_Star(maze)
        """
        self.__maze = maze
        self.__traveled: list[Cell] = []

    def solve(self) -> list[Cell]:
        """Solve the current maze.

        Returns:
            list[Cell]: exit path

        Example:
            >>> astar = A_Star(maze)
        """
        start = self.__maze.entry
        counter = 0

        heap = [(self.__get_h(start), 0, counter, start, [start])]
        visited = set()

        while heap:
            f, g, _, cell, path = heapq.heappop(heap)
            import time
            from display.Display import Display
            import os
            self.__maze.add_to_soluce(cell)
            os.system("clear")
            print(f"Cell {cell.pos}: {f}, {g}")
            Display.print_maze(self.__maze)
            time.sleep(0.5)

            if cell == self.__maze.exit:
                print("Exit found!")
                time.sleep(5)
                return path
            if cell not in visited:
                visited.add(cell)

            for option in self.__get_av_options(cell):
                neigh = option[Instruct.NEIGH_CELL]
                if neigh not in visited:
                    new_g = g + 1
                    new_f = new_g + self.__get_h(neigh)
                    counter += 1
                    heapq.heappush(heap, (new_f, new_g, counter,
                                          neigh, path + [neigh]))
        return []

    def __get_h(self, cell: Cell, ) -> float:
        return (abs(cell.x - self.__maze.exit.x) +
                abs(cell.y - self.__maze.exit.y))

    def __get_av_options(self, cell: Cell) -> list[Any]:
        options = self.__get_options(cell)
        av_options = []
        for option in options:
            if isinstance(option[Instruct.NEIGH_CELL], Cell):
                neigh = option[Instruct.NEIGH_CELL]
                cur_cell = option[Instruct.CUR_CELL]
                cell_wall = option[Instruct.CUR_WALL]
                neigh_wall = option[Instruct.NEIGH_WALL]
                if (not getattr(cur_cell, cell_wall) and
                        not getattr(neigh, neigh_wall) and
                        neigh not in self.__traveled):
                    av_options.append(option)
        return av_options

    def __get_options(self, cell: Cell
                      ) -> list[dict[Enum, Any]]:
        return [
                {
                    Instruct.NEIGH_CELL: self.__maze.get_cell(cell.x - 1,
                                                              cell.y),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "w",
                    Instruct.NEIGH_WALL: "e"
                 },
                {
                    Instruct.NEIGH_CELL: self.__maze.get_cell(cell.x + 1,
                                                              cell.y),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "e",
                    Instruct.NEIGH_WALL: "w"
                 },
                {
                    Instruct.NEIGH_CELL: self.__maze.get_cell(cell.x,
                                                              cell.y - 1),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "n",
                    Instruct.NEIGH_WALL: "s"
                 },
                {
                    Instruct.NEIGH_CELL: self.__maze.get_cell(cell.x,
                                                              cell.y + 1),
                    Instruct.CUR_CELL: cell,
                    Instruct.CUR_WALL: "s",
                    Instruct.NEIGH_WALL: "n"
                 },
            ]
