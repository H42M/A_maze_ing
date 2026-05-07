*This activity has been created as part of the 42 curriculum by ngaubil, hgeorges.*

# A-Maze-ing

A-Maze-ing is a Python maze generator and visualizer. It reads a plain-text configuration file, generates a valid maze, displays it visually, writes the maze to a hexadecimal output file, and exposes the generator logic through a reusable pip-installable module named `mazegen`.

## Description

The goal of this activity is to generate random mazes while keeping the generated data coherent and reusable. Each maze is made of cells with walls on the four cardinal directions: North, East, South, and West. The final output file stores each cell as one hexadecimal digit, where each bit represents one closed wall.

The project supports both perfect and imperfect mazes. A perfect maze has exactly one path between the entry and the exit. An imperfect maze keeps the maze connected but opens additional walls to create loops and multiple valid paths.

The project also provides visual rendering. The terminal version shows the maze, the entry, the exit, and optionally the shortest solution path. A Pygame version is also available with buttons, themes, and a movable player.

## Features

- Random maze generation from a configuration file.
- Reproducible generation with a seed.
- Perfect maze generation using Depth-First Search / recursive backtracking.
- Optional imperfect maze generation by opening extra coherent walls.
- Entry and exit validation.
- Fully closed external borders.
- Coherent wall encoding between neighboring cells.
- Shortest path solving from entry to exit.
- Hexadecimal output file compatible with the subject format.
- Visible `42` pattern made from fully closed cells when the maze is large enough.
- Terminal rendering with optional solution display, animation, and wall color changes.
- Pygame rendering with theme selection, regeneration, solution toggle, and player movement.
- Standalone reusable `mazegen.py` module.
- Buildable Python package producing a `mazegen-*` wheel or source archive.

## Requirements

- Python 3.10 or later.
- A virtual environment is recommended.
- Project dependencies are listed in `requirements.txt`.

The main dependencies used by the complete activity are:

```text
flake8
mypy
pygame
pydantic
```

The standalone reusable `mazegen` package itself has no third-party runtime dependency.

## Instructions

### Install dependencies

From the root of the repository:

```bash
make install
```

This creates `.venv`, upgrades `pip`, and installs the dependencies from `requirements.txt`.

### Run the activity

The required subject command is:

```bash
python3 a_maze_ing.py config.txt
```

You can also use:

```bash
make run
```

The program expects exactly one argument: the path to a configuration file.

### Debug

```bash
make debug
```

This runs the main script with Python's built-in debugger.

### Clean generated files

```bash
make clean
```

This removes Python cache folders and mypy cache folders.

For a deeper cleanup, including the virtual environment and generated maze output:

```bash
make fclean
```

### Lint and type-check

```bash
make lint
```

This runs:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

An optional stricter target is also available:

```bash
make lint-strict
```

### Build the reusable package

The reusable generator package is built from the root-level `mazegen.py` module and `pyproject.toml`.

```bash
make package
```

This builds the package and copies the wheel to the root of the repository. After building, the root of the repository should contain a file named like:

```text
mazegen-1.0.0-py3-none-any.whl
```

The build may also create files inside `dist/`, such as:

```text
dist/mazegen-1.0.0-py3-none-any.whl
dist/mazegen-1.0.0.tar.gz
```

Both `.whl` and `.tar.gz` are valid Python build artifacts. The important file for review is the root-level `mazegen-*` package file.

Manual build command:

```bash
.venv/bin/python -m pip install --upgrade build
.venv/bin/python -m build
cp dist/mazegen-*.whl .
```

### Test the reusable package in a clean virtual environment

```bash
python3 -m venv package_test_env
package_test_env/bin/python -m pip install ./mazegen-1.0.0-py3-none-any.whl
package_test_env/bin/python - <<'PY'
from mazegen import MazeGenerator

generator = MazeGenerator(width=10, height=8, entry=(0, 0), exit=(9, 7), seed=42)
generator.generate()

print(generator.to_hex_rows())
print(generator.solution)
print(generator.solution_moves)
PY
```

## Configuration file

The configuration file is a plain-text file using one `KEY=VALUE` pair per line.

Rules:

- Empty lines are ignored.
- Lines starting with `#` are ignored as comments.
- Spaces around keys and values are allowed.
- Coordinates use the format `x,y`.
- All mandatory keys must be present.

Complete structure:

