from maze.Maze import Maze
# from maze.Cell import Cell


class Output:
    """Output class for maze"""

    def __init__(self, maze: Maze) -> None:
        self.__maze = maze

    def write(self):
        with open('output.txt', 'w') as f:

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
