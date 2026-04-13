from typing import Tuple, Self, TypedDict
from pydantic import BaseModel, Field, model_validator


class CleanConfig(TypedDict):
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


class MazeConfig(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str = Field(min_length=1)
    perfect: bool
    seed: int | None = None

    def bounds_check(self, position: Tuple[int, int]) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    @model_validator(mode="after")
    def entry_and_exit_validation(self) -> Self:
        if self.entry == self.exit:
            raise ValueError("Entry can't be the same as exit")
        if (
            not self.bounds_check(self.entry)
            or not self.bounds_check(self.exit)
        ):
            raise ValueError("Entry and exit must be within the maze bounds")
        return self
