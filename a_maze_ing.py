from config.Config import Config
from Errors import ConfigError
from Logs import Log

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Configuration file must be provided in arguments\n"
              "Usage: python3 a_maze_ing.py <conf_file>")
        exit(-1)
    conf_file = sys.argv[1]

    logs = Log(verbose=True)
    config = Config(logs=logs)
    try:
        config.parse_config_file(conf_file)
        config.print_config()
    except ConfigError as e:
        print(e)
