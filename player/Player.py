import pygame
from typing import Optional

from Maze.Maze import Maze
from render.RenderObj import RenderObj
from render.RenderBloc import Bloc
from Config.GameState import GameState


class Player:
    def __init__(self, maze: Maze, player_skin: Optional[str] = None) -> None:
        self.__maze = maze
        self.__speed = 3
        self.__size = GameState.bloc_size
        if maze.entry:
            half_width = int(GameState.cell_size[0] / 2)
            half_height = int(GameState.cell_size[1] / 2)
            self.__pos = pygame.Vector2(
                (maze.entry.x * GameState.cell_size[0]) +
                maze.gap[0] + half_width,
                (maze.entry.y * GameState.cell_size[1]) +
                maze.gap[1] + half_height
            )
        else:
            print("Error: Maze entry point is not defined.")
            self.__pos = pygame.Vector2(0, 0)

        self.__skin_path = player_skin

    def render(self, screen):
        if self.__skin_path:
            color = self.__skin_path
            Bloc.load_image(color)
        else:
            color = (255, 0, 0)

        render_player = Bloc(
            pos=(int(self.__pos.x), int(self.__pos.y)),
            color=color
        )
        render_player.render(screen)

    def get_keys(self):
        # render_maze = self.__maze.get_render_maze()
        keys = pygame.key.get_pressed()
        new_pos = pygame.Vector2(self.__pos)

        if keys[pygame.K_LEFT]:
            new_pos.x -= self.__speed
        if keys[pygame.K_RIGHT]:
            new_pos.x += self.__speed
        if keys[pygame.K_UP]:
            new_pos.y -= self.__speed
        if keys[pygame.K_DOWN]:
            new_pos.y += self.__speed

        # if not self.__check_collision(new_pos, render_maze):
        self.__pos = new_pos

    def __check_collision(self, pos: pygame.Vector2,
                          render_maze: list[RenderObj]) -> bool:
        # Hitbox du joueur à la nouvelle position
        player_rect = pygame.Rect(pos.x, pos.y, *self.__size)

        # On vérifie chaque mur du labyrinthe
        for wall in render_maze:
            if wall.collision:
                wall_rect = pygame.Rect(
                    wall._pos[0],
                    wall._pos[1],
                    wall._size[0],
                    wall._size[1]
                )
                if player_rect.colliderect(wall_rect):
                    return True  # collision détectée

        return False  # pas de collision

    def __load_skin(self, skin_path):
        import os
        try:
            if os.path.isfile(skin_path):
                image = pygame.image.load(skin_path)
                self.__skin = pygame.transform.scale(image, self.__size)
                print(f"Skin loaded: {skin_path}", flush=True)
                return True
            else:
                print(f"Skin image not found: {skin_path}", flush=True)
                return False
        except Exception as e:
            print(f"Error loading Skin: {e}", flush=True)
            return False
