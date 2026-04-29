"""GameState module for centralized game state management.

Provides a singleton class that stores and manages all global game
data calculated at startup, including cell sizes, textures, and theme
information.
"""

from Config.Config import Config
import pygame
from typing import Union


class GameState:
    """Singleton class for managing global game state.

    This class stores and provides access to all global game data
    including cell dimensions, textures, themes, and layout parameters.
    Data is calculated once during initialization and accessible
    throughout the entire program.

    Attributes:
        cell_size (tuple[int, int]): Size of each maze cell.
        cell_nb_bloc (int): Number of blocks per cell.
        bloc_size (tuple[int, int]): Size of each block.
        gap (tuple[int, int]): Centering offset for the maze.
        wall_thickness (int): Thickness of maze walls in pixels.
        wall_texture (pygame.Surface): Texture for maze walls.
        player_texture (pygame.Surface): Texture for the player.
        soluce_texture (pygame.Surface): Texture for solution path.
        bg_texture (pygame.Surface): Background texture.
        exit_texture (pygame.Surface): Texture for the exit.
        theme_manager: Manager instance for theme operations.
    """

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
        """Initialize game state data (called once at startup).

        Calculates and stores all global game data based on the provided
        configuration and screen size. This method should only be called once.

        Args:
            config (Config): Maze configuration object.
            screen_size (tuple[int, int]): Screen dimensions (width, height).
            cell_nb_bloc (int): Number of blocks per cell.
            wall_thickness (int): Thickness of maze walls in pixels.
                Defaults to 5.
        """
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
        """Load textures for the specified theme from ThemeManager.

        Args:
            theme (str): Name of the theme to load textures for.
        """
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
        """Calculate the optimal cell size based on screen and maze dimensions.

        Args:
            screen_size (tuple[int, int]): Screen dimensions (width, height).
            cell_nb_bloc (int): Number of blocks per cell.
            config (Config): Maze configuration object.

        Returns:
            tuple[int, int]: Calculated cell size (width, height).
        """
        cell_by_screen = (screen_size[0] // (config.width + 4),
                          screen_size[1] // (config.height + 4))

        return (round(cell_by_screen[0] / cell_nb_bloc) * cell_nb_bloc,
                round(cell_by_screen[1] / cell_nb_bloc) * cell_nb_bloc)

    @classmethod
    def set_theme(cls, theme: Union[str, int]) -> None:
        """Change the current theme and load its textures.

        Args:
            theme (Union[str, int]): Theme name or index to set.
                If int, uses the index in available themes list.
        """
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
        """Get the list of available themes.

        Returns:
            list[str]: List of available theme names.
        """
        if cls.theme_manager:
            return cls.theme_manager.get_available_themes()
        return []

    @classmethod
    def get_cell_size(cls) -> tuple[int, int]:
        """Get the size of each maze cell.

        Returns:
            tuple[int, int]: Cell size (width, height).
        """
        return cls.cell_size

    @classmethod
    def get_bloc_size(cls) -> tuple[int, int]:
        """Get the size of each block.

        Returns:
            tuple[int, int]: Block size (width, height).
        """
        return cls.bloc_size

    @classmethod
    def get_gap(cls) -> tuple[int, int]:
        """Get the centering offset for the maze.

        Returns:
            tuple[int, int]: Gap offset (x, y) in pixels.
        """
        return cls.gap

    @classmethod
    def get_cell_nb_bloc(cls) -> int:
        """Get the number of blocks per cell.

        Returns:
            int: Number of blocks per cell.
        """
        return cls.cell_nb_bloc

    @classmethod
    def get_wall_thickness(cls) -> int:
        """Get the thickness of maze walls.

        Returns:
            int: Wall thickness in pixels.
        """
        return cls.wall_thickness
