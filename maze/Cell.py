"""Single cell class management."""


class Cell:
    """Cell class."""

    def __init__(self, x: int, y: int, w: bool = True, s: bool = True,
                 e: bool = True, n: bool = True,) -> None:
        """Initialize a Cell class instance.

        Args:
            x (int): postition x in the maze.
            y (int): position y in the maze.
            w (bool): State of west wall.
            s (bool): State of south wall.
            e (bool): State of east wall.
            n (bool): State of north wall.

        Example:
            >>> cell = Cell(True, True, False, False)
        """
        self._w: bool = w
        self._s: bool = s
        self._e: bool = e
        self._n: bool = n
        self._x = x
        self._y = y
        self._visited: bool = False
        self._42: bool = False

    @property
    def pos(self) -> tuple[int, int]:
        """Gets the pos of the Cell in the maze.

        Returns:
            tuple[int, int]: pos of the cell.

        Example:
            >>> print(cell.pos)
            (5, 3)
        """
        return (self.x, self.y)

    @property
    def x(self) -> int:
        """Gets the x pos of the Cell in the maze.

        Returns:
            int: x pos of the cell.

        Example:
            >>> print(cell.x)
            5
        """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        """Set the state of the x position.

        Args:
            value (int): New position.

        Raises:
            TypeError: If value is not a integer.

        Example:
            >>> cell.x = 5
        """
        if not isinstance(value, int):
            raise TypeError("X positon must be an integer.")
        self._x = value

    @property
    def y(self) -> int:
        """Gets the x pos of the Cell in the maze.

        Returns:
            int: x pos of the cell.

        Example:
            >>> print(cell.x)
            5
        """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        """Set the state of the x position.

        Args:
            value (int): New position.

        Raises:
            TypeError: If value is not a integer.

        Example:
            >>> cell.x = 5
        """
        if not isinstance(value, int):
            raise TypeError("X positon must be an integer.")
        self._y = value

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

    @property
    def visited(self) -> bool:
        """Gets the state of the cell.

        Returns:
            bool: True if the has visited.

        Example:
            >>> print(cell.visited)
            True
        """
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> None:
        """Set the state of the cell.

        Args:
            value (bool): New state of the cell.

        Raises:
            TypeError: If value is not a boolean.

        Example:
            >>> cell.n = True
        """
        if not isinstance(value, bool):
            raise TypeError("Cell state must be a boolean.")
        self._visited = value

    @property
    def is42(self) -> bool:
        """Gets the state of the cell.

        Returns:
            bool: True if the has visited.

        Example:
            >>> print(cell.visited)
            True
        """
        return self._42

    @is42.setter
    def is42(self, value: bool) -> None:
        """Set the state of the cell.

        Args:
            value (bool): New state of the cell.

        Raises:
            TypeError: If value is not a boolean.

        Example:
            >>> cell.n = True
        """
        if not isinstance(value, bool):
            raise TypeError("Cell state must be a boolean.")
        self._42 = value
