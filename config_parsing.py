from dotenv import dotenv_values
from typing import Dict
from maze_config import MazeConfig, CleanConfig


class MazeConfigLoader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.config: Dict[str, str | None] = {}
        self.cleaned_config: CleanConfig | None

    def read_config(self) -> None:
        config: Dict[str, str | None] = {}

        try:
            config = dotenv_values("config.txt")
        except FileNotFoundError:
            print(
                "config.txt not found, generating maze with default_config..."
                )
        self.config = config

    def clean_config(self) -> None:
        cfg = self.config
        new_cfg: Dict = {}

        for k, v in cfg.items():
            if v is None:
                raise ValueError(f"Missing value for {k}")
            elif k in ("WIDTH", "HEIGHT"):
                new_cfg[k.lower()] = int(v)
            elif k in ("ENTRY", "EXIT"):
                x, y = v.split(sep=",")
                new_cfg[k.lower()] = (int(x), int(y))
            elif k == "OUTPUT_FILE":
                new_cfg[k.lower()] = v.lower()
            elif k == "PERFECT":
                new_cfg[k.lower()] = True if v == "True" else False
            else:
                raise ValueError("Incorrect shape for config.txt")

        self.cleaned_config = new_cfg

    def load(self) -> MazeConfig:
        self.read_config()
        self.clean_config()
        return MazeConfig(**self.cleaned_config)
