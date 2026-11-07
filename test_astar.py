
import unittest

from astar import astar


class TestAStarSearch(unittest.TestCase):

    def test_simple_path(self):
        maze = [
            [0, 0],
            [0, 0]
        ]

        path, explored = astar(maze, (0, 0), (1, 1))

        self.assertIsNotNone(path)
        self.assertEqual(len(path) - 1, 2)

    def test_wall_avoidance(self):
        maze = [
            [0, 1, 0],
            [0, 0, 0]
        ]

        path, explored = astar(maze, (0, 0), (0, 2))

        self.assertIsNotNone(path)

        for row, col in path:
            self.assertEqual(maze[row][col], 0)

    def test_no_path(self):
        maze = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0]
        ]

        path, explored = astar(maze, (0, 0), (2, 2))

        self.assertIsNone(path)

    def test_start_equals_goal(self):
        maze = [
            [0, 0],
            [0, 0]
        ]

        path, explored = astar(maze, (0, 0), (0, 0))

        self.assertEqual(path, [(0, 0)])

    def test_invalid_start(self):
        maze = [
            [1, 0],
            [0, 0]
        ]

        with self.assertRaises(ValueError):
            astar(maze, (0, 0), (1, 1))


if __name__ == "__main__":
    unittest.main()
