import unittest
import irc


class TestStringMethods(unittest.TestCase):

    def test_channel(self):
        self.assertEqual(irc.channel("aaa"), "#aaa")


if __name__ == '__main__':
    unittest.main()
