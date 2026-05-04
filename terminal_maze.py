from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from render.terminal import render_maze
import os
import time

config = ParserConfig('settings.txt').init_config()
maze = Maze(config)
maze.solve()

while (True):
	if not maze.is_maze_generated:
		maze.generate_anim()
		maze.solve()
	ascii_maze = render_maze(maze, maze.entry, maze.exit, maze.soluce)
	os.system('clear')
	print(ascii_maze)
	time.sleep(0.1)