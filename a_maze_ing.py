"""Generate a Maze an resolve it."""

from config.Config import Config
from display.Display import Display
from maze.Maze import Maze
from algo.Dfs import Dfs
from Errors import ConfigError
from Logs import Log

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Configuration file must be provided in arguments\n"
              "Usage: python3 a_maze_ing.py <conf_file>")
        exit(-1)
    conf_file = sys.argv[1]

    logs = Log(verbose=True)
    config = Config(logs=logs)
    try:
        config.parse_config_file(conf_file)

        maze = Maze(logs, config)
        mid_cell = maze.get_cell(
            int((config.width - 7) / 2),
            int((config.height - 5) / 2),
        )
        if mid_cell:
            maze.generate_42(mid_cell)
        Display.print_maze(maze)
        dfs = Dfs(logs)
        dfs.build(maze)
        config.print_config()

    except ConfigError as e:
        print(e)


"""Exemple de Docstring a implementer dans tout le code selon le Google Style.

    Args:
        weight_kg (float): Le poids de la personne en kilogrammes.
        height_m (float): La taille de la personne en mètres.

    Returns:
        float: L'IMC calculé, arrondi à deux décimales.

    Raises:
        ValueError: Si le poids ou la taille sont négatifs ou nuls.

    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
