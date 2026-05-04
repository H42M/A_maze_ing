from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from render.terminal import render_maze
from Maze.Output import Output
import os
import time

config = ParserConfig('settings.txt').init_config()
maze = Maze(config)
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
    ascii_maze = render_maze(maze, maze.entry, maze.exit, maze.soluce)

    os.system('clear')
    print(ascii_maze)
    time.sleep(0.05)
    if maze_over:
        output = Output(maze)
        output.write()
        break
