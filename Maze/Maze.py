import pygame

from Config.Config import Config
from Maze.Cell import Cell
from render.RenderObj import RenderObj
from Config.GameState import GameState

from typing import Union


class Maze:
    def __init__(self, config: Config) -> None:
        from Maze.algo.Dfs import DFS
        self.__width = config.width
        self.__height = config.height
        self.__entry = config.entry
        self.__exit = config.exit

        self.__cell_size = GameState.get_cell_size()
        self.__wall_thickness = GameState.get_wall_thickness()
        self.__gap = GameState.get_gap()

        self.__is_maze_generated = False
        self.__color: tuple[int, int, int] = (255, 255, 0)
        self.__maze_lst = self.__empty_maze()
        self.__set_42_logo()
        self.__dfs = DFS(self)

        self.__soluce: list[Cell] = []
        self.__display_soluce = True

    def __empty_maze(self) -> list[list[Cell]]:
        maze = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                row.append(Cell(x, y, self.__color,))
            maze.append(row)
        return maze

    def generate_anim(self):
        if self.__is_maze_generated:
            return True

        instruct = self.__dfs.get_instruct()
        if instruct:
            print(instruct._cell.pos)
            setattr(instruct._cell, instruct._wall, False)
            setattr(instruct._neigh, instruct._neigh_wall, False)
            instruct._cell.set_render_cell()
            instruct._neigh.set_render_cell()
            return False

        self.__is_maze_generated = True
        return True

    def render(self, screen: pygame.Surface):
        # Render Background:
        RenderObj((self.__gap[0], self.__gap[1]),
                  ((self.__cell_size[0] * self.__width) +
                  GameState.bloc_size[0],
                  (self.__cell_size[1] * self.__height) +
                   GameState.bloc_size[1]),
                  color=(203, 203, 252),
                  collision=False).render(screen)

        for row in self.__maze_lst:
            for cell in row:
                render_exit = False
                render_soluce = False
                if (cell in self.__soluce and cell != self.exit and
                        cell != self.entry):
                    render_soluce = True
                if cell == self.exit:
                    render_exit = True
                cell.render(screen, render_exit, render_soluce)

    def get_cell(self, coord: tuple[int, int]):
        x, y = coord
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__maze_lst[y][x]
        return None

    def set_color(self, color: Union[tuple[int, int, int],
                                     pygame.Surface]):
        for row in self.__maze_lst:
            for cell in row:
                if isinstance(color, pygame.Surface):
                    cell.wall_texture = color
                else:
                    cell.color = color
        self.__render_maze = []

    def solve(self):
        from Maze.algo.AStar import A_Star
        astar = A_Star(self)
        self.__soluce = astar.solve()
        print("Soluce: ")
        [print(cell.pos) for cell in self.__soluce]

    def add_to_soluce(self, cell: Cell) -> None:
        if self.get_cell(cell.pos):
            self.__soluce.append(cell)

    def __set_42_logo(self) -> None:
        """Generate 42 logo in maze.

        Args:
            cell (Cell): 42 logo Start.

        Example:
            >>> maze.genrate_42()
        """
        starting_cell = self.get_cell((
            (self.__width - 7) // 2,
            (self.__height - 5) // 2
        ))
        if not starting_cell:
            return

        starting_cell.is42 = True
        cell = starting_cell
        # Number 4:
        for _ in range(2):
            if cell:
                cell = self.get_cell((cell.x, cell.y + 1))
                if cell:
                    cell.is42 = True
        for _ in range(2):
            if cell:
                cell = self.get_cell((cell.x + 1, cell.y))
                if cell:
                    cell.is42 = True
        for _ in range(2):
            if cell:
                cell = self.get_cell((cell.x, cell.y + 1))
                if cell:
                    cell.is42 = True

        # Number 2:
        cell = self.get_cell((starting_cell.x + 4, starting_cell.y))
        if cell:
            cell.is42 = True

            for _ in range(2):
                if cell:
                    cell = self.get_cell((cell.x + 1, cell.y))
                    if cell:
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell((cell.x, cell.y + 1))
                    if cell:
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell((cell.x - 1, cell.y))
                    if cell:
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell((cell.x, cell.y + 1))
                    if cell:
                        cell.is42 = True
            for _ in range(2):
                if cell:
                    cell = self.get_cell((cell.x + 1, cell.y))
                    if cell:
                        cell.is42 = True

    @property
    def entry(self) -> Cell:
        entry = self.get_cell(self.__entry)
        if entry:
            return entry
        else:
            raise ValueError("Entry cell has not found")

    @property
    def exit(self) -> Cell:
        exit = self.get_cell(self.__exit)
        if exit:
            return exit
        else:
            raise ValueError("Exit cell has not found")

    @property
    def cell_size(self):
        return self.__cell_size

    @property
    def maze_lst(self):
        return self.__maze_lst

    @property
    def wall_thickness(self):
        return self.__wall_thickness

    @property
    def gap(self):
        return self.__gap

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value
