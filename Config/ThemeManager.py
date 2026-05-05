import pygame
import json
import os
from typing import Optional, Callable, Any
from Errors import ConfigError


class ThemeManager:
    """Manage game themes and textures."""

    _instance = None
    _observers: list[Callable[[str], None]] = []

    def __new__(cls) -> "ThemeManager":
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize theme storage once."""
        if not hasattr(self, 'initialized'):
            self.themes: dict[str, Any] = {}
            self.current_theme_name: Optional[str] = None
            self.current_theme_data = None
            self.initialized = True

    def load_themes_config(
            self,
            config_path: str = 'Config/themes.json') -> None:
        """Load theme configuration from JSON."""
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
        """Set the active theme."""
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
        """Load textures for a theme."""
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
        """Return a texture from the active theme."""
        if not self.current_theme_data:
            return None
        return self.current_theme_data.get(
            'loaded_assets', {}).get(texture_name)

    def get_all_textures(self) -> dict[str, pygame.Surface]:
        """Return all textures from the active theme."""
        if not self.current_theme_data:
            print('No texture to return')
            return {}
        return self.current_theme_data.get('loaded_assets', {})

    # def get_theme_config(self, key: str, default=None) -> dict:
    #     """Get a configuration value from the current theme.

    #     Args:
    #         key (str): Configuration key to retrieve.
    #         default: Default value if key not found.

    #     Returns:
    #         The configuration value or default if not found.
    #     """
    #     if not self.current_theme_data:
    #         return default
    #     return self.current_theme_data.get(
    #         'config', {}).get(key, default)

    def get_available_themes(self) -> list[str]:
        """Return available theme names."""
        return list(self.themes.keys())

    def register_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """Register a theme-change callback."""
        if callback not in self._observers:
            self._observers.append(callback)

    def unregister_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """Unregister a theme-change callback."""
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, theme_name: str) -> None:
        """Notify registered theme observers."""
        for callback in self._observers:
            try:
                callback(theme_name)
            except Exception as e:
                print(f"✗ Erreur notification observateur: {e}",
                      flush=True)
