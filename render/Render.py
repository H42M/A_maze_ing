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
        Gérer les événements et les clics de boutons

        Args:
            buttons: liste des boutons à vérifier
        """
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si un bouton est cliqué
                if buttons:
                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            button.execute()

        # Mettre à jour l'état de survol des boutons
        if buttons:
            for button in buttons:
                button.update_hover(mouse_pos)

        return True

    def clear(self):
        """Effacer l'écran avec le background ou une couleur"""
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
