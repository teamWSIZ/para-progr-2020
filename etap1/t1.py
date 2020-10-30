import unittest

from etap2.klasy_extend import TeslaUser


class TestSum(unittest.TestCase):
    def setUp(self):
        self.u = TeslaUser('aa','11','x')
        print('preparing test')

    def tearDown(self):
        print('finishing test')


    def test_sum(self):
        print(f'test list {self.u.name}')
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        print('test tuple')
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")

if __name__ == '__main__':
    unittest.main()
