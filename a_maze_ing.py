import config_parsing
import maze_config


class Maze:
    config: maze_config.MazeConfig

    def load_config(self) -> dict[str, str | None]:
        cfg = config_parsing.MazeConfigParser.default_parser()
        print(cfg)
        return cfg
        # self.config = maze_config.MazeConfig(**cfg)


if __name__ == "__main__":
    maze = Maze()
    cfg = maze.load_config()
    for k, v in cfg.items():
        print(k, v)
