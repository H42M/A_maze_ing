"""Depth-first search maze generation module.

Implements the DFS algorithm for generating random mazes by randomly
choosing unvisited neighbors and carving passages.
"""

from Maze.Maze import Maze
from Maze.Cell import Cell

import random
from typing import Optional


class DFS:
    """Depth-first search maze generation.

    Generates a random maze using the depth-first search algorithm
    by recursively visiting unvisited neighbors and removing walls
    between cells.

    Attributes:
        _DFS__visited (list[Cell]): List of visited cells.
        _DFS__maze (Maze): The maze being generated.
        _DFS__cell (Cell): Current cell in the generation process.
    """

    def __init__(self, maze: Maze, seed: Optional[int] = None) -> None:
        """Initialize DFS maze generator.

        Args:
            maze (Maze): The maze instance to generate.
        """
        self.__visited: list[Cell] = []
        self.__maze = maze
        if maze.entry:
            self.__cell = maze.entry
        if seed:
            random.seed(seed)

    def get_instruct(self) -> Optional["Instruct"]:
        """Get next instruction for maze generation step.

        Returns:
            Optional[Instruct]: An instruction for wall removal, or None
                if generation is complete.
        """
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
        """Get all available unvisited neighbors as instructions.

        Returns:
            list[Instruct]: List of instructions for unvisited neighbors.
        """
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
        """Get all adjacent cells in four cardinal directions.

        Returns:
            dict[str, Cell]: Dictionary mapping directions ('n', 's', 'e', 'w')
                to adjacent Cell objects.
        """
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
        """Get the opposite wall direction.

        Args:
            wall (str): Wall direction ('n', 's', 'e', 'w').

        Returns:
            str: The opposite direction or 'None' if invalid.
        """
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


"""Instruction class for maze wall removal.

Represents an instruction to remove a wall between two adjacent cells.
"""


class Instruct:
    """Represents a maze generation instruction.

    Contains information about a wall to remove between two adjacent cells
    during depth-first search maze generation.

    Attributes:
        _Instruct__cell (Cell): Current cell.
        _Instruct__wall (str): Wall identifier on current cell.
        _Instruct__neigh (Cell): Neighbor cell.
        _Instruct__neigh_wall (str): Wall identifier on neighbor cell.
    """

    def __init__(self, cell: Cell, wall: str,
                 neigh: Cell, neigh_wall: str) -> None:
        """Initialize a maze generation instruction.

        Args:
            cell (Cell): Current cell.
            wall (str): Wall identifier on current cell ('n', 's', 'e', 'w').
            neigh (Cell): Adjacent neighbor cell.
            neigh_wall (str): Wall identifier on neighbor cell.
        """
        self.__cell = cell
        self.__wall = wall
        self.__neigh = neigh
        self.__neigh_wall = neigh_wall

    @property
    def _cell(self) -> Cell:
        """Get the current cell.

        Returns:
            Cell: The current cell in the instruction.
        """
        return self.__cell

    @_cell.setter
    def _cell(self, value: Cell) -> None:
        """Set the current cell.

        Args:
            value (Cell): The new current cell.
        """
        self.__cell = value

    @property
    def _wall(self) -> str:
        """Get the wall identifier.

        Returns:
            str: Wall direction ('n', 's', 'e', or 'w').
        """
        return self.__wall

    @_wall.setter
    def _wall(self, value: str) -> None:
        """Set the wall identifier.

        Args:
            value (str): Wall direction ('n', 's', 'e', or 'w').
        """
        self.__wall = value

    @property
    def _neigh(self) -> Cell:
        """Get the neighbor cell.

        Returns:
            Cell: The neighbor cell in the instruction.
        """
        return self.__neigh

    @_neigh.setter
    def _neigh(self, value: Cell) -> None:
        """Set the neighbor cell.

        Args:
            value (Cell): The new neighbor cell.
        """
        self.__neigh = value

    @property
    def _neigh_wall(self) -> str:
        """Get the neighbor's wall identifier.

        Returns:
            str: Wall direction on neighbor ('n', 's', 'e', or 'w').
        """
        return self.__neigh_wall

    @_neigh_wall.setter
    def _neigh_wall(self, value: str) -> None:
        """Set the neighbor's wall identifier.

        Args:
            value (str): Wall direction on neighbor ('n', 's', 'e', or 'w').
        """
        self.__neigh_wall = value
