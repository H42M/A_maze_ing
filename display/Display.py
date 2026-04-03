"""Display class management."""


from maze import Maze


class Display:
    """Manage the maze display."""

    @classmethod
    def print_maze(cls, maze_obj: Maze) -> None:
        """Print current maze.

        Example:
            >>> maze.print_maze()
        """
        maze = maze_obj.maze_list
        FOND_VERT = "\033[42m"
        FOND_ROUGE = "\033[41m"
        FOND_BLEU = "\033[44m"
        RESET = "\033[0m"

        for y, col in enumerate(maze):
            for x, cell in enumerate(col):
                if cell.n:
                    print("████", end="")
                else:
                    print(FOND_BLEU + "    " + RESET, end="")
            print()
            for x, cell in enumerate(col):
                if cell.w:
                    print("█", end="")
                else:
                    print(" ", end="")
                if x == maze_obj.entry.x and y == maze_obj.entry.y:
                    color = FOND_ROUGE
                elif x == maze_obj.exit.x and y == maze_obj.exit.y:
                    color = FOND_VERT
                elif maze_obj.get_cell(x, y).visited:
                    color = FOND_BLEU
                else:
                    color = RESET
                print(color + "  " + RESET, end="")
                if cell.e:
                    print("█", end="")
                else:
                    print(" ", end="")
            print()
            for x, cell in enumerate(col):
                if cell.s:
                    print("████", end="")
                else:
                    print(FOND_BLEU + "    " + RESET, end="")
            print()

    @classmethod
    def print_maze_v2(cls, maze_obj: 'Maze') -> None:
        """Print current maze with box-drawing characters and ANSI colours.

        Example:
        >>> maze.print_maze()
        """
        maze = maze_obj.maze_list
        height = len(maze)
        width = len(maze[0]) if height else 0
        ex, ey = maze_obj.entry.pos
        xx, xy = maze_obj.exit.pos

        # ── Couleurs ANSI ────────────────────────────────────────────────────
        R = "\033[0m"
        WALL = "\033[90m"        # gris sombre  → murs
        ENTRY = "\033[1;37;41m"   # blanc gras / fond rouge   → départ
        EXIT_C = "\033[1;37;42m"   # blanc gras / fond vert    → arrivée
        VISITED = "\033[34;40m"     # bleu / fond noir          → chemin visité

        # ── Prédicats de murs ────────────────────────────────────────────────
        def h_wall(r: int, c: int) -> bool:
            """Mur horizontal au-dessus de la rangée r, colonne c."""
            if r == 0 or r == height:
                return True
            return bool(maze[r][c].n)

        def v_wall(r: int, c: int) -> bool:
            """Mur vertical à gauche de la colonne c, rangée r."""
            if c == 0 or c == width:
                return True
            return bool(maze[r][c].w)

        # ── Caractère de coin selon les segments connectés ───────────────────
        _CORNER = {
            (0, 0, 0, 0): " ",
            (1, 0, 0, 0): "╵", (0, 1, 0, 0): "╶",
            (0, 0, 1, 0): "╷", (0, 0, 0, 1): "╴",
            (1, 1, 0, 0): "└", (1, 0, 1, 0): "│", (1, 0, 0, 1): "┘",
            (0, 1, 1, 0): "┌", (0, 1, 0, 1): "─", (0, 0, 1, 1): "┐",
            (1, 1, 1, 0): "├", (1, 1, 0, 1): "┴",
            (1, 0, 1, 1): "┤", (0, 1, 1, 1): "┬",
            (1, 1, 1, 1): "┼",
        }

        def corner(r: int, c: int) -> str:
            u = v_wall(r - 1, c) if r > 0 else False
            d = v_wall(r,     c) if r < height else False
            le = h_wall(r, c - 1) if c > 0 else False
            ri = h_wall(r,     c) if c < width else False
            return _CORNER.get((int(u), int(ri), int(d), int(le)), "?")

        # ── Contenu de cellule (3 caractères) ───────────────────────────────
        def cell_str(x: int, y: int) -> str:
            if x == ex and y == ey:
                return ENTRY + " S " + R
            if x == xx and y == xy:
                return EXIT_C + " E " + R
            if maze_obj.get_cell(x, y).visited:
                return " · " + R
                # return VISITED + " · " + R

            return "   "

        # ── Rendu ────────────────────────────────────────────────────────────
        lines: list[str] = []
        for r in range(height + 1):
            # Ligne de séparation (murs horizontaux)
            row = WALL
            for c in range(width):
                row += corner(r, c) + ("───" if h_wall(r, c) else "   ")
            row += corner(r, width) + R
            lines.append(row)

            if r < height:
                # Ligne de cellules (murs verticaux + contenu)
                row = ""
                for c in range(width):
                    row += WALL + ("│" if v_wall(r, c) else " ") + R
                    row += cell_str(c, r)
                row += WALL + ("│" if v_wall(r, width) else " ") + R
                lines.append(row)

        # Légende
        lines.append(
            f"\n  {ENTRY} S {R} Départ   "
            f"{EXIT_C} E {R} Arrivée   "
            f"{VISITED} · {R} Visité"
        )
        print("\n".join(lines))

    @classmethod
    def print_maze_2(cls, maze_obj: Maze) -> None:
        """Print current maze.

        Example:
            >>> maze.print_maze()
        """
        maze = maze_obj.maze_list
        FOND_VERT = "\033[42m"
        FOND_ROUGE = "\033[41m"
        RESET = "\033[0m"

        for y, col in enumerate(maze):
            for x, cell in enumerate(col):
                if cell.n:
                    print("┏━━┓", end="")
            print()
            for x, cell in enumerate(col):
                if cell.w:
                    print("┃", end="")
                if x == maze_obj.entry[0] and y == maze_obj.entry[1]:
                    color = FOND_ROUGE
                elif x == maze_obj.exit[0] and y == maze_obj.exit[1]:
                    color = FOND_VERT
                else:
                    color = RESET
                print(color + "  " + RESET, end="")
                if cell.e:
                    print("┃", end="")
            print()
            for x, cell in enumerate(col):
                if cell.s:
                    print("┗━━┛", end="")
            print()
