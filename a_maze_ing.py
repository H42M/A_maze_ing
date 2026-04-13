"""Generate a Maze an resolve it."""

from config.Config import Config
from display.Display import Display
from maze.Maze import Maze
from Errors import ConfigError
from maze.Output import Output

import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Configuration file must be provided in arguments\n"
              "Usage: python3 a_maze_ing.py <conf_file>")
        exit(-1)
    conf_file = sys.argv[1]

    config = Config()
    try:
        config.parse_config_file(conf_file)
        maze = Maze(config)
        output = Output(maze)
        maze.generate_maze()
        maze.resolve_a_star()
        Display.print_maze(maze)
        output.write()
        choice = 0
        soluce = False
        animation = False
        while (choice != 6):
            print("=== A-Maze-Ing ===")
            print("1. Re-generate a new random maze")
            print("2. Re-Generate a new maze with seed")
            print("3. Show / Hide path from entry to exit")
            print("4. Toggle / Disable animation")
            print("5. Rotate maze colors")
            print("6. Quit")
            try:
                choice = int(input("Choice ? (1-6): "))
                if choice > 4 or choice < 1:
                    raise ValueError

                if choice == 1 or choice == 2:
                    import random
                    if choice == 2:
                        while (True):
                            try:
                                seed = int(input("Enter a valid seed: "))
                                break
                            except Exception:
                                print("Invalid seed provided")
                    else:
                        seed = random.randint(1000, 1000000)
                    maze.reset()
                    maze.generate_maze(seed=seed, animate=animation)
                    resolve_anim = False
                    if animation and soluce:
                        resolve_anim = animation
                    maze.resolve_a_star(animate=resolve_anim)
                    Display.print_maze(maze, print_soluce=soluce)
                    output.write()

                if choice == 3:
                    if soluce:
                        soluce = False
                    else:
                        soluce = True
                    Display.print_maze(maze, print_soluce=soluce)

                if choice == 4:
                    while (True):
                        try:
                            animation = float(input("Enter animation speed "
                                                    "(0 = disable): "))
                            if animation > 0.2:
                                print("Animation speed too slow (min 0.2)")
                            break
                        except Exception:
                            print("Invalid animation speed")

            except Exception:
                print("Invalid input, must be a valid int between 1 and 6")

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
