from render.RenderObj import RenderObj
from typing import Union
from Config.GameState import GameState
import os
import pygame


class Bloc(RenderObj):

    image: pygame.Surface

    def __init__(self, pos: tuple[int, int],
                 color: Union[tuple[int, int, int], str]
                 ):
        super().__init__(pos=pos, size=GameState.bloc_size)
        self.__is_image = False
        self.__get_color(color)

    def render(self, screen):
        if self.__is_image:
            pos_tuple = (int(self._pos.x), int(self._pos.y))
            screen.blit(self._surface, pos_tuple)
        else:
            super().render(screen)

    def __get_color(self, color):
        from random import randint

        if isinstance(color, str) and os.path.isfile(color):
            try:
                if not self.image:
                    self.load_image(color)
                image = pygame.transform.scale(self.image, self._size)
                self._surface = image
                self._color = (255, 255, 255)
                self.__is_image = True
                return
            except Exception as e:
                print(f"Error loading image: {e}", flush=True)

        # Sinon, traiter comme couleur
        self.__is_image = False
        if color == 'random':
            self._color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self._surface.fill(self._color)
        elif isinstance(color, tuple):
            self._color = color
            self._surface.fill(self._color)
        else:
            self._color = (255, 255, 0)
            self._surface.fill(self._color)

    @classmethod
    def load_image(cls, path: str):
        if os.path.isfile(path):
            try:
                cls.image = pygame.image.load(path)
                return
            except Exception as e:
                print(f"Error loading image: {e}", flush=True)
