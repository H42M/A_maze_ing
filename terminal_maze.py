from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from Config.Config import Config
from render.terminal import render_maze
from Maze.Output import Output
import os
from typing import Optional
import time
from random import randint


def generate_maze(config: Config,
                  seed: Optional[int] = None,
                  display_solve: bool = True,
                  animate: float = 0.05, color: str = "\033[37m"
                  ) -> str:
    """Generate complete ascii maze."""
    PATH_COLOR = "\033[36m"
    RESET = "\033[0m"

    if not seed:
        seed = randint(500, 10000)

    maze = Maze(config, seed=seed)
    maze.solve()

    maze_over = False
    while (True):
        if not maze.is_maze_generated and not maze_over:
            maze.generate_anim()
        elif maze.is_maze_generated and not maze_over:
            maze_over = True
            if not config.perfect:
                maze.unperfect()
            maze.solve()

        if display_solve:
            soluce = maze.soluce
        else:
            soluce = []
        ascii_maze = render_maze(maze, maze.entry, maze.exit, soluce,
                                 wall_color=color, path_color=PATH_COLOR,
                                 reset_color=RESET)

        os.system('clear')
        print(ascii_maze)
        print(f'Seed: {seed}')
        if maze.warnings:
            print()
            print("\n".join(maze.warnings))
        time.sleep(animate)
        if maze_over:
            output = Output(maze)
            output.write(config.output_file)
            input('Press Enter to return to the menu')
            return "\n".join(maze.warnings)
