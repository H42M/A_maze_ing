from terminal_maze import generate_maze
from pygame_maze import pygame_maze
import os
from typing import Optional

class Option_menu:
    def __init__(self, str_to_display: str, val: int,
                 options: Optional[list[str]] = None) -> None:
        self.__str = str_to_display
        self.__val = val
        self.__options = options
        self.__display_str = ""
        self.__current_option = 0

    def switch_option(self):
        if self.__options:
            self.__current_option += 1
            if self.__current_option > len(self.__options) - 1:
                self.__current_option = 0
    
    def __set_display_str(self):
        if '%' in self.__str and self.__options:
            str_val = self.__options[self.__current_option]
            self.__display_str = self.__str.replace('%', str_val)
        else:
            self.__display_str = self.__str

    @property
    def val(self):
        return self.__val

    @val.setter
    def _val(self, value):
        self.__val = value

    @property
    def display_str(self):
        self.__set_display_str()
        return self.__display_str

    @property
    def _current_option(self):
        return self.__current_option


def select_menu(options: list[Option_menu]) -> int:
    os.system('clear')
    print("=== A-Maze-Ing ===")
    [print(f"{i}. {opt.display_str}") for i, opt in enumerate(options)]
    while(True):
        try:
            choice = int(input(f'Choose (0-{len(options) - 1}): '))
            if choice < 0 or choice > len(options):
                raise ValueError()
            return choice
        except:
            print(f'Invalid choice provided !')
    
if __name__ == "__main__":
    options = [
        Option_menu('Re-generate a new random maze', 0),
        Option_menu('Re-Generate a new maze with seed', 1),
        Option_menu('% path from entry to exit', 2, ['Show', 'Hide']),
        Option_menu('animation', 3, ['Show' 'Hide']),
        Option_menu('Rotate maze colors', 4),
        Option_menu('Open with pygame', 5),
        Option_menu('Quit', 6),
    ]
    opt = 0
    while (opt != len(options) - 1):
        opt = select_menu(options)
        if opt == 0:
            generate_maze()
        if opt == 1:
            seed = input('Enter valid seed (ex: 3242): ')
            if seed.isdigit():
                generate_maze(int(seed))
            else:
                print('Invalid Seed provided')
                input('Press Enter to return to the menu')
        if opt == 5:
            pygame_maze()



    
