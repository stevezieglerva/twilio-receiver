import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch


class S3RepoUnitTests(unittest.TestCase):
    def test_should_save_reminder(self):
        # Arrange
        subject = Class()

        # Act
        results = subject.method()
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
