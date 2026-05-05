import pygame
from typing import Optional, Union

from Maze.Maze import Maze
from render.RenderBloc import Bloc
from Config.GameState import GameState


class Player:
    """Control and render the maze player."""

    def __init__(self, maze: Maze, player_skin: Optional
                 [Union[str, pygame.Surface]] = None) -> None:
        """Initialize the player."""
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

    def render(self, screen: pygame.Surface) -> None:
        """Render the player."""
        if isinstance(self.__skin_path, pygame.Surface):
            render_player = Bloc(
                pos=(int(self.__pos.x), int(self.__pos.y)),
                texture=self.__skin_path
            )
            render_player.render(screen)
            return

        render_player = Bloc(
            pos=(int(self.__pos.x), int(self.__pos.y)),
            color=(255, 0, 0)
        )
        render_player.render(screen)

    def get_keys(self) -> None:
        """Move the player from keyboard input."""
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

        if not self.__check_collision(new_pos):
            self.__pos = new_pos

    def __check_collision(self, pos: pygame.Vector2) -> bool:
        """Return whether the player collides at a position."""
        player_rect = pygame.Rect(pos.x, pos.y, *self.__size)

        for row in self.__maze.maze_lst:
            for cell in row:
                render_cell = cell.get_render_cell()
                for wall in render_cell:
                    if wall.collision:
                        wall_rect = pygame.Rect(
                            wall._pos[0],
                            wall._pos[1],
                            wall._size[0],
                            wall._size[1]
                        )
                        if player_rect.colliderect(wall_rect):
                            return True
        return False

    def reset_pos(self) -> None:
        """Reset the player to the maze entry."""
        if self.__maze.entry:
            half_width = int(GameState.cell_size[0] / 2)
            half_height = int(GameState.cell_size[1] / 2)
            self.__pos = pygame.Vector2(
                (self.__maze.entry.x * GameState.cell_size[0]) +
                self.__maze.gap[0] + half_width,
                (self.__maze.entry.y * GameState.cell_size[1]) +
                self.__maze.gap[1] + half_height
            )
        else:
            print("Error: Maze entry point is not defined.")
            self.__pos = pygame.Vector2(0, 0)

    def update_texture(self, texture: pygame.Surface) -> None:
        """Update the player texture."""
        if texture:
            self.__skin_path = texture