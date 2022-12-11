"""
Example test.
"""

import unittest


class ExampleTester(unittest.TestCase):
    """Example tester."""

    def test_example(self) -> None:
        """Example tester."""
        alwaystrue = True
        self.assertTrue(alwaystrue, "This should always be true.")


if __name__ == '__main__':
    unittest.main()
