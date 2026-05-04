from Maze.Maze import Maze
from Maze.Cell import Cell


from typing import Union


def get_direction(start: Union[tuple[int, int], Cell], end: Union[tuple[int, int], Cell]) -> str:
    if isinstance(start, Cell):
        start_pos = start.pos
    else:
        start_pos = start

    if isinstance(end, Cell):
        end_pos = end.pos
    else:
        end_pos = end

    x1, y1 = start_pos
    x2, y2 = end_pos
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


def build_path_connections(path: list[Cell]) -> dict[Cell, set[str]]:
    connections: dict[Cell, set[str]] = {}

    for current, next_cell in zip(path, path[1:]):
        direction = get_direction(current, next_cell)
        if current not in connections:
            connections[current] = set()
        if next_cell not in connections:
            connections[next_cell] = set()
        connections[current].add(direction)
        connections[next_cell].add(opposite(direction))
    return connections


def render_maze(maze: Maze, entry: Cell, exit: Cell,
                path: list[Cell] | None = None,
                wall_color: str = "",
                path_color: str = "",
                reset_color: str = "",) -> str:

    lines: list[str] = []
    path_connections = build_path_connections(path) if path else {}
    path_cells = set(path) if path is not None else set()
    grid = maze.maze_lst
    if not grid:
        return ""

    # render top line
    top_parts: list[str] = [f"{wall_color}┌{reset_color}"]
    for x, cell in enumerate(grid[0]):
        top_parts.append(f"{wall_color}───{reset_color}"
                         if cell and cell.n else "   ")
        if x == len(grid[0]) - 1:
            top_parts.append(f"{wall_color}┐{reset_color}")
        else:
            top_parts.append(f"{wall_color}┬{reset_color}")
    lines.append("".join(top_parts))

    # render inner maze
    for y, row in enumerate(grid):
        inner_maze: list[str] = []
        inner_maze.append(f"{wall_color}│{reset_color}"
                          if row[0] and row[0].w else " ")
        for x, cell in enumerate(row):
            cur_cell = maze.get_cell((x, y))
            if cur_cell:
                if cur_cell == entry:
                    content = " E "
                elif cur_cell == exit:
                    content = " X "
                elif cur_cell in path_cells:
                    content = f"{path_color} • {reset_color}"
                else:
                    content = "   "
                inner_maze.append(content)
                directions = path_connections.get(cur_cell, set())
                if cell and cell.e:
                    inner_maze.append(f"{wall_color}│{reset_color}")
                elif "E" in directions:
                    inner_maze.append(f"{path_color}•{reset_color}")
                else:
                    inner_maze.append(" ")
        lines.append("".join(inner_maze))
        if y != len(grid) - 1:
            sep_parts: list[str] = [f"{wall_color}├{reset_color}"]
            for x, cell in enumerate(row):
                cur_cell = maze.get_cell((x, y))
                if cur_cell:
                    directions = path_connections.get(cur_cell, set())
                    if cell and cell.s:
                        sep_parts.append(f"{wall_color}───{reset_color}")
                    elif "S" in directions:
                        sep_parts.append(f"{path_color} • {reset_color}")
                    else:
                        sep_parts.append("   ")
                    if x == len(row) - 1:
                        sep_parts.append(f"{wall_color}┤{reset_color}")
                    else:
                        sep_parts.append(f"{wall_color}┼{reset_color}")
            lines.append("".join(sep_parts))

    # render bottom line
    bottom_parts: list[str] = [f"{wall_color}└{reset_color}"]
    for x, cell in enumerate(grid[-1]):
        bottom_parts.append(f"{wall_color}───{reset_color}"
                            if cell and cell.s else "   ")
        if x == len(grid[-1]) - 1:
            bottom_parts.append(f"{wall_color}┘{reset_color}")
        else:
            bottom_parts.append(f"{wall_color}┴{reset_color}")
    lines.append("".join(bottom_parts))

    return "\n".join(lines)