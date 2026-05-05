from terminal_maze import generate_maze
from pygame_maze import pygame_maze
import os
from typing import Optional


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


def select_menu(options: list[Option_menu]) -> int:
    """Print menu selection and return user input."""
    os.system('clear')
    print("=== A-Maze-Ing ===")
    [print(f"{i}. {opt.display_str}") for i, opt in enumerate(options)]
    while (True):
        try:
            choice = int(input(f'Choose (0-{len(options) - 1}): '))
            if choice < 0 or choice > len(options):
                raise ValueError()
            return choice
        except Exception:
            print('Invalid choice provided !')


if __name__ == "__main__":
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
        Option_menu('% path from entry to exit', 2, ['Show', 'Hide']),
        Option_menu('% animation', 3, ['Disable', 'Toggle']),
        Option_menu('Rotate maze colors (Current color: %)', 4, [color[0] for color in colors.values()]),
        Option_menu('Open with pygame', 5),
        Option_menu('Quit', 6),
    ]
    opt = 0
    solve = False
    animate = 0.05
    selected_color = colors[0][1]

    while (opt != len(options) - 1):
        opt = select_menu(options)
        if opt == 0:
            try:
                generate_maze(display_solve=solve, animate=animate, color=selected_color)
            except Exception as e:
                print(f'Error: {e}')
                input('Press Enter to continue')

        if opt == 1:
            seed = input('Enter valid seed (ex: 3242): ')
            if seed.isdigit():
                try:
                    generate_maze(int(seed), display_solve=solve, animate=animate, color=selected_color)
                except Exception as e:
                    print(f'Error: {e}')
                    print('Press Enter to continue')
            else:
                print('Invalid Seed provided')
                input('Press Enter to return to the menu')

        if opt == 2:
            options[2].switch_option()
            solve = not solve

        if opt == 3:
            options[3].switch_option()
            if options[3].current_option == 0:
                try:
                    animate = float(input('Enter animation '
                                          'speed (ex: 0.05): '))
                except Exception:
                    print('Animation speed must be valid float (ex: 0.01)')
                    animate = 0.05
            else:
                animate = 0.0
        
        if opt == 4:
            options[4].switch_option()
            selected_color = colors[options[4].current_option][1]

        if opt == 5:
            pygame_maze()
