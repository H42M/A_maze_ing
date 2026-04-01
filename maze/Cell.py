"""Single cell class management."""


class Cell:
    """Cell class."""

    def __init__(self, w: bool = True, s: bool = True,
                 e: bool = True, n: bool = True) -> None:
        """Initialize a Cell class instance.

        Args:
            w (bool): State of west wall.
            s (bool): State of south wall.
            e (bool): State of east wall.
            n (bool): State of north wall.

        Example:
            >>> cell = Cell(True, True, False, False)
        """
        self._w = w
        self._s = s
        self._e = e
        self._n = n

    @property
    def w(self) -> bool:
        """Gets the state of the west wall.

        Returns:
            bool: True if the wall exists, False otherwise.

        Example:
            >>> print(cell.w)
            True
        """
        return self._w

    @w.setter
    def w(self, value: bool) -> None:
        """Set the state of the west wall.

        Args:
            value (bool): New state of the west wall.

        Raises:
            TypeError: If value is not a boolean.

        Example:
            >>> cell.w = False
        """
        if not isinstance(value, bool):
            raise TypeError("Wall state must be a boolean.")
        self._w = value

    @property
    def s(self) -> bool:
        """Gets the state of the south wall.

        Returns:
            bool: True if the wall exists, False otherwise.

        Example:
            >>> print(cell.s)
            True
        """
        return self._s

    @s.setter
    def s(self, value: bool) -> None:
        """Set the state of the south wall.

        Args:
            value (bool): New state of the south wall.

        Raises:
            TypeError: If value is not a boolean.

            Example:
            >>> cell.s = False
        """
        if not isinstance(value, bool):
            raise TypeError("Wall state must be a boolean.")
        self._s = value

    @property
    def e(self) -> bool:
        """Gets the state of the east wall.

        Returns:
            bool: True if the wall exists, False otherwise.

        Example:
            >>> print(cell.e)
            True
        """
        return self._e

    @e.setter
    def e(self, value: bool) -> None:
        """Set the state of the east wall.

        Args:
            value (bool): New state of the east wall.

        Raises:
            TypeError: If value is not a boolean.

        Example:
            >>> cell.e = True
        """
        if not isinstance(value, bool):
            raise TypeError("Wall state must be a boolean.")
        self._e = value

    @property
    def n(self) -> bool:
        """Gets the state of the north wall.

        Returns:
            bool: True if the wall exists, False otherwise.

        Example:
            >>> print(cell.n)
            True
        """
        return self._n

    @n.setter
    def n(self, value: bool) -> None:
        """Set the state of the north wall.

        Args:
            value (bool): New state of the north wall.

        Raises:
            TypeError: If value is not a boolean.

        Example:
            >>> cell.n = True
        """
        if not isinstance(value, bool):
            raise TypeError("Wall state must be a boolean.")
        self._n = value
