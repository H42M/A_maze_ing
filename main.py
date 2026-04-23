from render.Render import Render
from Maze.Maze import Maze
from Config.ParserConfig import ParserConfig
from player.Player import Player
from Errors import ConfigError
from Config.GameState import GameState

if __name__ == "__main__":
    try:
        parser = ParserConfig('settings.txt')
        config = parser.init_config()

        render = Render(background_image='srcs/mario-cloud-bg-1.png')
        GameState.initialize(
            config,
            render.screen.get_size(),
            cell_nb_bloc=3,
            wall_thickness=5
            )
        maze = Maze(config)
        player = Player(maze, 'srcs/mario.png')

    except ConfigError as e:
        print(f"[CONFIG ERROR] {e}")
        exit()
    except Exception as e:
        print(f"[OTHER ERROR] {e}")
        exit()

    maze_over = False
    # maze.set_color((255, 255, 0))
    maze.set_color('srcs/mario-cloud.png')
    while True:
        if not render.handle_events():
            break
        render.clear()
        if not maze_over:
            if maze.generate_anim():
                maze_over = True
                maze.solve()

        maze.render(render.screen)

        if maze_over:
            player.get_keys()
            player.render(render.screen)
        render.flip()
    render.quit()
