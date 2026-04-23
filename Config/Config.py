from pydantic import BaseModel, Field, model_validator


class Config(BaseModel):

    width: int = Field(gt=3, le=50)
    height: int = Field(gt=3, le=50)
    exit: tuple[int, int]
    entry: tuple[int, int]

    @model_validator(mode='after')
    def check_coordinates(self):
        for coordinate in [self.exit, self.entry]:
            x, y = coordinate
            if x < 0 or x > self.width or y < 0 or y > self.height:
                raise ValueError(f"Invalid Coordinates ({x}, {y})")
        if self.exit == self.entry:
            raise ValueError("Exit and Entry cannot be placed "
                             "as same location")
        return self
