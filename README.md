
# Maze Solver Using A* Search Algorithm

## 1. Project Overview

Maze Solver Using A* Search is an Artificial Intelligence
project that finds the shortest path between a starting
point and a goal in a grid-based maze.

The project uses the A* Search algorithm and Manhattan
Distance heuristic to navigate around obstacles.

## 2. Objectives

- Understand informed search algorithms.
- Implement A* Search using Python.
- Represent a maze using a 2D grid.
- Find the shortest possible path.
- Visualize explored nodes and the final path.
- Handle unreachable destinations.

## 3. Technologies Used

- Python
- Matplotlib
- NumPy
- VS Code

## 4. Project Features

- 2D Grid Maze Representation
- Start and Goal Positions
- Obstacle Detection
- A* Search Implementation
- Manhattan Distance Heuristic
- Shortest Path Calculation
- No Path Detection
- Animated Maze Visualization
- Execution Time Measurement
- Explored Nodes Statistics
- Automated Unit Testing

## 5. A* Search Formula

f(n) = g(n) + h(n)

Where:

- g(n): Actual cost from the start node.
- h(n): Estimated cost to the goal.
- f(n): Total estimated path cost.

## 6. Maze Representation

- 0 represents an empty cell.
- 1 represents a wall.
- Start represents the initial position.
- Goal represents the destination.

## 7. Installation

Install Python 3.

Install project dependencies:

pip install -r requirements.txt

## 8. How to Run

Execute the following command:

python main.py

## 9. Run Automated Tests

python -m unittest test_astar -v

## 10. Visualization Legend

- Black: Walls
- White: Empty cells
- Green: Start
- Red: Goal
- Light Blue: Explored nodes
- Blue: Shortest path

## 11. Expected Output

The program displays:

- Whether a path was found.
- The shortest path coordinates.
- Total path length.
- Number of explored nodes.
- Execution time.
- Animated maze visualization.

## 12. Conclusion

This project demonstrates how the A* Search algorithm
solves pathfinding problems using an informed search
strategy and heuristic estimation.

It provides practical understanding of AI search
algorithms, path optimization, and visualization.
