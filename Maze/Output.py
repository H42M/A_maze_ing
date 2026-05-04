"""Maze output export module.

Provides functionality to export maze data to a text file in hexadecimal
format with entry, exit, and solution path information.
"""

from Maze.Maze import Maze


class Output:
    """Export maze to output file.

    Handles exporting maze structure, entry/exit points, and solution
    path to a text file in hexadecimal format.

    Attributes:
        _Output__maze (Maze): The maze instance to export.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize output exporter for a maze.

        Args:
            maze (Maze): The maze instance to export.
        """
        self.__maze = maze

    def write(self) -> None:
        """Write maze data to output file.

        Exports maze structure as hexadecimal, entry/exit coordinates,
        and solution path to 'output.txt'.
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
        """Convert solution path to direction string.

        Converts the list of cells in the solution path to a string of
        direction characters (N/S/E/W for North/South/East/West).

        Returns:
            str: Direction string representing solution path (e.g., 'WSSENW').
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
        """Convert maze structure to hexadecimal representation.

        Each cell is converted to a hex digit (0-F) where bits represent
        wall states (N, E, S, W).

        Returns:
            str: Maze in hexadecimal format with newlines for each row.
        """
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
