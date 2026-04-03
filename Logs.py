"""Manage program logs."""

from enum import Enum


class LogType(Enum):
    """List of differents logs types."""

    LOGERROR = "LOGERROR"
    LOGINFO = "LOGINFO"
    LOGSUCESS = "LOGSUCCESS"


class Log:
    """Log class."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize Log instance.

        Args:
            verbose (bool): is program should print logs.

        Example:
            >>> logs = Log(verbose=True)
        """
        self.__verbose = verbose
        self.__logs: dict[LogType, list[str]] = {
            LogType.LOGERROR: [],
            LogType.LOGINFO: [],
            LogType.LOGSUCESS: []
        }

    def add_log(self, log: str, log_type: LogType) -> None:
        """Add log to the list.

        Args:
            log (str): Log string to add.
            log_type (LogType): Type of log added.

        Example:
            >>> logs.add_log("log exemple ....", LogType.LOGERROR)
        """
        self.__logs[log_type].append(log)
        if self.__verbose or log_type == LogType.LOGERROR:
            print(f"[{log_type.value}]: {log}")
