from dotenv import dotenv_values
from typing import Dict
from maze_config import MazeConfig
from pathlib import Path


class MazeConfigLoader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.config: Dict[str, str | None] = {}

    def read_config(self) -> None:
        config_path = Path(self.path)

        if not config_path.is_file():
            raise FileNotFoundError(f"{self.path} not found")
        self.config = dotenv_values(self.path)

    def clean_config(self) -> MazeConfig:
        cfg = self.config

        width_raw = cfg.get("WIDTH")
        height_raw = cfg.get("HEIGHT")
        entry_raw = cfg.get("ENTRY")
        exit_raw = cfg.get("EXIT")
        output_file = cfg.get("OUTPUT_FILE")
        perfect_raw = cfg.get("PERFECT")
        seed_raw = cfg.get("SEED")

        if width_raw is None:
            raise ValueError("Missing WIDTH")
        if height_raw is None:
            raise ValueError("Missing HEIGHT")
        if entry_raw is None:
            raise ValueError("Missing ENTRY")
        if exit_raw is None:
            raise ValueError("Missing EXIT")
        if output_file is None:
            raise ValueError("Missing OUTPUT_FILE")
        if perfect_raw is None:
            raise ValueError("Missing PERFECT")

        entry_x, entry_y = entry_raw.split(",")
        exit_x, exit_y = exit_raw.split(",")

        perfect_value = perfect_raw.strip().lower()
        if perfect_value == "true":
            perfect = True
        elif perfect_value == "false":
            perfect = False
        else:
            raise ValueError("PERFECT must be True or False")

        return MazeConfig(
            width=int(width_raw),
            height=int(height_raw),
            entry=(int(entry_x), int(entry_y)),
            exit=(int(exit_x), int(exit_y)),
            output_file=output_file,
            perfect=perfect,
            seed=None if seed_raw is None else int(seed_raw)
        )

    def load(self) -> MazeConfig:
        self.read_config()
        return self.clean_config()
