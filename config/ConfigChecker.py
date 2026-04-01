"""Config checker class manager."""


from typing import Any
from Errors import ConfigError


class ConfigChecker:
    """Validates maze configuration parameters before use.

    Attributes:
        __max_size (int): Maximum allowed size for width and height.
        __min_size (int): Minimum allowed size for width and height.
    """

    __max_size = 20
    __min_size = 3

    @classmethod
    def check_width(cls, width: int) -> None:
        """Check that the width is within the allowed range.

        Args:
            width (int): The maze width to validate.

        Raises:
            ConfigError: If width is less than __min_size or greater
            than __max_size.
        """
        if width < cls.__min_size or width > cls.__max_size:
            raise ConfigError(f"Invalid width provided: {width}")

    @classmethod
    def check_height(cls, height: int) -> None:
        """Check that the height is within the allowed range.

        Args:
            height (int): The maze height to validate.

        Raises:
            ConfigError: If height is less than __min_size or greater
            than __max_size.
        """
        if height < cls.__min_size or height > cls.__max_size:
            raise ConfigError(f"Invalid height provided: {height}")

    @classmethod
    def check_entry(cls, entry: tuple[int, int], width: int,
                    height: int) -> None:
        """Check that the entry point is within the maze boundaries.

        Args:
            entry (tuple[int, int]): The (x, y) coordinates of the entry point.
            width (int): The maze width used as x boundary.
            height (int): The maze height used as y boundary.

        Raises:
            ConfigError: If entry coordinates are out of bounds.
        """
        if (entry[0] < 0 or entry[0] > width or
                entry[1] < 0 or entry[1] > height):
            raise ConfigError(f"Invalid entry provided: {entry}")

    @classmethod
    def check_exit(cls, exit: tuple[int, int], width: int,
                   height: int) -> None:
        """Check that the exit point is within the maze boundaries.

        Args:
            exit (tuple[int, int]): The (x, y) coordinates of the exit point.
            width (int): The maze width used as x boundary.
            height (int): The maze height used as y boundary.

        Raises:
            ConfigError: If exit coordinates are out of bounds.
        """
        if (exit[0] < 0 or exit[0] > width or
                exit[1] < 0 or exit[1] > height):
            raise ConfigError(f"Invalid exit provided: {exit}")

    @classmethod
    def check_output_file(cls, output_file: str) -> None:
        """Check that the output file path is not empty.

        Args:
            output_file (str): The output file path to validate.

        Raises:
            ConfigError: If output_file is an empty string or None.
        """
        if not output_file:
            raise ConfigError(f"Invalid output file provided: {output_file}")

    @classmethod
    def check_full_config(cls, config: dict[str, Any]) -> None:
        """Validate all parameters of a maze configuration dictionary.

        Runs all individual checks on the provided config. Stops and raises
        on the first invalid value encountered.

        Args:
            config (dict[str, Any]): A dictionary containing
            the following keys:
                - WIDTH (int): The maze width.
                - HEIGHT (int): The maze height.
                - ENTRY (tuple[int, int]): The entry point coordinates.
                - EXIT (tuple[int, int]): The exit point coordinates.
                - OUTPUT_FILE (str): The output file path.

        Raises:
            ConfigError: If any of the configuration values are invalid.
        """
        try:
            cls.check_width(config["WIDTH"])
            cls.check_height(config["HEIGHT"])
            cls.check_entry(config["ENTRY"], config["WIDTH"], config["HEIGHT"])
            cls.check_exit(config["EXIT"], config["WIDTH"], config["HEIGHT"])
            cls.check_output_file(config["OUTPUT_FILE"])
        except ConfigError as e:
            raise ConfigError(e)
