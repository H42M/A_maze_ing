from typing import Any
from Errors import ConfigError


class ConfigChecker:

    __max_size = 20
    __min_size = 3

    @classmethod
    def check_width(cls, width: int) -> None:
        if width < cls.__min_size or width > cls.__max_size:
            raise ConfigError(f"Invalid width provided: {width}")

    @classmethod
    def check_height(cls, height: int) -> None:
        if height < cls.__min_size or height > cls.__max_size:
            raise ConfigError(f"Invalid height provided: {height}")

    @classmethod
    def check_entry(cls, entry: tuple[int, int], width: int,
                    height: int) -> None:
        if (entry[0] < 0 or entry[0] > width or
                entry[1] < 0 or entry[1] > height):
            raise ConfigError(f"Invalid entry provided: {entry}")

    @classmethod
    def check_exit(cls, exit: tuple[int, int], width: int,
                   height: int) -> None:
        if (exit[0] < 0 or exit[0] > width or
                exit[1] < 0 or exit[1] > height):
            raise ConfigError(f"Invalid exit provided: {exit}")

    @classmethod
    def check_output_file(cls, output_file: str) -> None:
        if not output_file:
            raise ConfigError(f"Invalid output file provided: {output_file}")

    # @classmethod
    # def check_perfect(cls, perfect: bool) -> None:
    #     if perfect or not perfect:
    #         raise ConfigError(f"Invalid perfect parameter provided: {perfect}")

    @classmethod
    def check_full_config(cls, config: dict[str, Any]) -> None:
        try:
            cls.check_width(config["WIDTH"])
            cls.check_height(config["HEIGHT"])
            cls.check_entry(config["ENTRY"], config["WIDTH"], config["HEIGHT"])
            cls.check_exit(config["EXIT"], config["WIDTH"], config["HEIGHT"])
            cls.check_output_file(config["OUTPUT_FILE"])
        except ConfigError as e:
            raise ConfigError(e)
