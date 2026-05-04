"""Configuration file parser for maze settings.

Provides a parser class to read maze configuration from text files
and validate the parameters before creating a Config object.
"""

from Errors import ConfigError
from typing import Union, cast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Config.Config import Config


class ParserConfig:
    """Parser for maze configuration files.

    Reads maze configuration from a text file, validates the data,
    and creates a Config object. Configuration files should contain
    key-value pairs separated by '=' (WIDTH, HEIGHT, ENTRY, EXIT).

    Attributes:
        _ParserConfig__file_path (str): Path to the configuration file.
        _ParserConfig__expected_data (list): Expected configuration keys.
        _ParserConfig__parsed_data (dict): Parsed configuration data.
    """

    def __init__(self, file_path: str) -> None:
        """Initialize the parser with a configuration file path.

        Args:
            file_path (str): Path to the configuration file to parse.
        """
        self.__file_path = file_path
        self.__expected_data = [
            'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'PERFECT'
        ]
        self.__parsed_data: dict[str, Union[int, tuple[int, int]]] = {}

    def init_config(self) -> "Config":
        """Parse configuration file and return a Config object.

        Returns:
            Config: A validated configuration object.

        Raises:
            ConfigError: If parsing or validation fails.
        """
        from Config.Config import Config

        try:
            self.__parse_and_check()
        except Exception as e:
            raise ConfigError(e)

        config = Config(
            width=cast(int, self.__parsed_data['WIDTH']),
            height=cast(int, self.__parsed_data['HEIGHT']),
            perfect=cast(bool, self.__parsed_data['PERFECT']),
            exit=cast(tuple[int, int], self.__parsed_data['EXIT']),
            entry=cast(tuple[int, int], self.__parsed_data['ENTRY'])
        )

        return config

    def __parse_and_check(self) -> None:
        """Parse the file and validate all configuration values.

        Raises:
            ValueError: If validation fails during parsing or checking.
        """
        self.__parse()
        try:
            self.__check_parsed()
        except ValueError as e:
            raise ValueError(f"[PARSER-CHECKER ERROR] {e}")

    def __parse(self) -> None:
        """Parse key-value pairs from the configuration file.

        Reads the file line by line, skipping comments and empty lines.
        Supports both integer values and coordinate tuples (x,y).

        Raises:
            ValueError: If coordinate format is invalid.
        """
        parsed_file: dict[str, Union[int, tuple[int, int]]] = {}

        with open(self.__file_path, 'r') as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                if ',' in value:
                    parts = value.split(',')
                    if len(parts) != 2:
                        raise ValueError(f"Invalid coord format for {key}")

                    x = int(parts[0].strip())
                    y = int(parts[1].strip())

                    parsed_file[key] = (x, y)
                elif key == 'PERFECT':
                    parsed_file[key] = (True if value.upper() == 'TRUE'
                                        else False)
                else:
                    parsed_file[key] = int(value)

        self.__parsed_data = parsed_file

    def __check_parsed(self) -> None:
        """Validate that all required keys exist and have correct types.

        Ensures all expected configuration keys are present and validates
        data types for WIDTH, HEIGHT, ENTRY, and EXIT.

        Raises:
            ValueError: If required keys are missing or types are invalid.
        """
        for expected in self.__expected_data:
            if expected not in self.__parsed_data:
                raise ValueError(f"Expected {expected} in config file")

        for key, val in self.__parsed_data.items():

            if key == 'WIDTH':
                if not isinstance(val, int):
                    raise ValueError("Width must be an integer")

            elif key == 'HEIGHT':
                if not isinstance(val, int):
                    raise ValueError("Height must be an integer")

            elif key == "PERFECT":
                if not isinstance(val, bool):
                    raise ValueError("Perfect must be boolean")

            elif key in ('EXIT', 'ENTRY'):
                if not (
                    isinstance(val, tuple)
                    and len(val) == 2
                    and all(isinstance(v, int) for v in val)
                ):
                    raise ValueError(f"{key} must be two integers (ex: 5,3)")
