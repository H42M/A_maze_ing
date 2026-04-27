from render.RenderObj import RenderObj
import pygame
from typing import Callable, Optional, Union


class Button(RenderObj):
    def __init__(self, text: str,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 color: tuple[int, int, int] | None = None,
                 callback: Optional[Union[Callable, list[Callable]]] = None,
                 ) -> None:

        super().__init__(pos, size, color)
        self._text = text
        self._callback = callback
        self._is_hovered = False
        self._hover_color = None
        self._font = pygame.font.Font(None, 36)

    def render(self, screen: pygame.Surface):
        # Changer la couleur si survolée
        current_color = self._hover_color if self._is_hovered \
                                            else self._color
        if not current_color:
            current_color = (255, 255, 255)
        self._surface.fill(current_color)

        # Afficher le texte
        text_surface = self._font.render(self._text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self._size[0] // 2,
                                                  self._size[1] // 2))
        self._surface.blit(text_surface, text_rect)

        # Afficher le bouton
        pos_tuple = (int(self._pos.x), int(self._pos.y))
        screen.blit(self._surface, pos_tuple)

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Vérifier si le bouton est cliqué"""
        rect = pygame.Rect(int(self._pos.x), int(self._pos.y),
                           self._size[0], self._size[1])
        return rect.collidepoint(mouse_pos)

    def update_hover(self, mouse_pos: tuple[int, int]) -> None:
        """Mettre à jour l'état de survol"""
        rect = pygame.Rect(int(self._pos.x), int(self._pos.y),
                           self._size[0], self._size[1])
        self._is_hovered = rect.collidepoint(mouse_pos)

    def set_callback(self, callback: Callable) -> None:
        """Définir la fonction à exécuter au clic"""
        self._callback = callback

    def set_hover_color(self, color: tuple[int, int, int]) -> None:
        """Définir la couleur au survol"""
        self._hover_color = color

    def execute(self) -> None:
        """Exécuter le callback si défini"""
        if self._callback:
            if isinstance(self._callback, list):
                [callback() for callback in self._callback]
            else:
                self._callback()
            print(f'Button {self._text} callback executed')

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value


class ToggleButton(Button):
    def __init__(self, text: str,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 callback: Callable,
                 callback_state: Callable,
                 disable_color: tuple[int, int, int] | None = None,
                 enable_color: tuple[int, int, int] | None = None
                 ) -> None:
        super().__init__(text, pos, size, (0, 0, 0), callback)
        self.__callback_state = callback_state
        self.__disable_color = disable_color
        self.__enable_color = enable_color

        if not disable_color:
            self.__disable_color = (255, 0, 0)
        if not enable_color:
            self.__enable_color = (0, 255, 0)

    def render(self, screen: pygame.Surface):
        current_color = self.__enable_color if self.__callback_state() \
            else self.__disable_color
        current_color = (255, 255, 255) if self._is_hovered \
            else current_color
        if not current_color:
            current_color = (255, 255, 255)
        self._surface.fill(current_color)

        text_surface = self._font.render(self._text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self._size[0] // 2,
                                                  self._size[1] // 2))
        self._surface.blit(text_surface, text_rect)

        pos_tuple = (int(self._pos.x), int(self._pos.y))
        screen.blit(self._surface, pos_tuple)


class SelectButton(Button):
    def __init__(self, text: str,
                 pos: tuple[int, int],
                 size: tuple[int, int],
                 callback: Callable,
                 options: list[str]
                 ) -> None:
        super().__init__(text, pos, size, (0, 0, 255), callback)
        self.__options = options
        self.selected_opt: int = 0

    def render(self, screen: pygame.Surface):
        # Changer la couleur si survolée
        current_color = self._hover_color if self._is_hovered \
                                            else self._color
        if not current_color:
            current_color = (255, 255, 255)
        self._surface.fill(current_color)

        text_surface = self._font.render(self._text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self._size[0] // 2,
                                                  self._size[1] // 2))
        self._surface.blit(text_surface, text_rect)

        option_surface = self._font.render(self.__options[self.selected_opt],
                                           True, (0, 0, 0))
        option_rect = option_surface.get_rect(center=(self._size[0] // 2,
                                                      self._size[1] // 2))
        self._surface.blit(option_surface, option_rect)

        pos_tuple = (int(self._pos.x), int(self._pos.y))
        screen.blit(self._surface, pos_tuple)

    def execute(self) -> None:
        if self._callback and isinstance(self._callback, Callable):
            self.selected_opt += 1
            if self.selected_opt >= len(self.__options):
                self.selected_opt = 0

            self._callback(self.__options[self.selected_opt])
            print(self.__options[self.selected_opt])
