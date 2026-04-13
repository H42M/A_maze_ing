from config_parsing import MazeConfigLoader
from maze_config import MazeConfig


class Maze:
    config: MazeConfig

    def load_config(self) -> None:
        try:
            loader = MazeConfigLoader("config.txt")
        except FileNotFoundError:
            loader = MazeConfigLoader("default_config.txt")
        self.config = loader.load()


if __name__ == "__main__":
    maze = Maze()
    maze.load_config()
    print(maze.config)
