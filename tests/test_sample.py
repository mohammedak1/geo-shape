import unittest
from sample import Sample
import numpy as np
from countries import get_shape_polygon
from fit import fit_function

class TEST(unittest.TestCase):
    def testMutation(self):
        seq = np.zeros(shape=(100, 5, 2),  dtype=np.int32,)  
        seq[:, 0, 0] = 150 #(x)
        seq[:, 0, 1] = 150 #(y)

        seq[:, 1, 0] = 150 #(x)
        seq[:, 1, 1] = 155 #(y)

        seq[:, 2, 0] = 155 #(x)
        seq[:, 2, 1] = 155 #(y)

        seq[:, 3, 0] = 155 #(x)
        seq[:, 3, 1] = 150 #(y)

        t = get_shape_polygon("temp/img.png") 
        fit_map = {}
        for i in range(100):
            s = Sample(seq).copy_with_mutation()
            fit = fit_function(s, t)        
            fit_map[s.id] = fit
        
        least = float('inf')
        most = float('-inf')
        for key in fit_map.keys():
            value = fit_map[key]
            if value < least:
                least = value
            if value > most:
                most = value


        print("least", least)
        print("most", most)
        
         

