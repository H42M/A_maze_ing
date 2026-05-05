from Maze.Maze import Maze
from Maze.Cell import Cell

import random
from typing import Optional


class DFS:
    """Generate a maze using depth-first search."""

    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        """Initialize the generator."""
        self.__visited: list[Cell] = []
        self.__maze = maze
        if maze.entry:
            self.__cell = maze.entry
        if seed:
            random.seed(seed)

    def get_instruct(self) -> Optional["Instruct"]:
        """Return the next wall-removal instruction."""
        self.__visited.append(self.__cell)
        if self.__cell == self.__maze.exit:
            index = self.__visited.index(self.__cell)
            self.__cell = self.__visited[index - 1]
        av_neighs = self.get_av_neigh()

        index = 1
        while (not av_neighs):
            index = self.__visited.index(self.__cell)
            self.__cell = self.__visited[index - 1]
            av_neighs = self.get_av_neigh()
            if index == 0 and not av_neighs:
                return None

        instruct = random.choice(av_neighs)
        self.__cell = instruct._neigh
        return instruct

    def get_av_neigh(self) -> list["Instruct"]:
        """Return instructions for available neighbors."""
        neigh_list = self.__get_neigh()
        av_neighs = []
        for wall, neigh in neigh_list.items():
            if neigh not in self.__visited and not neigh.is42:
                av_neighs.append(Instruct(
                    cell=self.__cell,
                    wall=wall,
                    neigh=neigh,
                    neigh_wall=self.__opposite_wall(wall)
                ))
        return av_neighs

    def __get_neigh(self) -> dict[str, Cell]:
        """Return adjacent cells by wall direction."""
        neigh_list: dict[str, Cell] = {}
        infos: dict[str, tuple[int, int]] = {
            'n': (0, -1),
            's': (0, 1),
            'e': (1, 0),
            'w': (-1, 0)
        }
        for wall, dir in infos.items():
            neigh_pos = (self.__cell.pos[0] + dir[0],
                         self.__cell.pos[1] + dir[1])
            neigh_cell = self.__maze.get_cell((neigh_pos[0], neigh_pos[1]))
            if neigh_cell:
                neigh_list[wall] = neigh_cell
        return neigh_list

    def __opposite_wall(self, wall: str) -> str:
        """Return the opposite wall direction."""
        if wall == 'n':
            return 's'
        elif wall == 's':
            return 'n'
        elif wall == 'e':
            return 'w'
        elif wall == 'w':
            return 'e'
        else:
            return "None"


class Instruct:
    """Store a wall-removal instruction."""

    def __init__(self, cell: Cell, wall: str,
                 neigh: Cell, neigh_wall: str) -> None:
        """Initialize the instruction."""
        self.__cell = cell
        self.__wall = wall
        self.__neigh = neigh
        self.__neigh_wall = neigh_wall

    @property
    def _cell(self) -> Cell:
        return self.__cell

    @_cell.setter
    def _cell(self, value: Cell) -> None:
        self.__cell = value

    @property
    def _wall(self) -> str:
        return self.__wall

    @_wall.setter
    def _wall(self, value: str) -> None:
        self.__wall = value

    @property
    def _neigh(self) -> Cell:
        return self.__neigh

    @_neigh.setter
    def _neigh(self, value: Cell) -> None:
        self.__neigh = value

    @property
    def _neigh_wall(self) -> str:
        return self.__neigh_wall

    @_neigh_wall.setter
    def _neigh_wall(self, value: str) -> None:
        self.__neigh_wall = value