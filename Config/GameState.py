"""
Stockage des données calculées une fois au démarrage
et accessibles partout dans le programme
"""

from Config.Config import Config
import pygame
from typing import Union


class GameState:
    """Singleton pour stocker les données globales du jeu"""

    _instance = None

    cell_size: tuple[int, int] = (55, 65)
    cell_nb_bloc: int = 3
    bloc_size: tuple[int, int] = (0, 0)
    gap: tuple[int, int] = (0, 0)
    wall_thickness: int = 5

    wall_texture: pygame.Surface
    player_texture: pygame.Surface
    soluce_texture: pygame.Surface
    bg_texture: pygame.Surface
    exit_texture: pygame.Surface

    theme_manager = None

    @classmethod
    def initialize(cls, config: Config, screen_size: tuple[int, int],
                   cell_nb_bloc: int, wall_thickness: int = 5):
        """Initialiser les données une seule fois"""
        from Config.ThemeManager import ThemeManager

        cls.cell_size = cls.__process_cell_size(screen_size,
                                                cell_nb_bloc,
                                                config)
        cls.cell_nb_bloc = cell_nb_bloc
        cls.bloc_size = (cls.cell_size[0] // cell_nb_bloc,
                         cls.cell_size[1] // cell_nb_bloc)
        cls.gap = (cls.cell_size[0] * 2, cls.cell_size[1] * 2 + 80)
        cls.wall_thickness = wall_thickness
        cls.screen_size = screen_size

        # Initialiser ThemeManager
        cls.theme_manager = ThemeManager()
        cls.theme_manager.load_themes_config('Config/themes.json')

        print("GameState initialized:", flush=True)
        print(f"  Cell size: {cls.cell_size}", flush=True)
        print(f"  Bloc size: {cls.bloc_size}", flush=True)
        print(f"  Gap: {cls.gap}", flush=True)
        print(f"  Wall thickness: {cls.wall_thickness}", flush=True)

    @classmethod
    def __load_textures(cls, theme: str):
        """Charger les textures via ThemeManager"""
        if cls.theme_manager:
            textures = cls.theme_manager.get_all_textures()

            # Mapper les noms des textures
            wall = textures.get('wall')
            player = textures.get('player')
            checkpoint = textures.get('checkpoint')
            background = textures.get('background')
            exit_tex = textures.get('exit')

            if wall is not None:
                cls.wall_texture = wall
            if player is not None:
                cls.player_texture = player
            if checkpoint is not None:
                cls.soluce_texture = checkpoint
            if background is not None:
                cls.bg_texture = background
            if exit_tex is not None:
                cls.exit_texture = exit_tex

    @staticmethod
    def __process_cell_size(
            screen_size: tuple[int, int],
            cell_nb_bloc: int,
            config: Config) -> tuple[int, int]:
        cell_by_screen = (screen_size[0] // (config.width + 4),
                          screen_size[1] // (config.height + 4))

        return (round(cell_by_screen[0] / cell_nb_bloc) * cell_nb_bloc,
                round(cell_by_screen[1] / cell_nb_bloc) * cell_nb_bloc)

    @classmethod
    def set_theme(cls, theme: Union[str, int]) -> None:
        """Changer le thème via ThemeManager"""
        if cls.theme_manager is None:
            print("✗ ThemeManager not initialized", flush=True)
            return

        if isinstance(theme, int):
            themes = cls.theme_manager.get_available_themes()
            if 0 <= theme < len(themes):
                theme_name = themes[theme]
                cls.__load_textures(theme_name)
        else:
            cls.__load_textures(theme)

    @classmethod
    def get_themes(cls) -> list[str]:
        """Retourner la liste des thèmes disponibles"""
        if cls.theme_manager:
            return cls.theme_manager.get_available_themes()
        return []

    @classmethod
    def get_cell_size(cls) -> tuple[int, int]:
        """Obtenir la taille de chaque cellule"""
        return cls.cell_size

    @classmethod
    def get_bloc_size(cls) -> tuple[int, int]:
        """Obtenir la taille de chaque bloc"""
        return cls.bloc_size

    @classmethod
    def get_gap(cls) -> tuple[int, int]:
        """Obtenir l'espace de centrage du labyrinthe"""
        return cls.gap

    @classmethod
    def get_cell_nb_bloc(cls) -> int:
        """Obtenir le nombre de blocs par cellule"""
        return cls.cell_nb_bloc

    @classmethod
    def get_wall_thickness(cls) -> int:
        """Obtenir l'épaisseur des murs"""
        return cls.wall_thickness
