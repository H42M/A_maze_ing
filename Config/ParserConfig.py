from Errors import ConfigError
from typing import Union, cast


class ParserConfig:

    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        self.__expected_data = [
            'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT'
        ]
        self.__parsed_data = {}

    def init_config(self):
        from Config.Config import Config

        try:
            self.__parse_and_check()
        except Exception as e:
            raise ConfigError(e)

        config = Config(
            width=cast(int, self.__parsed_data['WIDTH']),
            height=cast(int, self.__parsed_data['HEIGHT']),
            exit=cast(tuple[int, int], self.__parsed_data['EXIT']),
            entry=cast(tuple[int, int], self.__parsed_data['ENTRY'])
        )

        return config

    def __parse_and_check(self):
        self.__parse()
        try:
            self.__check_parsed()
        except ValueError as e:
            raise ValueError(f"[PARSER-CHECKER ERROR] {e}")

    def __parse(self):
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
                else:
                    parsed_file[key] = int(value)

        self.__parsed_data = parsed_file

    def __check_parsed(self):
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

            elif key in ('EXIT', 'ENTRY'):
                if not (
                    isinstance(val, tuple)
                    and len(val) == 2
                    and all(isinstance(v, int) for v in val)
                ):
                    raise ValueError(f"{key} must be two integers (ex: 5,3)")
