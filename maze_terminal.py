from maze_config import Coordinate
from maze_generator import Grid, Wall


def render_maze(grid: Grid, entry: Coordinate, exit: Coordinate) -> str:
    lines: list[str] = []
    if not grid:
        return ""

    # render top line
    top_parts: list[str] = ["┌"]
    for x, cell in enumerate(grid[0]):
        top_parts.append("───" if cell & Wall.NORTH else "   ")
        if x == len(grid[0]) - 1:
            top_parts.append("┐")
        else:
            top_parts.append("┬")
    lines.append("".join(top_parts))

    # render inner maze
    for y, row in enumerate(grid):
        inner_maze: list[str] = []
        inner_maze.append("│" if row[0] & Wall.WEST else " ")
        for x, cell in enumerate(row):
            if (x, y) == entry:
                content = " E "
            elif (x, y) == exit:
                content = " X "
            else:
                content = "   "
            inner_maze.append(content)
            inner_maze.append("│" if cell & Wall.EAST else " ")
        lines.append("".join(inner_maze))
        if y != len(grid) - 1:
            sep_parts: list[str] = ["├"]
            for x, cell in enumerate(row):
                sep_parts.append("───" if cell & Wall.SOUTH else "   ")
                if x == len(row) - 1:
                    sep_parts.append("┤")
                else:
                    sep_parts.append("┼")
            lines.append("".join(sep_parts))

    # render bottom line
    bottom_parts: list[str] = ["└"]
    for x, cell in enumerate(grid[-1]):
        bottom_parts.append("───" if cell & Wall.SOUTH else "   ")
        if x == len(grid[-1]) - 1:
            bottom_parts.append("┘")
        else:
            bottom_parts.append("┴")
    lines.append("".join(bottom_parts))

    return "\n".join(lines)
