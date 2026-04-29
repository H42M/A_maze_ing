"""Game theme manager module.

Provides a singleton class for managing game themes, including loading
theme configurations, managing textures, and notifying observers when
themes change.
"""

import pygame
import json
import os
from typing import Optional, Callable
from Errors import ConfigError


class ThemeManager:
    """Singleton class for managing game themes.

    Handles loading theme configurations from JSON files, loading and
    caching textures, switching themes, and notifying observers about
    theme changes through a callback system.

    Attributes:
        themes (dict): Loaded theme configurations.
        current_theme_name (str): Name of currently active theme.
        current_theme_data (dict): Data of currently active theme.
        initialized (bool): Whether this instance was initialized.
    """

    _instance = None
    _observers = []

    def __new__(cls):
        """Create or return the unique instance of ThemeManager (Singleton).

        Returns:
            ThemeManager: The unique instance of the class.
        """
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the ThemeManager on its first instantiation.

        Attributes:
            themes (dict): Dictionary of available themes.
            current_theme_name (str | None): Name of the currently
            active theme.
            current_theme_data (Any | None): Data of the currently
            active theme.
            initialized (bool): Flag indicating whether initialization
            has already been performed.
        """
        if not hasattr(self, 'initialized'):
            self.themes = {}
            self.current_theme_name = None
            self.current_theme_data = None
            self.initialized = True

    def load_themes_config(
            self,
            config_path: str = 'Config/themes.json') -> None:
        """Load theme configurations from a JSON file.

        Args:
            config_path (str): Path to the theme configuration JSON file.
                Defaults to 'Config/themes.json'.

        Raises:
            ConfigError: If file not found or JSON parsing fails.
        """
        try:
            with open(config_path, 'r') as f:
                self.themes = json.load(f)
            print(f"Themes charges: {list(self.themes.keys())}",
                  flush=True)
        except FileNotFoundError:
            raise ConfigError(
                f"Fichier de configuration Themes "
                f"non trouve: {config_path}")
        except json.JSONDecodeError:
            raise ConfigError(
                f"Erreur de parsing JSON: {config_path}")

    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme and notify all observers.

        Loads textures for the specified theme, sets it as active,
        and calls all registered observer callbacks.

        Args:
            theme_name (str): Name of the theme to activate.

        Returns:
            bool: True if theme was successfully set, False otherwise.
        """
        if theme_name not in self.themes:
            print(f"Theme '{theme_name}' non trouve", flush=True)
            return False

        if not self._load_theme_textures(theme_name):
            print(f"Theme '{theme_name}' n'a pas pu etre charge", flush=True)
            return False

        self.current_theme_name = theme_name
        self.current_theme_data = self.themes[theme_name]

        self._notify_observers(theme_name)

        print(f"Theme change: {theme_name}", flush=True)
        return True

    def _load_theme_textures(self, theme_name: str) -> bool:
        """Load all textures for a specific theme.

        Args:
            theme_name (str): Name of the theme to load textures for.

        Returns:
            bool: True if all textures loaded successfully, False otherwise.
        """
        theme = self.themes[theme_name]
        textures = {}

        for texture_key, texture_path in theme.get('assets', {}).items():
            if os.path.isfile(texture_path):
                try:
                    textures[texture_key] = pygame.image.load(texture_path)
                except Exception as e:
                    print(f"Erreur chargement {texture_key}: {e}")
                    return False
            else:
                print(f"Fichier non trouve: {texture_path}")
                return False

        self.themes[theme_name]['loaded_assets'] = textures
        return True

    def get_texture(self, texture_name: str) -> Optional[pygame.Surface]:
        """Get a single texture from the current theme.

        Args:
            texture_name (str): Name of the texture to retrieve.

        Returns:
            Optional[pygame.Surface]: The texture surface or None if not found.
        """
        if not self.current_theme_data:
            return None
        return self.current_theme_data.get(
            'loaded_assets', {}).get(texture_name)

    def get_all_textures(self) -> dict[str, pygame.Surface]:
        """Get all textures from the current theme.

        Returns:
            dict[str, pygame.Surface]: Dictionary mapping texture names
                to pygame.Surface objects.
        """
        if not self.current_theme_data:
            print('No texture to return')
            return {}
        return self.current_theme_data.get('loaded_assets', {})

    def get_theme_config(self, key: str, default=None):
        """Get a configuration value from the current theme.

        Args:
            key (str): Configuration key to retrieve.
            default: Default value if key not found.

        Returns:
            The configuration value or default if not found.
        """
        if not self.current_theme_data:
            return default
        return self.current_theme_data.get(
            'config', {}).get(key, default)

    def get_available_themes(self) -> list[str]:
        """Get list of all available themes.

        Returns:
            list[str]: List of theme names.
        """
        return list(self.themes.keys())

    def register_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """Register a callback to be notified on theme changes.

        Args:
            callback (Callable[[str], None]): Function to call with
                theme_name when theme changes.
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def unregister_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """Unregister an observer callback.

        Args:
            callback (Callable[[str], None]): The callback to remove.
        """
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, theme_name: str) -> None:
        """Notify all registered observers of a theme change.

        Args:
            theme_name (str): Name of the new active theme.
        """
        for callback in self._observers:
            try:
                callback(theme_name)
            except Exception as e:
                print(f"✗ Erreur notification observateur: {e}",
                      flush=True)
