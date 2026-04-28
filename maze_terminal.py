from maze_config import Coordinate
from maze_generator import Grid, Wall


def get_direction(start: Coordinate, end: Coordinate) -> str:
    x1, y1 = start
    x2, y2 = end
    if x2 == x1 + 1 and y2 == y1:
        return "E"
    if x2 == x1 - 1 and y2 == y1:
        return "W"
    if y2 == y1 + 1 and x2 == x1:
        return "S"
    if y2 == y1 - 1 and x2 == x1:
        return "N"
    raise ValueError("Path contains non-adjacent cells")


def opposite(direction: str) -> str:
    opposites = {
        "N": "S",
        "E": "W",
        "S": "N",
        "W": "E",
    }
    return opposites[direction]


def build_path_connections(
        path: list[Coordinate]) -> dict[Coordinate, set[str]]:
    connections: dict[Coordinate, set[str]] = {}
    for current, next_cell in zip(path, path[1:]):
        direction = get_direction(current, next_cell)
        if current not in connections:
            connections[current] = set()
        if next_cell not in connections:
            connections[next_cell] = set()
        connections[current].add(direction)
        connections[next_cell].add(opposite(direction))
    return connections


def render_maze(grid: Grid, entry: Coordinate, exit: Coordinate,
                path: list[Coordinate] | None = None) -> str:
    lines: list[str] = []
    path_connections = build_path_connections(path) if path else {}
    path_cells = set(path) if path is not None else set()
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
            elif (x, y) in path_cells:
                content = " • "
            else:
                content = "   "
            inner_maze.append(content)
            directions = path_connections.get((x, y), set())
            if cell & Wall.EAST:
                inner_maze.append("│")
            elif "E" in directions:
                inner_maze.append("•")
            else:
                inner_maze.append(" ")
        lines.append("".join(inner_maze))
        if y != len(grid) - 1:
            sep_parts: list[str] = ["├"]
            for x, cell in enumerate(row):
                directions = path_connections.get((x, y), set())
                if cell & Wall.SOUTH:
                    sep_parts.append("───")
                elif "S" in directions:
                    sep_parts.append(" • ")
                else:
                    sep_parts.append("   ")
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
