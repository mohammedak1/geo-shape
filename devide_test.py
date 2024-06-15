import unittest
from arena import devide_based_on_cpus


class TEST_DEVIDE(unittest.TestCase):
    def test_devide(self):
        res1 = devide_based_on_cpus(2, [1, 2, 3, 4, 5, 6])
        self.assertEqual([[1, 2, 3], [4, 5, 6]], res1)

        res2 = devide_based_on_cpus(3, [1, 2, 3, 4, 5, 6])
        self.assertEqual([[1, 2], [3,4], [5, 6]], res2)

        res3 = devide_based_on_cpus(3, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual([[1, 2], [3, 4], [5, 6, 7]], res3)


if __name__ == '__main__':
    unittest.main()


        