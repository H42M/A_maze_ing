"""Generate a Maze an resolve it."""

from config.Config import Config
from display.Display import Display
from maze.Maze import Maze
from Errors import ConfigError
from Logs import Log
from maze.Output import Output

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
        maze.generate_maze()
        Display.print_maze(maze)
        output = Output(maze)
        choice = 0
        soluce = False
        while (choice != 4):
            print("=== A-Maze-Ing ===")
            print("1. Re-generate a new maze")
            print("2. Show / Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            try:
                choice = int(input("Choice ? (1-4): "))
                if choice > 4 or choice < 1:
                    raise ValueError

                if choice == 1:
                    maze.reset()
                    maze.generate_maze()
                    maze.resolve_a_star()
                    Display.print_maze(maze, print_soluce=soluce)

                if choice == 2:
                    if soluce:
                        soluce = False
                    else:
                        soluce = True
                    Display.print_maze(maze, print_soluce=soluce)

            except Exception:
                print("Invalid input, must be a valid int between 1 and 4")

        output.write()
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
