import unittest
from arena import Arena
from shapely import MultiPolygon, Polygon


class TEST_ARENA(unittest.TestCase):
    def test_total_area_should_not_change(self):
        a = Arena()
        area_before = MultiPolygon([Polygon(p) for p in a.samples[0]]).area 
        print(area_before)
        
        for _ in range(1, 1000):
            a.pass_one_generation()
        
        area_after = MultiPolygon([Polygon(p) for p in a.samples[0]]).area
        
        print("before", area_before, "after", area_after)
        self.assertEqual(area_before, area_after)

         
        
        