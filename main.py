
import time
from astar import astar
from visualization import visualize_maze


# ══════════════════════════════════════════════════════════════════
#   MAZE CONFIGURATION
#   0 = Empty Cell  |  1 = Wall
# ══════════════════════════════════════════════════════════════════

maze = [
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
]

start = (0, 0)
goal  = (6, 6)


# ══════════════════════════════════════════════════════════════════
#   CONSOLE HELPERS
# ══════════════════════════════════════════════════════════════════

def _separator(char="═", width=52, color="\033[94m"):
    RESET = "\033[0m"
    print(f"{color}{char * width}{RESET}")


def _header():
    B  = "\033[1m"          # bold
    C  = "\033[96m"         # cyan
    Y  = "\033[93m"         # yellow
    R  = "\033[0m"          # reset

    _separator("═", 52, "\033[94m")
    print(f"\033[94m║{R}  {B}{C}  A* Maze Solver  —  Professional Edition   {R}\033[94m║{R}")
    print(f"\033[94m║{R}  {Y}  Heuristic: Manhattan Distance               {R}\033[94m║{R}")
    _separator("═", 52, "\033[94m")
    print()


def _print_maze(maze, start, goal):
    WALL  = "\033[47m\033[30m  W  \033[0m"
    EMPTY = "\033[100m\033[37m  .  \033[0m"
    START = "\033[42m\033[30m  S  \033[0m"
    GOAL  = "\033[41m\033[37m  G  \033[0m"

    print("  \033[90mMaze Layout:\033[0m")
    for r, row in enumerate(maze):
        print("  ", end="")
        for c, cell in enumerate(row):
            if (r, c) == start:
                print(START, end="")
            elif (r, c) == goal:
                print(GOAL, end="")
            elif cell == 1:
                print(WALL, end="")
            else:
                print(EMPTY, end="")
        print()
    print()


def _print_path(path):
    G = "\033[92m"
    R = "\033[0m"
    B = "\033[1m"
    Y = "\033[93m"

    print(f"  {B}{G}Path Coordinates:{R}")
    line = "  "
    for i, node in enumerate(path):
        line += f"{Y}{node}{R}"
        if i < len(path) - 1:
            line += f" {G}→{R} "
        if len(line) > 72:
            print(line)
            line = "  "
    if line.strip():
        print(line)
    print()


def _print_stats(path, explored, elapsed_ms):
    B  = "\033[1m"
    C  = "\033[96m"
    Y  = "\033[93m"
    G  = "\033[92m"
    R  = "\033[0m"
    DIM = "\033[90m"

    _separator("─", 52, "\033[90m")
    print(f"  {B}{C}Results{R}")
    _separator("─", 52, "\033[90m")

    rows = len(maze)
    cols = len(maze[0])
    walls = sum(cell for row in maze for cell in row)

    stats = [
        ("Grid Size",        f"{rows} × {cols}"),
        ("Total Cells",      f"{rows * cols}"),
        ("Wall Cells",       f"{walls}"),
        ("Free Cells",       f"{rows * cols - walls}"),
        ("Explored Nodes",   f"{len(explored)}"),
        ("Path Steps",       f"{len(path) - 1}" if path else "N/A"),
        ("Path Efficiency",  f"{(len(path)-1)/len(explored)*100:.1f}%" if path else "N/A"),
        ("Execution Time",   f"{elapsed_ms:.3f} ms"),
    ]

    for label, value in stats:
        pad = 22 - len(label)
        print(f"  {DIM}{label}{R}{' ' * pad}{B}{Y}{value}{R}")

    _separator("─", 52, "\033[90m")
    print()


# ══════════════════════════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    _header()

    # Print maze layout
    _print_maze(maze, start, goal)

    print(f"  \033[90mRunning A* Search…\033[0m")
    print()

    # ── Run A* ────────────────────────────────────────────────────
    t0 = time.perf_counter()
    path, explored = astar(maze, start, goal)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    # ── Print Results ─────────────────────────────────────────────
    if path:
        print(f"  \033[1m\033[92m✔  Path Found Successfully!\033[0m")
        print()
        _print_path(path)
    else:
        print(f"  \033[1m\033[91m✘  No Path Found — Goal is Unreachable.\033[0m")
        print()

    _print_stats(path, explored, elapsed_ms)

    # ── Launch Visualizer ─────────────────────────────────────────
    print("  \033[96mLaunching animated visualizer…\033[0m")
    _separator("═", 52, "\033[94m")
    print()

    visualize_maze(maze, start, goal, path, explored)


if __name__ == "__main__":
    main()
