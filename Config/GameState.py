"""
Stockage des données calculées une fois au démarrage
et accessibles partout dans le programme
"""

from Config.Config import Config
from Errors import ConfigError
import pygame


class GameState:
    """Singleton pour stocker les données globales du jeu"""

    _instance = None\


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

    @classmethod
    def initialize(cls, config: Config, screen_size: tuple[int, int],
                   cell_nb_bloc: int, wall_thickness: int = 5):
        """Initialiser les données une seule fois"""
        cls.cell_size = cls.__process_cell_size(screen_size,
                                                cell_nb_bloc,
                                                config)
        cls.cell_nb_bloc = cell_nb_bloc
        cls.bloc_size = (cls.cell_size[0] // cell_nb_bloc,
                         cls.cell_size[1] // cell_nb_bloc)
        cls.gap = (cls.cell_size[0] * 2, cls.cell_size[1] * 2 + 80)
        cls.wall_thickness = wall_thickness
        cls.screen_size = screen_size
        cls.__load_textures('MARIO')

        print("GameState initialized:", flush=True)
        print(f"  Cell size: {cls.cell_size}", flush=True)
        print(f"  Bloc size: {cls.bloc_size}", flush=True)
        print(f"  Gap: {cls.gap}", flush=True)
        print(f"  Wall thickness: {cls.wall_thickness}", flush=True)

    @classmethod
    def __load_textures(cls, theme: str):
        texture_path = {
            'wall_texture': '',
            'player_texture': '',
            'soluce_texture': '',
            'bg_texture': '',
            'exit_texture': ''
        }

        if theme.upper() == 'MARIO':
            path = 'srcs/mario'
            path_cloud = path + '/mario-cloud'
            texture_path['wall_texture'] = path_cloud + '/mario-cloud.png'
            texture_path['player_texture'] = path + '/mario.png'
            texture_path['soluce_texture'] = path + '/mario-coin.png'
            texture_path['bg_texture'] = path_cloud + '/mario-cloud-bg-1.png'
            texture_path['exit_texture'] = path + '/mario-flag-1.png'
        else:
            return

        import os
        for key, value in texture_path.items():
            if len(value) > 5 and os.path.isfile(value):
                try:
                    setattr(cls, key, pygame.image.load(value))
                except Exception as e:
                    print(f"Error loading image {value}: {e}", flush=True)
            else:
                raise ConfigError(f"Impossible to load texture: {value}")

    @staticmethod
    def __process_cell_size(screen_size: tuple[int, int],
                            cell_nb_bloc: int, config: Config):
        cell_by_screen = (screen_size[0] // (config.width + 4),
                          screen_size[1] // (config.height + 4))

        return (round(cell_by_screen[0] / cell_nb_bloc) * cell_nb_bloc,
                round(cell_by_screen[1] / cell_nb_bloc) * cell_nb_bloc)

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
