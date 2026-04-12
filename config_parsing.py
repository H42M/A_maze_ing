from dotenv import dotenv_values
from typing import Dict


class MazeConfigParser:
    @staticmethod
    def default_parser() -> Dict[str, str | None]:
        config: Dict[str, str | None] = {}

        try:
            config = dotenv_values("config.txt")
        except FileNotFoundError:
            print(
                "config.txt not found, generating maze with default_config..."
                )
        return config
