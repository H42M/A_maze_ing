from enum import Enum


class LogType(Enum):
    LOGERROR = "LOGERROR"
    LOGINFO = "LOGINFO"
    LOGSUCESS = "LOGSUCCESS"


class Log:
    def __init__(self, verbose: bool = False) -> None:
        self.__verbose = verbose
        self.__logs: dict[LogType, list[str]] = {
            LogType.LOGERROR: [],
            LogType.LOGINFO: [],
            LogType.LOGSUCESS: []
        }

    def add_log(self, log: str, log_type: LogType) -> None:
        self.__logs[log_type].append(log)
        if self.__verbose or log_type == LogType.LOGERROR:
            print(f"[{log_type.value}]: {log}")
