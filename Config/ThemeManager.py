"""
Gestionnaire centralise des Themes du jeu
Permet de charger, changer et mettre à jour les Themes facilement
"""

import pygame
import json
import os
from typing import Optional, Callable
from Errors import ConfigError


class ThemeManager:
    """Singleton pour gerer les Themes du jeu"""

    _instance = None
    _observers = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.themes = {}
            self.current_theme_name = None
            self.current_theme_data = None
            self.initialized = True

    def load_themes_config(
            self,
            config_path: str = 'Config/themes.json') -> None:
        """Charger la configuration des Themes depuis un JSON"""
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
        """
        Changer le Theme actuel et notifier les observateurs

        Args:
            theme_name: Nom du Theme à activer

        Returns:
            True si succes, False sinon
        """
        if theme_name not in self.themes:
            print(f"✗ Theme '{theme_name}' non trouve", flush=True)
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
        """Recuperer une texture du Theme actuel"""
        if not self.current_theme_data:
            return None
        return self.current_theme_data.get(
            'loaded_assets', {}).get(texture_name)

    def get_all_textures(self) -> dict:
        """Recuperer toutes les textures du Theme actuel"""
        if not self.current_theme_data:
            print('No texture to return')
            return {}
        return self.current_theme_data.get('loaded_assets', {})

    def get_theme_config(self, key: str, default=None):
        """Recuperer une configuration du Theme actuel"""
        if not self.current_theme_data:
            return default
        return self.current_theme_data.get(
            'config', {}).get(key, default)

    def get_available_themes(self) -> list[str]:
        """Lister tous les Themes disponibles"""
        return list(self.themes.keys())

    def register_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """
        Enregistrer un observateur pour être notifie

        Args:
            callback: Fonction à appeler avec (theme_name)
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def unregister_observer(
            self,
            callback: Callable[[str], None]) -> None:
        """Retirer un observateur"""
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, theme_name: str) -> None:
        """Notifier tous les observateurs du changement de Theme"""
        for callback in self._observers:
            try:
                callback(theme_name)
            except Exception as e:
                print(f"✗ Erreur notification observateur: {e}",
                      flush=True)
