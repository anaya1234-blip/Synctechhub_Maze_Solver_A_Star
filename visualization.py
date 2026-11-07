
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.gridspec as gridspec


# ─────────────────────────── Color Palette ────────────────────────────────── #
DARK_BG        = "#0d1117"
PANEL_BG       = "#161b22"
WALL_COLOR     = "#21262d"
EMPTY_COLOR    = "#1c2128"
GRID_COLOR     = "#30363d"
START_COLOR    = "#3fb950"
GOAL_COLOR     = "#f85149"
EXPLORED_START = "#1f6feb"
EXPLORED_END   = "#58a6ff"
PATH_COLOR     = "#ffd700"
PATH_GLOW      = "#ffec6e"
TEXT_PRIMARY   = "#e6edf3"
TEXT_SECONDARY = "#8b949e"
ACCENT         = "#58a6ff"
ACCENT_2       = "#bc8cff"
SUCCESS_COLOR  = "#3fb950"
FAIL_COLOR     = "#f85149"
# ──────────────────────────────────────────────────────────────────────────── #


def _make_explored_cmap():
    """Create a gradient colormap for explored nodes."""
    return LinearSegmentedColormap.from_list(
        "explored_grad",
        [EXPLORED_START, EXPLORED_END, "#79c0ff"],
        N=256
    )


