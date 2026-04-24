from render.Render import Render
from render.RenderButtons import ToggleButton, Button, SelectButton
from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from player.Player import Player
from Errors import ConfigError
from Config.GameState import GameState

if __name__ == "__main__":
    try:
        parser = ParserConfig('settings.txt')
        config = parser.init_config()

        render = Render()
        GameState.initialize(
            config,
            render.screen.get_size(),
            cell_nb_bloc=3,
            wall_thickness=5
            )
        render.load_background(GameState.bg_texture)
        maze = Maze(config, GameState.wall_texture)
        player = Player(maze, GameState.player_texture)
        btns = [
            ToggleButton('Afficher la solution',
                         (10, 10),
                         (200, 60),
                         maze.set_display_soluce,
                         maze.get_display_soluce,
                         ),
            Button('Generer a nouveau',
                   pos=(210, 10),
                   size=(200, 60),
                   callback=[maze.reset, player.reset_pos]),
            SelectButton('Choisir un theme',
                         pos=(450, 10),
                         size=(200, 60),
                         callback=GameState.set_theme,
                         options=GameState.get_themes()
                         )
        ]

    except ConfigError as e:
        print(f"[CONFIG ERROR] {e}")
        exit()
    except Exception as e:
        print(f"[OTHER ERROR] {e}")
        exit()

    while True:
        if not render.handle_events(btns):
            break
        render.clear()
        [btn.render(render.screen) for btn in btns]
        if not maze.is_maze_generated:
            if maze.generate_anim():
                maze.solve()

        maze.render(render.screen)

        if maze.is_maze_generated:
            player.get_keys()
            player.render(render.screen)
        render.flip()
    render.quit()
