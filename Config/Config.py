from pydantic import BaseModel, Field, model_validator


class Config(BaseModel):
    """Store and validate maze configuration."""

    width: int = Field(gt=3, le=200)
    height: int = Field(gt=3, le=200)
    perfect: bool
    exit: tuple[int, int]
    entry: tuple[int, int]
    output_file: str = Field(min_length=5, max_length=50)

    @model_validator(mode='after')
    def check_coordinates(self) -> "Config":
        """Validate entry and exit coordinates."""
        for coordinate in [self.exit, self.entry]:
            x, y = coordinate
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                raise ValueError(f"Invalid Coordinates ({x}, {y})")
        if self.exit == self.entry:
            raise ValueError("Exit and Entry cannot be placed "
                             "as same location")
        return self
