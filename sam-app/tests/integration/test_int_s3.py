import unittest
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from infrastructure.repository.S3 import S3


class S3IntTests(unittest.TestCase):
    def test_should_remove_object(self):
        # Arrange
        subject = S3()
        subject.put_object("twilio-apps", "integration_delete_text.txt", "junk data")

        # Act
        results = subject.delete_object("twilio-apps", "integration_delete_text.txt")
        print(f"test results: {results}")

        # Assert
        self.assertEqual(results, "")


if __name__ == "__main__":
    unittest.main()
