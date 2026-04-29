"""Configuration data model for maze generation.

This module defines the pydantic model for storing maze configuration
parameters such as width, height, entry, and exit coordinates.
"""

from pydantic import BaseModel, Field, model_validator


class Config(BaseModel):
    """Maze configuration model.

    This class validates and stores the configuration parameters
    for maze generation including dimensions and entry/exit points.

    Attributes:
        width (int): Width of the maze (3 < width <= 50).
        height (int): Height of the maze (3 < height <= 50).
        exit (tuple[int, int]): Exit coordinates (x, y).
        entry (tuple[int, int]): Entry coordinates (x, y).
    """

    width: int = Field(gt=3, le=50)
    height: int = Field(gt=3, le=50)
    exit: tuple[int, int]
    entry: tuple[int, int]

    @model_validator(mode='after')
    def check_coordinates(self):
        """Validate that all coordinates are within maze bounds.

        Ensures that entry and exit coordinates are within the maze
        dimensions and that they are not at the same location.

        Returns:
            Config: The validated configuration object.

        Raises:
            ValueError: If coordinates are invalid or out of bounds.
        """
        for coordinate in [self.exit, self.entry]:
            x, y = coordinate
            if x < 0 or x > self.width or y < 0 or y > self.height:
                raise ValueError(f"Invalid Coordinates ({x}, {y})")
        if self.exit == self.entry:
            raise ValueError("Exit and Entry cannot be placed "
                             "as same location")
        return self
