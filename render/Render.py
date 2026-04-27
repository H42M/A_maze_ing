import pygame
from typing import Optional


class Render:

    def __init__(self) -> None:
        pygame.init()
        self.__screen_size = (800, 800)
        self.__screen_name = "Hello World"
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode(
            self.__screen_size,
            # pygame.RESIZABLE
        )
        pygame.display.set_caption(self.__screen_name)
        self.__background = None

        # S'enregistrer pour les changements de theme
        try:
            from Config.ThemeManager import ThemeManager
            self.theme_manager = ThemeManager()
            self.theme_manager.register_observer(
                self.on_theme_changed)
            print("Render enregistre", flush=True)
        except Exception as e:
            print(f"Erreur observer theme: {e}", flush=True)
            self.theme_manager = None

    def on_theme_changed(self, theme_name: str) -> None:
        """Callback appele quand le theme change"""
        print(f"Render - Nouveau theme: {theme_name}", flush=True)
        self.__reload_theme_assets()

    def __reload_theme_assets(self) -> None:
        """Recharger les assets du theme"""
        if self.theme_manager:
            bg_texture = self.theme_manager.get_texture('background')
            if bg_texture:
                self.load_background(bg_texture)

    def load_background(self, bg: pygame.Surface) -> bool:
        """Charger une image comme background"""
        try:

            self.__background = pygame.transform.scale(bg,
                                                       self.__screen_size)
            return True
        except Exception as e:
            print(f"Error loading background: {e}", flush=True)
            return False

    def handle_events(self, buttons: Optional[list] = None) -> bool:
        """
        Gerer les evenements et les clics de boutons

        Args:
            buttons: liste des boutons à verifier
        """
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifier si un bouton est clique
                if buttons:
                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            button.execute()

        # Mettre à jour l'etat de survol des boutons
        if buttons:
            for button in buttons:
                button.update_hover(mouse_pos)

        return True

    def clear(self):
        """Effacer l'ecran avec le background ou une couleur"""
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self):
        self.__clock.tick(60)
        pygame.display.flip()

    def get_screen_size(self):
        return self.__screen.get_size()

    def quit(self):
        pygame.quit()

    @property
    def screen(self):
        return self.__screen
