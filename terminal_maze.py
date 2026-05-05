"""Run termnal maze."""

from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from render.terminal import render_maze
from Maze.Output import Output
import os
from typing import Optional
import time

def generate_maze(seed: Optional[int] = None, solve: bool = True,
                  animate = 0.05
                  ) -> None:
    """Generate complete ascii maze"""
    config = ParserConfig('settings.txt').init_config()
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
            if solve:
                maze.solve()
                print('Maze Solved')
                input('Wait!')
        ascii_maze = render_maze(maze, maze.entry, maze.exit, maze.soluce)

        os.system('clear')
        print(ascii_maze)
        time.sleep(animate)
        if maze_over:
            output = Output(maze)
            output.write()
            input('Press Enter to return to the menu')
            break
