"""Output module."""


from maze.Maze import Maze
# from maze.Cell import Cell


class Output:
    """Output class for maze."""

    def __init__(self, maze: Maze, output_file: str) -> None:
        """Initialize an Output class instance.

        Args:
            maze (Maze): Current maze to write

        Example:
            >>> astar = A_Star(maze)
        """
        self.__maze = maze
        self.__output_file = output_file

    def write(self) -> None:
        """Write maze's output.

        Example:
            >>> astar = A_Star(maze)
        """
        with open(self.__output_file, 'w') as f:

            f.write(self.__get_hexa_maze())
            f.write("\n\n")
            f.write(f"{self.__maze.entry.pos}")
            f.write("\n")
            f.write(f"{self.__maze.exit.pos}")
            f.write("\n")
            f.write(self.__maze.get_soluce_as_str())

    def __get_hexa_maze(self) -> str:
        final_str = ''
        for y in self.__maze.maze_list:
            for cell in y:
                value = 0
                value += cell.n * 1
                value += cell.e * 2
                value += cell.s * 4
                value += cell.w * 8
                final_str += hex(value).replace('0x', '').capitalize()
            final_str += '\n'
        return final_str
