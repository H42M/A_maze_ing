from config_parsing import MazeConfigLoader
from maze_config import MazeConfig
from maze_generator import MazeGenerator
from maze_solver import solve_shortest_path
from maze_terminal import render_maze
import sys


class Maze:
    config: MazeConfig
    generator: MazeGenerator

    def load_config(self) -> None:
        try:
            self.config = MazeConfigLoader(sys.argv[1]).load()
        except IndexError:
            print("Incorrect number of arguments, please run \'make run\'"
                  " or \'python3 a_maze_ing.py config.txt\'")
            sys.exit(1)
        except FileNotFoundError:
            print("config file not found")
            print("Generating maze with default values...\n")
            self.config = MazeConfigLoader("default_config.txt").load()

    def load_generator(self) -> None:
        self.generator = MazeGenerator(self.config)


if __name__ == "__main__":
    maze = Maze()
    maze.load_config()

    maze.load_generator()
    maze.generator.generate_perfect()
    path = solve_shortest_path(maze.generator.grid,
                               maze.config.entry,
                               maze.config.exit)
    print(render_maze(maze.generator.grid, maze.config.entry,
                      maze.config.exit, path))
