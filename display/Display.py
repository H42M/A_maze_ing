"""Display class management."""


from maze import Maze


class Display:
    """Manage the maze display."""

    @classmethod
    def print_maze(cls, maze_obj: Maze):
        """Print current maze.

        Example:
            >>> maze.print_maze()
        """
        maze = maze_obj.maze_list
        FOND_VERT = "\033[42m"
        FOND_ROUGE = "\033[41m"
        FOND_BLEU = "\033[44m"
        RESET = "\033[0m"

        for y, col in enumerate(maze):
            for x, cell in enumerate(col):
                if cell.n:
                    print("████", end="")
                else:
                    print(FOND_BLEU + "    " + RESET, end="")
            print()
            for x, cell in enumerate(col):
                if cell.w:
                    print("█", end="")
                else:
                    print(" ", end="")
                if x == maze_obj.entry[0] and y == maze_obj.entry[1]:
                    color = FOND_ROUGE
                elif x == maze_obj.exit[0] and y == maze_obj.exit[1]:
                    color = FOND_VERT
                elif maze_obj.get_cell(x, y).visited:
                    color = FOND_BLEU
                else:
                    color = RESET
                print(color + "  " + RESET, end="")
                if cell.e:
                    print("█", end="")
                else:
                    print(" ", end="")
            print()
            for x, cell in enumerate(col):
                if cell.s:
                    print("████", end="")
                else:
                    print(FOND_BLEU + "    " + RESET, end="")
            print()

    @classmethod
    def print_maze_2(cls, maze_obj: Maze):
        """Print current maze.

        Example:
            >>> maze.print_maze()
        """
        maze = maze_obj.maze_list
        FOND_VERT = "\033[42m"
        FOND_ROUGE = "\033[41m"
        RESET = "\033[0m"

        for y, col in enumerate(maze):
            for x, cell in enumerate(col):
                if cell.n:
                    print("┏━━┓", end="")
            print()
            for x, cell in enumerate(col):
                if cell.w:
                    print("┃", end="")
                if x == maze_obj.entry[0] and y == maze_obj.entry[1]:
                    color = FOND_ROUGE
                elif x == maze_obj.exit[0] and y == maze_obj.exit[1]:
                    color = FOND_VERT
                else:
                    color = RESET
                print(color + "  " + RESET, end="")
                if cell.e:
                    print("┃", end="")
            print()
            for x, cell in enumerate(col):
                if cell.s:
                    print("┗━━┛", end="")
            print()
