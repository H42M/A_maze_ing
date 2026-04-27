from render.Render import Render
from render.RenderButtons import ToggleButton, Button, SelectButton
from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from player.Player import Player
from Errors import ConfigError
from Config.GameState import GameState
from Config.ThemeManager import ThemeManager

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

        # Initialiser le thème
        theme_manager = ThemeManager()
        theme_manager.load_themes_config('Config/themes.json')

        # Charger le thème par défaut
        default_theme = 'MARIO'
        if not theme_manager.set_theme(default_theme):
            raise ConfigError(
                f"Impossible de charger le theme: {default_theme}")

        # Récupérer les textures du thème
        textures = theme_manager.get_all_textures()
        print(textures)
        bg_tex = textures.get('background')
        wall_tex = textures.get('wall')
        player_tex = textures.get('player')

        if bg_tex:
            render.load_background(bg_tex)

        if wall_tex:
            maze = Maze(config, wall_tex)
        else:
            maze = Maze(config, (100, 100, 100))
            print('Wall Texture not loaded')

        if player_tex:
            player = Player(maze, player_tex)
        else:
            player = Player(maze, None)
            print('Playeer Texture not loaded')

        # Enregistrer la mise à jour du Maze pour les changements
        def update_maze_texture(theme_name: str):
            # Mettre à jour GameState avec les nouvelles textures du thème
            GameState.set_theme(theme_name)
            
            new_textures = theme_manager.get_all_textures()
            new_wall = new_textures.get('wall')
            if new_wall:
                maze.update_texture(new_wall)

        # Enregistrer la mise à jour du Player
        def update_player_texture(theme_name: str):
            new_textures = theme_manager.get_all_textures()
            new_player = new_textures.get('player')
            if new_player:
                player.update_texture(new_player)

        theme_manager.register_observer(update_maze_texture)
        theme_manager.register_observer(update_player_texture)

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
                         callback=theme_manager.set_theme,
                         options=theme_manager.get_available_themes()
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
