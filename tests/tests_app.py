import unittest
from IRC import app


class TestStringMethods(unittest.TestCase):

    def test_channel(self):
        self.assertEqual(app.channel("aaa"), "#aaa")


if __name__ == '__main__':
    unittest.main()
