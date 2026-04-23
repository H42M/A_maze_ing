"""A Star Algorythm module."""


from Maze.Maze import Maze
from Maze.Cell import Cell

from typing import Any, Optional
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

    def solve(self, animate: Optional[float] = None) -> list[Cell]:
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
            if animate:
                self.__maze.add_to_soluce(cell)
                print(f"Cell {cell.pos}: {f}, {g}")

            if cell == self.__maze.exit:
                return path
            if cell not in visited:
                visited.add(cell)

            for option in self.__get_av_options(cell):
                neigh = option['neigh_cell']
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
            if isinstance(option['neigh_cell'], Cell):
                neigh = option['neigh_cell']
                cur_cell = option['cell']
                cell_wall = option['wall']
                neigh_wall = option['neigh_wall']
                if (not getattr(cur_cell, cell_wall) and
                        not getattr(neigh, neigh_wall) and
                        neigh not in self.__traveled):
                    av_options.append(option)
        return av_options

    def __get_options(self, cell: Cell
                      ) -> list[dict[str, Any]]:
        return [
                {
                    'neigh_cell': self.__maze.get_cell((cell.x - 1, cell.y)),
                    'cell': cell,
                    'wall': "w",
                    'neigh_wall': "e"
                 },
                {
                    'neigh_cell': self.__maze.get_cell((cell.x + 1, cell.y)),
                    'cell': cell,
                    'wall': "e",
                    'neigh_wall': "w"
                 },
                {
                    'neigh_cell': self.__maze.get_cell((cell.x, cell.y - 1)),
                    'cell': cell,
                    'wall': "n",
                    'neigh_wall': "s"
                 },
                {
                    'neigh_cell': self.__maze.get_cell((cell.x, cell.y + 1)),
                    'cell': cell,
                    'wall': "s",
                    'neigh_wall': "n"
                 },
            ]
