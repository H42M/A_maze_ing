from Maze.Maze import Maze


class Output:
    """Export maze data to a file."""

    def __init__(self, maze: Maze) -> None:
        """Initialize the exporter."""
        self.__maze = maze

    def write(self) -> None:
        """Write the maze output file."""
        with open('output.txt', 'w') as f:

            f.write(self.__get_hexa_maze())
            f.write("\n")
            f.write(f"{self.__maze.entry.pos}")
            f.write("\n")
            f.write(f"{self.__maze.exit.pos}")
            f.write("\n")
            f.write(self.__get_soluce_as_str())
            f.write("\n")

    def __get_soluce_as_str(self) -> str:
        """Return the solution as directions."""
        final_str = ''
        soluce = self.__maze.soluce

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
        """Return the maze as hexadecimal rows."""
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