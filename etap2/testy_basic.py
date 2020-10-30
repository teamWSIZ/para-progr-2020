import math
import unittest


def add(a, b):
    return a + b


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(add(2, 2), 4, "Dodawanie liczb dodatnich działa")

    def test_with_negative(self):
        self.assertEqual(add(2, -2), 0, "Dodawanie liczb ujemnych jest ok")

    def test_with_large_numbers(self):
        self.assertEqual(add(2 * 10 ** 10, -2 * 10 ** 10), 0, "Should add huge numbers")

    def test_with_fractions(self):
        self.assertEqual(add(0.007, 0.003), 0.01, "Should add fractions")

    def test_with_strings(self):
        self.assertEqual(add('aaa', 'bbb'), 'aaabbb', "Should add strings")

    def test_with_NaN(self):
        self.assertTrue(math.isnan(add(float('nan'), 1)), 'Adding 1 to NaN produces NaN')


if __name__ == '__main__':
    unittest.main()
