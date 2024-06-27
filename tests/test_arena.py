import unittest
from arena import Arena


class TEST_ARENA(unittest.TestCase):
    def test_mutate(self):
        print("hello")
        a = Arena() 
        for i in range(1, 3):
            print("generation", i)
            a.pass_one_generation()
        print(a.get_top_area())
        
        