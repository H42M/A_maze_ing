from config_parsing import MazeConfigLoader
from maze_config import MazeConfig
from maze_generator import MazeGenerator
from maze_terminal import render_maze


class Maze:
    config: MazeConfig
    generator: MazeGenerator

    def load_config(self) -> None:
        try:
            self.config = MazeConfigLoader("config.txt").load()
        except FileNotFoundError:
            print("config file not found")
            print("Generating maze with default values...\n")
            self.config = MazeConfigLoader("default_config.txt").load()

    def load_generator(self) -> None:
        self.generator = MazeGenerator(self.config)


if __name__ == "__main__":
    maze = Maze()
    maze.load_config()
    print(maze.config)

    maze.load_generator()
    maze.generator.remove_wall(3, 3, 4, 3)
    maze.generator.remove_wall(3, 3, 3, 4)
    print(render_maze(maze.generator.grid, maze.config.entry,
                      maze.config.exit))