```ini
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Mandatory keys

| Key | Type | Format | Description | Example |
| --- | --- | --- | --- | --- |
| `WIDTH` | Integer | `WIDTH=<number>` | Maze width in cells. Must be greater than 3 and at most 200. | `WIDTH=20` |
| `HEIGHT` | Integer | `HEIGHT=<number>` | Maze height in cells. Must be greater than 3 and at most 200. | `HEIGHT=15` |
| `ENTRY` | Coordinate | `ENTRY=x,y` | Entry cell coordinates. Must be inside the maze. | `ENTRY=0,0` |
| `EXIT` | Coordinate | `EXIT=x,y` | Exit cell coordinates. Must be inside the maze and different from entry. | `EXIT=19,14` |
| `OUTPUT_FILE` | String | `OUTPUT_FILE=<path>` | File where the hexadecimal maze output is written. | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Boolean | `PERFECT=True` or `PERFECT=False` | Generates a perfect maze when true, and an imperfect maze when false. | `PERFECT=True` |

A default/example `config.txt` is provided at the root of the repository.

## Output file format

The output file starts with the maze grid. Each cell is encoded as one hexadecimal digit representing its closed walls.

| Direction | Bit | Decimal value |
| --- | --- | --- |
| North | 0 | 1 |
| East | 1 | 2 |
| South | 2 | 4 |
| West | 3 | 8 |

Examples:

- `F` means all four walls are closed: `1 + 2 + 4 + 8 = 15`.
- `3` means North and East walls are closed: `1 + 2 = 3`.
- `A` means East and West walls are closed: `2 + 8 = 10`.

Rows are written from top to bottom, one line per maze row.

After the grid, the file contains an empty line followed by:

1. Entry coordinates.
2. Exit coordinates.
3. The shortest valid path from entry to exit using `N`, `E`, `S`, and `W`.

Example shape:

```text
FFFFFFFF
F...maze rows...
FFFFFFFF

0,0
7,7
EESSWWNN
```

All lines end with a newline character.

## Visual representation

The project provides two visual modes.

### Terminal mode

The terminal display is available from the main menu after running:

```bash
python3 a_maze_ing.py config.txt
```

Available menu actions:

| Option | Action |
| --- | --- |
| `0` | Re-generate a new random maze. |
| `1` | Re-generate a new maze with a user-provided seed. |
| `2` | Show or hide the solution path. |
| `3` | Enable or disable animation speed. |
| `4` | Rotate wall colors. |
| `5` | Open the Pygame visualizer. |
| `6` | Quit. |

### Pygame mode

The Pygame visualizer includes buttons to:

- show or hide the solution;
- generate a new maze;
- choose a visual theme.

The player can be moved with the arrow keys while respecting wall collisions.

## Maze generation algorithm

The main generation algorithm is Depth-First Search using the recursive backtracker strategy, implemented iteratively.

The generation starts from the entry cell. At each step, it chooses a random unvisited neighbor, opens the wall between the current cell and that neighbor, and continues from the neighbor. When no unvisited neighbor is available, it backtracks until another unvisited neighbor can be found. This continues until all walkable cells have been visited.

The `42` pattern cells are treated as blocked cells. They remain fully closed and are skipped by the generation algorithm. If the maze is too small, if the pattern overlaps the entry or exit, or if the pattern would disconnect the maze, the pattern is omitted and a warning is displayed.

When `PERFECT=True`, the resulting maze is kept as a spanning tree, which means there is exactly one path between any two walkable cells.

When `PERFECT=False`, the program opens additional walls after the DFS generation. These extra openings create loops and multiple possible paths while keeping neighboring wall encodings coherent.

## Why this algorithm was chosen

Depth-First Search / recursive backtracking was chosen because:

- it is simple to explain during review;
- it naturally produces perfect mazes;
- it is easy to make reproducible with a random seed;
- it works well with an animated generation display;
- it maps cleanly to the cell-and-wall representation used by the project;
- it can skip the fully closed `42` pattern cells without changing the whole architecture.

For solving, the main project uses A* with Manhattan distance to find a shortest path from entry to exit.

## Reusable code and package

The reusable part of this project is the root-level file:

```text
mazegen.py
```

It contains a standalone `MazeGenerator` class that can be imported by another Python project without importing the terminal renderer, Pygame renderer, menu system, or configuration parser.

The package is configured by:

```text
pyproject.toml
```

The package name is:

```text
mazegen
```

The generated build artifact is named like:

```text
mazegen-1.0.0-py3-none-any.whl
```

### Basic reusable usage

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15)
generator.generate()

print(generator.structure)
print(generator.solution)
print(generator.solution_moves)
```

