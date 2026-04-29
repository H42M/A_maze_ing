"""Maze generation and management module.

Provides the Maze class for creating, rendering, and managing maze
structures with pathfinding and texture support.
"""

import pygame

from Config.Config import Config
from Maze.Cell import Cell
from render.RenderObj import RenderObj
from Config.GameState import GameState

from typing import Union, Optional


class Maze:
    """Represents a maze with cells, walls, and pathfinding.

    Manages maze generation using depth-first search, rendering,
    texture management, and solution path computation using A* algorithm.

    Attributes:
        _Maze__width (int): Width of the maze in cells.
        _Maze__height (int): Height of the maze in cells.
        _Maze__entry (tuple[int, int]): Entry point coordinates.
        _Maze__exit (tuple[int, int]): Exit point coordinates.
    """

    def __init__(self, config: Config,
                 wall_tex: Union[tuple[int, int, int], pygame.Surface],
                 exit_tex: Union[tuple[int, int, int], pygame.Surface],
                 sol_tex: Union[tuple[int, int, int], pygame.Surface]) -> None:
        """Initialize a maze with configuration and textures.

        Args:
            config (Config): Maze configuration object.
            wall_tex (Union[tuple[int, int, int], pygame.Surface]):
            Wall texture.
            exit_tex (Union[tuple[int, int, int], pygame.Surface]):
            Exit texture.
            sol_tex (Union[tuple[int, int, int], pygame.Surface]):
            Solution texture.
        """
        from Maze.algo.Dfs import DFS
        self.__width = config.width
        self.__height = config.height
        self.__entry = config.entry
        self.__exit = config.exit

        self.__cell_size = GameState.get_cell_size()
        self.__wall_thickness = GameState.get_wall_thickness()
        self.__gap = GameState.get_gap()

        self.__wall_tex: Union[tuple[int, int, int], pygame.Surface] = wall_tex
        self.__exit_tex: Union[tuple[int, int, int], pygame.Surface] = exit_tex
        self.__sol_tex: Union[tuple[int, int, int], pygame.Surface] = sol_tex
        self.__is_maze_generated = False
        self.__maze_lst = self.__empty_maze()
        self.__set_42_logo()
        self.__dfs = DFS(self)

        self.__soluce: list[Cell] = []
        self.__display_soluce = False
        self.set_textures(wall_tex, exit_tex, sol_tex)

    def __empty_maze(self) -> list[list[Cell]]:
        """Create an empty maze filled with cells.

        Returns:
            list[list[Cell]]: 2D grid of Cell objects.
        """
        maze = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                row.append(Cell(x, y, self.__wall_tex,))
            maze.append(row)
        return maze

    def generate_anim(self):
        """Generate maze step-by-step for animation.

        Returns:
            bool: True if generation is complete, False if continuing.
        """
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
        """Render the maze and all cells to the screen.

        Args:
            screen (pygame.Surface): The display surface to render on.
        """
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
                cell.render(screen)

    def get_cell(self, coord: tuple[int, int]):
        """Get a cell at the specified coordinate.

        Args:
            coord (tuple[int, int]): (x, y) coordinate in maze grid.

        Returns:
            Optional[Cell]: The cell at given coordinates or None.
        """
        x, y = coord
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__maze_lst[y][x]
        return None

    def set_textures(self,
                     wall: Union[tuple[int, int, int], pygame.Surface],
                     exit: Union[tuple[int, int, int], pygame.Surface],
                     soluce: Union[tuple[int, int, int], pygame.Surface]):
        """Set textures for all maze cells.

        Args:
            wall (Union[tuple[int, int, int], pygame.Surface]): Wall texture.
            exit (Union[tuple[int, int, int], pygame.Surface]): Exit texture.
            soluce (Union[tuple[int, int, int], pygame.Surface]):
            Solution texture.
        """
        for row in self.__maze_lst:
            for cell in row:
                if isinstance(wall, pygame.Surface):
                    cell.wall_texture = wall
                    if cell == self.exit and isinstance(exit, pygame.Surface):
                        cell.set_exit_texture(exit)
                    elif cell in self.__soluce and isinstance(soluce,
                                                              pygame.Surface):
                        print('Cell texture set')
                        cell.set_soluce_texture(soluce)
                else:
                    cell.color = wall
        self.__wall_tex = wall
        self.__exit_tex = exit
        self.__sol_tex = soluce

    def update_texture(self, wall: pygame.Surface,
                       exit: pygame.Surface,
                       soluce: pygame.Surface) -> None:
        """Update maze textures on theme change.

        Args:
            wall (pygame.Surface): New wall texture.
            exit (pygame.Surface): New exit texture.
            soluce (pygame.Surface): New solution texture.
        """
        self.set_textures(wall, exit, soluce)

    def solve(self):
        """Compute the solution path from entry to exit using A* algorithm.

        Uses the A* pathfinding algorithm to find the optimal path and
        marks cells as part of the solution.
        """
        from Maze.algo.AStar import A_Star
        astar = A_Star(self)
        self.__soluce = astar.solve()
        print("Soluce: ")
        for cell in self.__soluce:
            cell.display_soluce = self.__display_soluce
        self.set_textures(self.__wall_tex, self.__exit_tex, self.__sol_tex)

    def add_to_soluce(self, cell: Cell) -> None:
        """Add a cell to the solution path.

        Args:
            cell (Cell): Cell to add to the solution path.
        """
        if self.get_cell(cell.pos):
            self.__soluce.append(cell)

    def reset(self):
        """Reset the maze to initial state (regenerate and clear solution).

        Clears the current maze, regenerates cells, resets the DFS state,
        and clears the solution path.
        """
        self.__is_maze_generated = False
        self.__maze_lst = self.__empty_maze()
        self.__set_42_logo()
        self.__soluce = []

    def __set_42_logo(self) -> None:
        """Generate a 42 school logo pattern in the maze.

        Creates the visual pattern of '42' using non-walkable cells
        positioned in the center of the maze.
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

    def set_display_soluce(self, value: Optional[bool] = None):
        """Toggle or set the display state of the solution path.

        Args:
            value (Optional[bool]): If None, toggles current state.
                If True/False, sets to that state.
        """
        if value is None:
            self.__display_soluce = not self.__display_soluce
        else:
            self.__display_soluce = value
        for cell in self.__soluce:
            cell.display_soluce = self.__display_soluce

    def get_display_soluce(self):
        """Check if solution path is currently displayed.

        Returns:
            bool: True if solution is being displayed, False otherwise.
        """
        return self.__display_soluce

    @property
    def entry(self) -> Cell:
        """Get the entry cell of the maze.

        Returns:
            Cell: The entry point cell.

        Raises:
            ValueError: If entry cell not found.
        """
        entry = self.get_cell(self.__entry)
        if entry:
            return entry
        else:
            raise ValueError("Entry cell has not found")

    @property
    def exit(self) -> Cell:
        """Get the exit cell of the maze.

        Returns:
            Cell: The exit point cell.

        Raises:
            ValueError: If exit cell not found.
        """
        exit = self.get_cell(self.__exit)
        if exit:
            return exit
        else:
            raise ValueError("Exit cell has not found")

    @property
    def cell_size(self):
        """Get the size of each maze cell.

        Returns:
            tuple: Cell dimensions (width, height).
        """
        return self.__cell_size

    @property
    def maze_lst(self):
        """Get the 2D list of all maze cells.

        Returns:
            list[list[Cell]]: Grid of cells.
        """
        return self.__maze_lst

    @property
    def soluce(self) -> list[Cell]:
        """Get the list of cells forming the solution path.

        Returns:
            list[Cell]: Cells in the solution path.
        """
        return self.__soluce

    @property
    def wall_thickness(self):
        """Get the thickness of maze walls in pixels.

        Returns:
            int: Wall thickness.
        """
        return self.__wall_thickness

    @property
    def gap(self):
        """Get the centering offset for the maze.

        Returns:
            tuple: Gap offset (x, y).
        """
        return self.__gap

    @property
    def color(self):
        """Get the maze color.

        Returns:
            tuple: RGB color tuple.
        """
        return self.__color

    @color.setter
    def color(self, value):
        """Set the maze color.

        Args:
            value (tuple): RGB color tuple.
        """
        self.__color = value

    @property
    def display_soluce(self):
        """Get whether solution path is displayed.

        Returns:
            bool: True if solution is shown, False otherwise.
        """
        return self.__display_soluce

    @property
    def is_maze_generated(self):
        """Get whether maze generation is complete.

        Returns:
            bool: True if generation finished, False otherwise.
        """
        return self.__is_maze_generated

    @is_maze_generated.setter
    def is_maze_generated(self, value):
        """Set maze generation completion status.

        Args:
            value (bool): True if generation is complete.
        """
        self.__is_maze_generated = value