def _draw_cell(ax, row, col, color, alpha=1.0, radius=0.38, zorder=3):
    """Draw a rounded rectangle cell on the grid."""
    rect = FancyBboxPatch(
        (col - radius, row - radius),
        2 * radius, 2 * radius,
        boxstyle="round,pad=0.04",
        linewidth=0,
        facecolor=color,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_patch(rect)
    return rect


def _draw_marker(ax, row, col, color, symbol, size=18, zorder=10):
    """Draw a labeled circle marker (Start / Goal)."""
    circle = Circle(
        (col, row), 0.42,
        facecolor=color, zorder=zorder, linewidth=2,
        edgecolor="white"
    )
    ax.add_patch(circle)
    ax.text(
        col, row, symbol,
        ha="center", va="center",
        fontsize=size, fontweight="bold",
        color="white", zorder=zorder + 1,
        path_effects=[
            pe.withStroke(linewidth=3, foreground="black")
        ]
    )
    return circle


def visualize_maze(maze, start, goal, path, explored_order):
    """
    Professional animated A* maze visualizer.

    Phases:
      1. Fade-in of the maze grid.
      2. Animated exploration (node-by-node, blue gradient).
      3. Animated shortest path drawing (gold trail with glow).
      4. Final freeze with stats overlay.

    Parameters
    ----------
    maze          : 2-D list   (0 = empty, 1 = wall)
    start         : (row, col)
    goal          : (row, col)
    path          : list of (row, col) or None
    explored_order: list of (row, col)
    """

    grid = np.array(maze, dtype=float)
    rows, cols = grid.shape

    # ── Layout ────────────────────────────────────────────────────────────── #
    fig = plt.figure(figsize=(14, 9), facecolor=DARK_BG)
    fig.canvas.manager.set_window_title("A* Maze Solver — Professional Visualizer")

    gs = gridspec.GridSpec(
        2, 2,
        figure=fig,
        width_ratios=[3, 1],
        height_ratios=[1, 10],
        hspace=0.06,
        wspace=0.08,
        left=0.04, right=0.97,
        top=0.96, bottom=0.04,
    )

    ax_title  = fig.add_subplot(gs[0, :])   # top banner
    ax_maze   = fig.add_subplot(gs[1, 0])   # main maze
    ax_info   = fig.add_subplot(gs[1, 1])   # right info panel

    for ax in (ax_title, ax_maze, ax_info):
        ax.set_facecolor(DARK_BG)
        for spine in ax.spines.values():
            spine.set_visible(False)

    # ── Title Banner ──────────────────────────────────────────────────────── #
    ax_title.set_xlim(0, 1)
    ax_title.set_ylim(0, 1)
    ax_title.axis("off")

    # Gradient title text
    ax_title.text(
        0.5, 0.65,
        "A* Maze Solver",
        ha="center", va="center",
        fontsize=26, fontweight="bold",
        color=TEXT_PRIMARY,
        transform=ax_title.transAxes,
        path_effects=[pe.withStroke(linewidth=6, foreground=ACCENT + "55")]
    )
    ax_title.text(
        0.5, 0.18,
        "Pathfinding with Manhattan Distance Heuristic  ·  "
        f"Grid: {rows}×{cols}  ·  "
        f"Start: {start}  ·  Goal: {goal}",
        ha="center", va="center",
        fontsize=10,
        color=TEXT_SECONDARY,
        transform=ax_title.transAxes,
    )

    # Decorative accent line under banner
    ax_title.axhline(0.0, color=ACCENT, linewidth=1.5, alpha=0.5)

    # ── Maze Background ───────────────────────────────────────────────────── #
    ax_maze.set_xlim(-0.5, cols - 0.5)
    ax_maze.set_ylim(rows - 0.5, -0.5)
    ax_maze.set_aspect("equal")
    ax_maze.axis("off")

    # Draw base cells
    for r in range(rows):
        for c in range(cols):
            color = WALL_COLOR if grid[r, c] == 1 else EMPTY_COLOR
            _draw_cell(ax_maze, r, c, color, alpha=1.0, zorder=1)

    # Subtle grid lines
    for x in np.arange(-0.5, cols, 1):
        ax_maze.axvline(x, color=GRID_COLOR, linewidth=0.5, zorder=2)
    for y in np.arange(-0.5, rows, 1):
        ax_maze.axhline(y, color=GRID_COLOR, linewidth=0.5, zorder=2)

    # Fixed start / goal markers (always visible)
    _draw_marker(ax_maze, start[0], start[1], START_COLOR, "S", zorder=10)
    _draw_marker(ax_maze, goal[0],  goal[1],  GOAL_COLOR,  "G", zorder=10)

    # ── Right Info Panel ──────────────────────────────────────────────────── #
    ax_info.set_xlim(0, 1)
    ax_info.set_ylim(0, 1)
    ax_info.axis("off")

    # Panel background box
    panel_bg = FancyBboxPatch(
        (0.04, 0.0), 0.92, 0.98,
        boxstyle="round,pad=0.02",
        linewidth=1,
        edgecolor=GRID_COLOR,
        facecolor=PANEL_BG,
        zorder=0,
        transform=ax_info.transAxes,
    )
    ax_info.add_patch(panel_bg)

    # Legend section
    legend_items = [
        (WALL_COLOR,     "■", "Wall"),
        (EMPTY_COLOR,    "■", "Empty Cell"),
        (START_COLOR,    "●", "Start Node"),
        (GOAL_COLOR,     "●", "Goal Node"),
        (EXPLORED_END,   "■", "Explored"),
        (PATH_COLOR,     "─", "Shortest Path"),
    ]

    ax_info.text(
        0.5, 0.95, "LEGEND",
        ha="center", va="top", fontsize=11,
        fontweight="bold", color=ACCENT,
        transform=ax_info.transAxes
    )

    for i, (color, sym, label) in enumerate(legend_items):
        y = 0.88 - i * 0.075
        ax_info.text(
            0.12, y, sym,
            ha="center", va="center",
            fontsize=14, color=color,
            transform=ax_info.transAxes
        )
        ax_info.text(
            0.22, y, label,
            ha="left", va="center",
            fontsize=9, color=TEXT_PRIMARY,
            transform=ax_info.transAxes
        )

    # Divider
    ax_info.plot(
        [0.06, 0.94], [0.44, 0.44],
        color=GRID_COLOR, linewidth=1,
        transform=ax_info.transAxes, clip_on=False
    )

    # Stats section header
    ax_info.text(
        0.5, 0.42, "STATISTICS",
        ha="center", va="top", fontsize=11,
        fontweight="bold", color=ACCENT,
        transform=ax_info.transAxes
    )

    stat_labels = [
        ("Grid Size",      f"{rows} × {cols}"),
        ("Total Cells",    f"{rows * cols}"),
        ("Wall Cells",     f"{int(grid.sum())}"),
        ("Free Cells",     f"{rows * cols - int(grid.sum())}"),
        ("Start",          str(start)),
        ("Goal",           str(goal)),
    ]

    for i, (label, value) in enumerate(stat_labels):
        y = 0.36 - i * 0.062
        ax_info.text(
            0.1, y, label + ":",
            ha="left", va="center",
            fontsize=8, color=TEXT_SECONDARY,
            transform=ax_info.transAxes
        )
        ax_info.text(
            0.9, y, value,
            ha="right", va="center",
            fontsize=8, color=TEXT_PRIMARY, fontweight="bold",
            transform=ax_info.transAxes
        )

    # Dynamic stats (updated during animation)
    ax_info.text(
        0.5, -0.01, "RESULTS",
        ha="center", va="top", fontsize=11,
        fontweight="bold", color=ACCENT_2,
        transform=ax_info.transAxes
    )

    # Result text objects (mutable)
    txt_explored = ax_info.text(
        0.1, -0.075, "Explored: 0",
        ha="left", va="center",
        fontsize=8.5, color=TEXT_PRIMARY,
        transform=ax_info.transAxes
    )
    txt_path_len = ax_info.text(
        0.1, -0.135, "Path Length: —",
        ha="left", va="center",
        fontsize=8.5, color=TEXT_PRIMARY,
        transform=ax_info.transAxes
    )
    txt_phase = ax_info.text(
        0.1, -0.195, "Phase: Initializing…",
        ha="left", va="center",
        fontsize=8.5, color=ACCENT,
        transform=ax_info.transAxes
    )

    # ── Status Bar (bottom of maze) ───────────────────────────────────────── #
    status_text = ax_maze.text(
        (cols - 1) / 2, rows - 0.05,
        "⚙  Initializing A* Search…",
        ha="center", va="bottom",
        fontsize=10, fontweight="bold",
        color=TEXT_SECONDARY, zorder=20
    )

    # ── Animation Data Prep ───────────────────────────────────────────────── #
    visible_explored = [
        node for node in explored_order
        if node != start and node != goal
    ]
    final_path = path if path else []

    n_explored   = len(visible_explored)
    n_path       = len(final_path)

    # Frames breakdown:
    #   [0 .. n_explored-1]              → exploration phase
    #   [n_explored .. n_explored+n_path-1] → path drawing phase
    #   n_explored + n_path              → final freeze frame
    total_frames = max(1, n_explored + n_path + 1)

    # Pre-create explored cell patches (hidden initially)
    explored_cmap   = _make_explored_cmap()
    explored_patches = []
    for idx, (r, c) in enumerate(visible_explored):
        t = idx / max(1, n_explored - 1)
        rgba = explored_cmap(t)
        patch = _draw_cell(ax_maze, r, c, rgba, alpha=0.0, zorder=3)
        explored_patches.append(patch)

    # Path line (drawn segment by segment)
    path_line, = ax_maze.plot(
        [], [], color=PATH_COLOR,
        linewidth=3.5, zorder=6,
        solid_capstyle="round",
        solid_joinstyle="round"
    )
    # Glow duplicate
    path_glow, = ax_maze.plot(
        [], [], color=PATH_GLOW,
        linewidth=7, alpha=0.25, zorder=5,
        solid_capstyle="round",
        solid_joinstyle="round"
    )
    # Path node dots
    path_dots = ax_maze.scatter(
        [], [], color=PATH_COLOR,
        s=55, zorder=7, edgecolors="white", linewidths=0.8
    )

    # ── Update Function ───────────────────────────────────────────────────── #
    def update(frame):

        # ── Phase 1: Exploration ─────────────────────────────────────────── #
        if frame < n_explored:
            patch = explored_patches[frame]
            patch.set_alpha(0.88)

            status_text.set_text(
                f"🔍  Exploring…  Node {frame + 1} / {n_explored}"
            )
            status_text.set_color(EXPLORED_END)
            txt_explored.set_text(f"Explored: {frame + 1}")
            txt_phase.set_text("Phase: Exploring")
            txt_phase.set_color(EXPLORED_END)

        # ── Phase 2: Path Drawing ─────────────────────────────────────────── #
        elif frame < n_explored + n_path:
            path_idx = frame - n_explored + 1
            current_path = final_path[:path_idx]

            xs = [c for r, c in current_path]
            ys = [r for r, c in current_path]

            path_line.set_data(xs, ys)
            path_glow.set_data(xs, ys)
            if xs:
                path_dots.set_offsets(list(zip(xs, ys)))

            # Highlight current head node
            if path_idx < n_path:
                hx, hy = final_path[path_idx]
                _draw_cell(
                    ax_maze, hx, hy,
                    PATH_COLOR, alpha=0.6, radius=0.42, zorder=5
                )

            status_text.set_text(
                f"✨  Drawing Path…  Step {path_idx} / {n_path}"
            )
            status_text.set_color(PATH_COLOR)
            txt_path_len.set_text(f"Path Length: {path_idx}")
            txt_phase.set_text("Phase: Drawing Path")
            txt_phase.set_color(PATH_COLOR)

        # ── Phase 3: Final Frame ──────────────────────────────────────────── #
        else:
            if final_path:
                xs = [c for r, c in final_path]
                ys = [r for r, c in final_path]
                path_line.set_data(xs, ys)
                path_glow.set_data(xs, ys)
                path_dots.set_offsets(list(zip(xs, ys)))

                status_text.set_text(
                    f"✅  Shortest Path Found!  "
                    f"{n_path - 1} steps  |  {n_explored} nodes explored"
                )
                status_text.set_color(SUCCESS_COLOR)
                txt_path_len.set_text(f"Path Length: {n_path - 1}")
                txt_phase.set_text("Phase: Complete ✓")
                txt_phase.set_color(SUCCESS_COLOR)
            else:
                status_text.set_text(
                    f"❌  No Path Found!  {n_explored} nodes explored."
                )
                status_text.set_color(FAIL_COLOR)
                txt_phase.set_text("Phase: No Path ✗")
                txt_phase.set_color(FAIL_COLOR)

            txt_explored.set_text(f"Explored: {n_explored}")

        return (
            *explored_patches,
            path_line, path_glow, path_dots,
            status_text, txt_explored, txt_path_len, txt_phase
        )

    # ── Run Animation ─────────────────────────────────────────────────────── #
    anim = FuncAnimation(
        fig,
        update,
        frames=total_frames,
        interval=120,          # ms per frame  (smooth ~8 fps exploration)
        repeat=False,
        blit=False,
    )

    fig.tight_layout(pad=0.5)
    plt.show()

    return anim
