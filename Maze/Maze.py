import pygame

from Config.Config import Config
from Maze.Cell import Cell
from render.RenderObj import RenderObj
from Config.GameState import GameState

from Errors import MazeError

from typing import Union, Optional


class Maze:
    """Manage maze cells, generation, rendering, and solving."""

    def __init__(self, config: Config,
                 wall_tex: Optional[Union[
                     tuple[int, int, int], pygame.Surface]] = None,
                 exit_tex: Optional[Union[
                     tuple[int, int, int], pygame.Surface]] = None,
                 sol_tex: Optional[Union[
                     tuple[int, int, int], pygame.Surface]] = None,
                 seed: Optional[int] = None
                 ) -> None:
        """Initialize the maze."""
        from Maze.algo.Dfs import DFS
        self.__width = config.width
        self.__height = config.height
        self.__entry = config.entry
        self.__exit = config.exit

        self.__cell_size = GameState.get_cell_size()
        self.__wall_thickness = GameState.get_wall_thickness()
        self.__gap = GameState.get_gap()

        self.__wall_tex: Optional[
            Union[tuple[int, int, int], pygame.Surface]] = wall_tex
        self.__exit_tex: Optional[
            Union[tuple[int, int, int], pygame.Surface]] = exit_tex
        self.__sol_tex: Optional[
            Union[tuple[int, int, int], pygame.Surface]] = sol_tex
        self.__is_maze_generated = False
        self.__maze_lst = self.__empty_maze()
        self.__set_42_logo()
        self.__dfs = DFS(self, seed)

        self.__soluce: list[Cell] = []
        self.__display_soluce = False
        if wall_tex and exit_tex and sol_tex:
            self.set_textures(wall_tex, exit_tex, sol_tex)

    def __empty_maze(self) -> list[list[Cell]]:
        """Return a closed grid of cells."""
        maze = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                row.append(Cell(x, y, self.__wall_tex,))
            maze.append(row)
        return maze

    def generate_anim(self) -> bool:
        """Run one animated generation step."""
        if self.__is_maze_generated:
            return True

        instruct = self.__dfs.get_instruct()
        if instruct:
            print(instruct._cell.pos)
            setattr(instruct._cell, instruct._wall, False)
            setattr(instruct._neigh, instruct._neigh_wall, False)
            if self.__wall_tex and self.__sol_tex and self.__exit_tex:
                instruct._cell.set_render_cell()
                instruct._neigh.set_render_cell()
            return False

        self.__is_maze_generated = True
        return True

    def render(self, screen: pygame.Surface) -> None:
        """Render the maze."""
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

    def get_cell(self, coord: tuple[int, int]) -> Optional[Cell]:
        """Return the cell at a coordinate."""
        x, y = coord
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__maze_lst[y][x]
        return None

    def set_textures(self,
                     wall: Union[tuple[int, int, int], pygame.Surface],
                     exit: Union[tuple[int, int, int], pygame.Surface],
                     soluce: Union[tuple[int, int, int], pygame.Surface]
                     ) -> None:
        """Set maze cell textures."""
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
        """Update maze textures."""
        self.set_textures(wall, exit, soluce)

    def solve(self) -> None:
        """Compute the solution path."""
        from Maze.algo.AStar import A_Star
        astar = A_Star(self)
        self.__soluce = astar.solve()
        for cell in self.__soluce:
            cell.display_soluce = self.__display_soluce
        if self.__sol_tex and self.__exit_tex and self.__wall_tex:
            self.set_textures(self.__wall_tex, self.__exit_tex, self.__sol_tex)

    def add_to_soluce(self, cell: Cell) -> None:
        """Add a cell to the solution path."""
        if self.get_cell(cell.pos):
            self.__soluce.append(cell)

    def reset(self) -> None:
        """Reset the maze state."""
        self.__is_maze_generated = False
        self.__maze_lst = self.__empty_maze()
        self.__set_42_logo()
        self.__soluce = []

    def __set_42_logo(self) -> None:
        """Mark cells forming the 42 pattern."""
        starting_cell = self.get_cell((
            (self.__width - 7) // 2,
            (self.__height - 5) // 2
        ))
        if not starting_cell:
            return

        starting_cell.is42 = True
        cell: Optional[Cell] = starting_cell
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
        self.check_entry_exit_in_42()

    def check_entry_exit_in_42(self):
        for row in self.__maze_lst:
            for cell in row:
                if cell.is42 and (cell == self.entry or cell == self.exit):
                    raise MazeError('Entry or Exit set in 42 Logo')

    def set_display_soluce(self, value: Optional[bool] = None) -> None:
        """Set or toggle solution display."""
        if value is None:
            self.__display_soluce = not self.__display_soluce
        else:
            self.__display_soluce = value
        for cell in self.__soluce:
            cell.display_soluce = self.__display_soluce

    def get_display_soluce(self) -> bool:
        return self.__display_soluce

    def unperfect(self) -> None:
        """Open extra walls to make the maze imperfect."""
        import random
        neigh_map = {
            'n': ('s', 0, -1),
            's': ('n', 0, +1),
            'e': ('w', +1, 0),
            'w': ('e', -1, 0)
        }

        end_points: list[Cell] = []
        for y in self.__maze_lst:
            for cell in y:
                if (sum([getattr(cell, w) for w in "nsew"]) >= 3 and
                        not cell.is42):
                    end_points.append(cell)
        print(f"Walls to break: {len(end_points)}")

        for cell in end_points:
            walls_present = [w for w in "nsew" if getattr(cell, w)]
            wall = random.choice(walls_present)

            neigh_wall, dx, dy = neigh_map[wall]
            neigh = self.get_cell((cell.x + dx, cell.y + dy))

            if neigh and not neigh.is42:
                setattr(cell, wall, False)
                setattr(neigh, neigh_wall, False)

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
    def cell_size(self) -> tuple[int, int]:
        return self.__cell_size

    @property
    def maze_lst(self) -> list[list[Cell]]:
        return self.__maze_lst

    @property
    def soluce(self) -> list[Cell]:
        return self.__soluce

    @property
    def wall_thickness(self) -> int:
        return self.__wall_thickness

    @property
    def gap(self) -> tuple[int, int]:
        return self.__gap

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.__color = value

    @property
    def display_soluce(self) -> bool:
        return self.__display_soluce

    @property
    def is_maze_generated(self) -> bool:
        return self.__is_maze_generated

    @is_maze_generated.setter
    def is_maze_generated(self, value: bool) -> None:
        self.__is_maze_generated = value
