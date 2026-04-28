"""Output module."""


from Maze.Maze import Maze
# from maze.Cell import Cell


class Output:
    """Output class for maze."""

    def __init__(self, maze: Maze) -> None:
        """Initialize an Output class instance.

        Args:
            maze (Maze): Current maze to write

        Example:
            >>> astar = A_Star(maze)
        """
        self.__maze = maze

    def write(self) -> None:
        """Write maze's output.

        Example:
            >>> astar = A_Star(maze)
        """
        with open('output.txt', 'w') as f:

            f.write(self.__get_hexa_maze())
            f.write("\n\n")
            f.write(f"{self.__maze.entry.pos}")
            f.write("\n")
            f.write(f"{self.__maze.exit.pos}")
            f.write("\n")
            f.write(self.__get_soluce_as_str())

    def __get_soluce_as_str(self) -> str:
        """Get soluce path as str.

        Returns:
            str: Soluce path

        Example:
            >>> maze.get_soluce_as_str()
            "WSSENW..."
        """
        final_str = ''
        soluce = self.__maze.soluce
        if self.__maze.exit not in soluce:
            soluce.append(self.__maze.exit)

        for i, cell in enumerate(soluce):
            if i < len(soluce) - 1:
                if soluce[i + 1].x == cell.x + 1:
                    final_str += 'E'
                elif soluce[i + 1].x == cell.x - 1:
                    final_str += 'W'
                elif soluce[i + 1].y == cell.y - 1:
                    final_str += 'N'
                elif soluce[i + 1].y == cell.y + 1:
                    final_str += 'S'
        return final_str

    def __get_hexa_maze(self) -> str:
        final_str = ''
        for y in self.__maze.maze_lst:
            for cell in y:
                value = 0
                value += cell.n * 1
                value += cell.e * 2
                value += cell.s * 4
                value += cell.w * 8
                final_str += hex(value).replace('0x', '').capitalize()
            final_str += '\n'
        return final_str
