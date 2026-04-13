*This activity has been created as part of the 42 curriculum by ngaubil, hgeorges*

# A-Maze-ing

> *"A labyrinth is not a place to be lost, but a path to be found."*

A random maze generator written in Python, featuring visual rendering, generation, resolution, and an embedded **42 logo** hidden inside every maze.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration File](#configuration-file)
- [Output Format](#output-format)
- [Project Structure](#project-structure)
- [Algorithms](#algorithms)
- [Development](#development)

---
This activity has been created as part of
the 42 curriculum by
## Overview

A-Maze-ing generates random mazes from a configuration file and outputs them in a hexadecimal wall-encoded format. Each cell encodes its walls (North, South, East, West) as a single hex digit. Mazes can be **perfect** (single path between entry and exit) or **imperfect** (multiple paths). A visual representation is displayed in the terminal, and a stylized **"42"** pattern is always embedded in the maze.

---

## Features

- **Random maze generation** with reproducible seeds
- **Perfect maze** support (unique path between entry and exit)
- **pathfinding** to resolve the maze
- **Terminal visual rendering** with optional step-by-step animation
- **Embedded "42" logo** composed of fully closed cells
- **Hexadecimal output file** encoding wall states per cell
- **Fully configurable** via a plain-text config file

---

## Requirements

- Python **3.10** or later
- Dependencies listed in `requirements.txt`

---

## Installation

```bash
# Install dependencies
make install
```

---

## Usage

```bash
python3 a_maze_ing.py config.txt
```

or

```bash
make run 
```

| Argument     | Description                              |
|--------------|------------------------------------------|
| `config.txt` | Path to your configuration file          |

**Examples:**

```bash
# Run with default config
make run

# Lint the project
make lint
```

---

## Configuration File

The configuration file uses `KEY=VALUE` pairs, one per line. Lines starting with `#` are treated as comments.

```ini
# Maze dimensions
WIDTH=20
HEIGHT=15

# Entry and exit coordinates (x,y)
ENTRY=0,0
EXIT=19,14

# Output file
OUTPUT_FILE=output.txt

# Perfect maze (single path between entry and exit)
PERFECT=True
```

### Mandatory keys

| Key           | Description                        | Example          |
|---------------|------------------------------------|------------------|
| `WIDTH`       | Number of columns                  | `WIDTH=20`       |
| `HEIGHT`      | Number of rows                     | `HEIGHT=15`      |
| `ENTRY`       | Entry cell coordinates `(x,y)`     | `ENTRY=0,0`      |
| `EXIT`        | Exit cell coordinates `(x,y)`      | `EXIT=19,14`     |
| `OUTPUT_FILE` | Name of the output file            | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | Whether the maze is perfect        | `PERFECT=True`   |

A default `config.txt` is included in the repository.

---

## Output Format

Each cell is encoded as a **single hexadecimal digit** representing which walls are closed, using bitmask values:

| Wall  | Bit | Value |
|-------|-----|-------|
| North | 0   | 1     |
| East  | 1   | 2     |
| South | 2   | 4     |
| West  | 3   | 8     |

A cell with all 4 walls closed has value `8 + 4 + 2 + 1 = 15` → `F`.  
A cell open to the South and West has value `1 + 2` → `3`.

**Example output (`maze.txt`):**
```
F9F3F6...
...
```

---

## Project Structure

```
a-maze-ing/
├── a_maze_ing.py          # Entry point
├── config/
│   └── Config.py          # Config file parser
│   └── ConfigChecker.py   # Config Validity Checker
├── maze/
│   ├── Maze.py            # Maze class (generation, resolution, display)
│   └── Cell.py            # Cell class (walls, state)
├── algo/
│   ├── Dfs.py             # DFS-based maze builder and resolver
│   └── A_Star.py          # A* pathfinding algorithm
├── display/
│   └── Display.py         # Terminal rendering
├── Logs.py                # Logging manager
├── Errors.py              # Custom exceptions
├── config.txt             # Default configuration file
├── Makefile               # Automation rules
├── requirements.txt       # Python dependencies
└── README.md
```

---

## Algorithms

### Generation — Depth-First Search (DFS)

The maze is built using a **recursive backtracker** (DFS). Starting from the entry cell, the algorithm carves passages by visiting unvisited neighbors randomly until all cells have been visited. This guarantees a **spanning tree** — i.e., a perfect maze with exactly one path between any two cells.

When `PERFECT=False`, random walls are additionally broken to create multiple paths, while respecting the 2-cell corridor width limit and preserving the 42 pattern.

### Resolution — A\*

The maze is solved using the **A\* algorithm**, which finds the shortest path from entry to exit using a heuristic (Manhattan distance). The solution path is stored and can be displayed or exported as a direction string (`N`, `S`, `E`, `W`).

---

## Development

```bash
# Remove caches and temporary files
make clean

# Run linting (flake8 + mypy)
make lint

# Run strict linting (optional)
make lint-strict
```

### Code Standards

- Style: **flake8**
- Type checking: **mypy** with `--warn-return-any --warn-unused-ignores --disallow-untyped-defs --check-untyped-defs`
- Docstrings: **PEP 257** (Google style)
- All functions include **type hints**

---

## License

This project is part of the **42 Association** curriculum.  
All rights reserved — see [legal@42.fr](mailto:legal@42.fr) for usage inquiries.