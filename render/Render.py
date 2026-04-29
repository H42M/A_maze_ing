"""Main render engine module.

Provides the Render class for managing the pygame display, handling events,
loading backgrounds, and managing theme changes.
"""

import pygame
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from render.RenderObj import RenderObj


class Render:
    """Main rendering engine for the game.

    Manages pygame display, screen updates, event handling, background
    textures, and theme change notifications.

    Attributes:
        _Render__screen_size (tuple): Display dimensions.
        _Render__screen_name (str): Window title.
        _Render__clock (pygame.time.Clock): Game loop timer.
        _Render__screen (pygame.Surface): Main display surface.
        _Render__background (pygame.Surface): Current background texture.
        theme_manager: Manager for theme handling.
    """

    def __init__(self) -> None:
        """Initialize the rendering engine with pygame.

        Sets up the display, clock, and theme manager observer.
        """
        pygame.init()
        self.__screen_size = (1000, 1000)
        self.__screen_name = "Hello World"
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(
            self.__screen_size,
            # pygame.RESIZABLE
        )
        pygame.display.set_caption(self.__screen_name)
        self.__background: Optional[pygame.Surface] = None

        # S'enregistrer pour les changements de theme
        from Config.ThemeManager import ThemeManager
        self.theme_manager: Optional[ThemeManager]

        try:
            self.theme_manager = ThemeManager()
            self.theme_manager.register_observer(
                self.on_theme_changed)
            print("Render enregistre", flush=True)
        except Exception as e:
            print(f"Erreur observer theme: {e}", flush=True)
            self.theme_manager = None

    def on_theme_changed(self, theme_name: str) -> None:
        """Handle theme change notification.

        Args:
            theme_name (str): Name of the new active theme.
        """
        print(f"Render - Nouveau theme: {theme_name}", flush=True)
        self.__reload_theme_assets()

    def __reload_theme_assets(self) -> None:
        """Reload theme assets from the theme manager.

        Called when theme changes to update the background and other textures.
        """
        if self.theme_manager:
            bg_texture = self.theme_manager.get_texture('background')
            if bg_texture:
                self.load_background(bg_texture)

    def load_background(self, bg: pygame.Surface) -> bool:
        """Load and scale a background image.

        Args:
            bg (pygame.Surface): The background surface to load.

        Returns:
            bool: True if loading succeeded, False otherwise.
        """
        try:

            self.__background = pygame.transform.scale(bg,
                                                       self.__screen_size)
            return True
        except Exception as e:
            print(f"Error loading background: {e}", flush=True)
            return False

    def handle_events(self, buttons: Optional[list["RenderObj"]] = None
                      ) -> bool:
        """Handle pygame events and button clicks.

        Args:
            buttons (Optional[list]): List of button objects to check
            for clicks.

        Returns:
            bool: False if quit event received, True otherwise.
        """
        from render.RenderButtons import Button
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifier si un bouton est clique
                if buttons:
                    for button in buttons:
                        if isinstance(button, Button):
                            if button.is_clicked(mouse_pos):
                                button.execute()

        # Mettre à jour l'etat de survol des boutons
        if buttons:
            for button in buttons:
                if isinstance(button, Button):
                    button.update_hover(mouse_pos)

        return True

    def clear(self) -> None:
        """Clear the screen with background or black color.

        Fills the screen with either the loaded background or black color.
        """
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        """Update the display and control frame rate.

        Updates the pygame display and limits the frame rate to 60 FPS.
        """
        self.__clock.tick(60)
        pygame.display.flip()

    def get_screen_size(self) -> tuple[int, int]:
        """Get the current screen dimensions.

        Returns:
            tuple: Screen size (width, height).
        """
        return self.__screen.get_size()

    def quit(self) -> None:
        """Cleanup pygame and exit.

        Closes pygame and releases resources.
        """
        pygame.quit()

    @property
    def screen(self) -> pygame.Surface:
        """Get screen instance.

        Returns:
            pygame.Surface: Screen instance.
        """
        return self.__screen