### Custom parameters

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit=(29, 19),
    seed=1234,
    perfect=True,
)
generator.generate()
```

Available constructor parameters:

| Parameter | Description |
| --- | --- |
| `width` | Maze width in cells. |
| `height` | Maze height in cells. |
| `entry` | Entry coordinate as `(x, y)`. Defaults to `(0, 0)`. |
| `exit` | Exit coordinate as `(x, y)`. Defaults to the bottom-right cell. |
| `seed` | Optional random seed for reproducible generation. |
| `perfect` | Keeps exactly one path when true. Opens extra walls when false. |
| `include_logo_42` | Reserves fully closed cells shaped like `42` when possible. |
| `extra_open_probability` | Controls how many extra walls may be opened when `perfect=False`. |

### Accessing generated data

After calling `generate()`, the reusable generator exposes:

| Attribute or method | Return type | Description |
| --- | --- | --- |
| `structure` | `list[list[int]]` | The generated maze as a copied 2D grid of wall bitmasks. |
| `solution` | `list[tuple[int, int]]` | The shortest path as coordinates from entry to exit. |
| `solution_moves` | `str` | The shortest path as `N`, `E`, `S`, `W` moves. |
| `to_hex_rows()` | `list[str]` | The maze as hexadecimal text rows. |
| `to_output_text()` | `str` | A subject-style output string containing rows, entry, exit, and solution. |
| `logo_cells` | `set[tuple[int, int]]` | Coordinates reserved for the `42` pattern. |
| `warnings` | `list[str]` | Non-fatal warnings, such as a maze being too small for the `42` pattern. |

The reusable structure does not depend on the output file format, but it uses the same wall bitmask values for convenience.

## Project structure

```text
.
├── a_maze_ing.py              # Main required entry point
├── config.txt                 # Default/example configuration file
├── Makefile                   # Install, run, debug, lint, clean, package targets
├── pyproject.toml             # Python package build configuration for mazegen
├── mazegen.py                 # Standalone reusable generator module
├── test_mazegen.py            # Small package usage test
├── requirements.txt           # Development and runtime dependencies
├── Config/                    # Config parsing, validation, game state, themes
├── Maze/                      # Main project maze model, DFS generation, A* solving, output
├── render/                    # Pygame rendering components
├── player/                    # Pygame player movement and collision
├── srcs/                      # Theme assets
├── terminal_maze.py           # Terminal generation and rendering workflow
└── pygame_maze.py             # Pygame visualizer workflow
```

## Advanced features

The project includes several features beyond basic file generation:

- Terminal menu workflow.
- Animated terminal generation.
- Solution path toggle.
- Wall color rotation.
- Pygame graphical display.
- Theme selection through `Config/themes.json`.
- Player movement with wall collision.
- Reusable pip-installable generator module.

## Team and project management

### Team roles

- `hgeorges`: maze generation/refinement, configuration validation fixes, terminal workflow, output format checks, `42` logo edge cases, reusable `mazegen` module, packaging, lint/build checks.
- `ngaubil`: Pygame visual rendering, UI/buttons, theme management, seed display, output integration, animation behavior, initial README structure, project integration fixes.

Both team members worked on debugging, merging branches, cleaning style issues, and keeping the implementation aligned with the subject requirements.

### Initial planning

The project was planned in stages:

1. Build a working maze model and generator.
2. Parse and validate the configuration file.
3. Export the maze in the required hexadecimal format.
4. Add a visual representation.
5. Add interactions: regeneration, solution toggle, and colors.
6. Add the `42` pattern constraint.
7. Clean lint/type issues and improve error handling.
8. Add the reusable `mazegen` package and documentation.

### How the planning evolved

The implementation started with the core maze model and terminal output because these were the safest mandatory requirements to validate. Pygame rendering and themes were then added as a richer visual layer. Near the end, the project was adjusted to better match the reusability requirement by extracting a clean standalone `mazegen.py` module and adding `pyproject.toml` packaging support.

### What worked well

- The cell wall model made output encoding straightforward.
- DFS generation was easy to animate and explain.
- A* solving gave a clear shortest path for display and export.
- The menu made subject-required interactions easy to access.
- Keeping `mazegen.py` standalone made the reusable module simpler and safer to install.

### What could be improved

- The reusable package could eventually become the single source of truth for both the main project and external users.
- More automated tests could be added for edge cases, such as very small mazes, invalid configurations, and impossible `42` logo placement.
- The Pygame code could be further separated from maze logic to reduce coupling.
- The Makefile package target could be adjusted to build directly at the root with `python -m build --outdir .`.

### Tools used

- Git and GitHub for version control and branch merging.
- Python virtual environments for dependency isolation.
- `flake8` for style checks.
- `mypy` for static type checking.
- `pydantic` for configuration validation.
- `pygame` for graphical rendering.
- Standard Python packaging tools: `pyproject.toml`, `setuptools`, `wheel`, and `build`.
- VS Code for development.
- AI assistance for subject interpretation, compliance checking, packaging guidance, reusable-module refactoring guidance, and README drafting. AI-generated suggestions were reviewed, tested, and adapted before inclusion.

## Resources

Classic references and documentation used or useful for this project:

- Python documentation: https://docs.python.org/3/
- Python `venv` documentation: https://docs.python.org/3/library/venv.html
- Python packaging guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- PyPA `build` documentation: https://build.pypa.io/en/stable/
- setuptools documentation: https://setuptools.pypa.io/
- Pygame documentation: https://www.pygame.org/docs/
- Pydantic documentation: https://docs.pydantic.dev/
- Flake8 documentation: https://flake8.pycqa.org/
- Mypy documentation: https://mypy.readthedocs.io/
- Maze generation reference: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Depth-First Search reference: https://en.wikipedia.org/wiki/Depth-first_search
- A* search algorithm reference: https://en.wikipedia.org/wiki/A*_search_algorithm

## License and subject context

This project was created for the 42 curriculum. The subject material belongs to Association 42. This repository contains the implementation produced for the activity.
