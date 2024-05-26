import random
from shapely import Polygon, MultiPolygon
from shapely.affinity import translate
import uuid

class Sample:
    width = 250
    height = 250 
    shapes_count = 70
    change_rate = 1

    def __init__(self, target_area , shapes=None):
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes
        self.id = str(uuid.uuid1())
        self.target_area = target_area
        
    def get_shapes_polygons(self):
        return list(map(lambda x: x.get_polygon(), self.shapes))

    def center_shapes(self, target_polygon, countries_multi_polygons):
        for country_multi_polygon in countries_multi_polygons:
            shape = Shape(country_multi_polygon)
            shape.center_to(target_polygon) 
            print("x", shape.get_x(), "y", shape.get_y())
            self.shapes.append(shape)
    
    def copy_with_mutation(self):
        shapes = []
        for shape in self.shapes:
           rate = self.change_rate

           percent = random.randint(1, 100)
           if percent <= 1:
             rate *= 5  
           elif percent <= 3:
             rate *= 2 
           elif percent <= 5:
             rate *= 1 
           else:
               rate = 0 
              
           x = min(self.width ,max(0, random.randint(shape.get_x() - rate, shape.get_x() + rate))) 
           y = min(self.height, max(0, random.randint(shape.get_y() - rate, shape.get_y() + rate)))

           shape.set_pos(x, y)
           shapes.append(shape)
        return Sample(self.target_area, shapes)

        


class Shape:
    def __init__(self, multi_polygon):
       self.multi_polygon  = multi_polygon

    def set_pos(self,x, y):
        self.multi_polygon = translate(self.multi_polygon, xoff=x, yoff=y)

    def center_to(self, target):
        center = target.centroid
        self.set_pos(center.x, center.y) 

    def get_polygon(self):
        return self.multi_polygon

    def get_x(self):
        return int(self.multi_polygon.centroid.x)

    def get_y(self):
        return int(self.multi_polygon.centroid.y)