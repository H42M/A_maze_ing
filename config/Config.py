"""Manage config object."""


from Logs import Log, LogType
from Errors import ConfigError
from .ConfigChecker import ConfigChecker

from typing import Optional, Any
import os


class Config:
    """Config Object."""

    def __init__(self, logs: Log, width: Optional[int] = None,
                 height: Optional[int] = None,
                 entry: Optional[tuple[int, int]] = None,
                 exit: Optional[tuple[int, int]] = None,
                 output_file: Optional[str] = None,
                 perfect: Optional[bool] = None,
                 config_path: Optional[str] = None) -> None:
        """Initialize Config instance.

        Args:
            logs (Log): Log manager.
            width (int): Maze width.
            height (int): Maze height.
            entry (tuple[int, int]): entry coordinates.
            exit (tuple[int, int]):  exit coordinates.

        Example:
            >>> config = Config()
        """
        self.__config: dict[str, Any] = {
            "WIDTH": width,
            "HEIGHT": height,
            "ENTRY": entry,
            "EXIT": exit,
            "OUTPUT_FILE": output_file,
            "PERFECT": perfect
        }
        self.__logs = logs

        if config_path:
            self.parse_config_file(config_path)

    def parse_config_file(self, config_path: str) -> None:
        """Parse configuration and check results.

        Args:
            config_path (str): path of config file.

        Raises:
            ConfigError: if config file is not correct.

        Example:
            >>> calculate_bmi(70, 1.75)
            22.86
        """
        if not os.path.isfile(config_path):
            raise ConfigError(f"Config file doesnt exist: {config_path}")

        with open(config_path, "r") as f:
            for line in f:
                if line.strip()[0] != "#":
                    key, value = line.split("=", maxsplit=1)
                    if key.strip() not in self.__config:
                        error_str = f"Unexpected parameter: {key}"
                        self.__logs.add_log(error_str, LogType.LOGERROR)
                        raise ConfigError()
                    if " " in line:
                        error_str = f"Unexpected space on line: {line}"
                        self.__logs.add_log(error_str, LogType.LOGERROR)
                        raise ConfigError()

                    if key in ["WIDTH", "HEIGHT"]:
                        self.__config[key] = int(value)
                    elif key in ["ENTRY", "EXIT"]:
                        val1, val2 = value.split(",")
                        self.__config[key] = tuple([int(val1), int(val2)])
                    elif key == "PERFECT":
                        self.__config[key] = (value.upper() == "TRUE")
                    elif key == "OUTPUT_FILE":
                        self.__config[key] = value.strip()
                    else:
                        self.__config[key] = value

        missing_conf = []
        for key, value in self.__config.items():
            if not value and key != "PERFECT":
                missing_conf.append(key)
        if missing_conf:
            raise ConfigError(f"Missing {missing_conf} in "
                              "configuration file")
        try:
            ConfigChecker.check_full_config(self.__config)
        except ConfigError as e:
            raise ConfigError(e)
        self.__logs.add_log("Config Successfully Parsed!",
                            LogType.LOGSUCESS)

    def print_config(self) -> None:
        """Print the current configuration.

        Example:
            >>> config.print_config()
            <config printed>
        """
        print("*******************")
        for key, value in self.__config.items():
            print(f" * {key}: {value}")
        print("*******************")

    # Getters
    @property
    def width(self) -> Optional[int]:
        """Gets the maze width.

        Returns:
            Optional[int]: The maze width, or None if not set.
        """
        return self.__config["WIDTH"]

    @property
    def height(self) -> Optional[int]:
        """Gets the maze height.

        Returns:
            Optional[int]: The maze height, or None if not set.
        """
        return self.__config["HEIGHT"]

    @property
    def entry(self) -> Optional[tuple[int, int]]:
        """Gets the entry point coordinates.

        Returns:
            Optional[tuple[int, int]]: The (x, y) entry coordinates,
            or None if not set.
        """
        return self.__config["ENTRY"]

    @property
    def exit(self) -> Optional[tuple[int, int]]:
        """Gets the exit point coordinates.

        Returns:
            Optional[tuple[int, int]]: The (x, y) exit coordinates,
            or None if not set.
        """
        return self.__config["EXIT"]

    @property
    def output_file(self) -> Optional[str]:
        """Gets the output file path.

        Returns:
            Optional[str]: The output file path, or None if not set.
        """
        return self.__config["OUTPUT_FILE"]

    @property
    def perfect(self) -> Optional[bool]:
        """Gets the perfect maze flag.

        Returns:
            Optional[bool]: True if the maze should be perfect,
            False otherwise, or None if not set.
        """
        return self.__config["PERFECT"]

    @property
    def config(self) -> dict[str, Any]:
        """Gets the full configuration dictionary.

        Returns:
            dict[str, Any]: The complete configuration with all keys
            and values.
        """
        return self.__config
