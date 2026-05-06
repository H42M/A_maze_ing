from terminal_maze import generate_maze
from pygame_maze import pygame_maze
import os
from typing import Optional
import sys
import os.path


class Option_menu:
    """Class menu option."""

    def __init__(self, str_to_display: str, val: int,
                 options: Optional[list[str]] = None) -> None:
        """Init Option_menu instance."""
        self.__str = str_to_display
        self.__val = val
        self.__options = options
        self.__display_str = ""
        self.__current_option = 0

    def switch_option(self) -> None:
        """Switch for next option."""
        if self.__options:
            self.__current_option += 1
            if self.__current_option > len(self.__options) - 1:
                self.__current_option = 0

    def __set_display_str(self) -> None:
        """Set display_str depending selected option."""
        if '%' in self.__str and self.__options:
            str_val = self.__options[self.__current_option]
            self.__display_str = self.__str.replace('%', str_val)
        else:
            self.__display_str = self.__str

    @property
    def val(self) -> int:
        return self.__val

    @val.setter
    def val(self, value: int) -> None:
        self.__val = value

    @property
    def display_str(self) -> str:
        self.__set_display_str()
        return self.__display_str

    @property
    def current_option(self) -> int:
        return self.__current_option


def select_menu(options: list[Option_menu],
                status_message: str = "") -> int:
    """Print menu selection and return user input."""
    local_error = ""

    while True:
        os.system('clear')
        print("=== A-Maze-Ing ===")

        for i, opt in enumerate(options):
            print(f"{i}. {opt.display_str}")

        message = local_error or status_message
        message = message.strip()

        if message:
            print()
            print(message)
            print()

        try:
            choice = int(input(f'Choose (0-{len(options) - 1}): '))
            if choice < 0 or choice > len(options):
                raise ValueError()
            return choice
        except ValueError:
            local_error = "Invalid choice provided!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Error: Only one parameter expected')
        print("  ex: python a_maze_ing.py config.txt")
        exit()
    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"Error: {config_path} doesn't exist")
        exit()

    colors = {
        0: ["WHITE", "\033[37m"],
        1: ["YELLOW", "\033[33m"],
        2: ["GREEN", "\033[32m"],
        3: ["BLUE", "\033[34m"],
        4: ["RED", "\033[31m"],
    }
    options = [
        Option_menu('Re-generate a new random maze', 0),
        Option_menu('Re-Generate a new maze with seed', 1),
        Option_menu('% path from entry to exit', 2, ["Hide", "Show"]),
        Option_menu('% animation', 3, ['Disable', 'Toggle']),
        Option_menu('Rotate maze colors (Current color: %)', 4,
                    [color[0] for color in colors.values()]),
        Option_menu('Open with pygame', 5),
        Option_menu('Quit', 6),
    ]
    opt = 0
    solve = True
    animate = 0.05
    selected_color = colors[0][1]
    status_message = ""

    while (opt != len(options) - 1):
        opt = select_menu(options, status_message)
        status_message = ""
        if opt == 0:
            try:
                status_message = generate_maze(config_path,
                                               display_solve=solve,
                                               animate=animate,
                                               color=selected_color)
            except Exception as e:
                status_message = f"Error: {e}"

        elif opt == 1:
            seed = input('Enter valid seed (ex: 3242): ')
            if seed.isdigit():
                try:
                    generate_maze(config_path, int(seed), display_solve=solve,
                                  animate=animate, color=selected_color)
                except Exception as e:
                    status_message = f"Error: {e}"
            else:
                status_message = "Invalid seed provided."

        elif opt == 2:
            options[2].switch_option()
            solve = not solve

        elif opt == 3:
            options[3].switch_option()
            if options[3].current_option == 0:
                try:
                    animate = float(input('Enter animation '
                                          'speed (ex: 0.05): '))
                    if animate < 0:
                        animate = 0.0
                    if animate > 1:
                        animate = 1.0
                except Exception:
                    animate = 0.05
                    status_message = "Animation speed must be a valid float. Reset to 0.05."
            else:
                animate = 0.0

        elif opt == 4:
            options[4].switch_option()
            selected_color = colors[options[4].current_option][1]

        if opt == 5:
            try:
                pygame_maze(config_path)
            except Exception as e:
                status_message = f"Pygame error: {e}"
