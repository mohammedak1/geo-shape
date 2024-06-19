import random
from shapely import Polygon, MultiPolygon
from shapely.affinity import translate, rotate
import uuid

class Sample:
    width = 250
    height = 250 
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
    
    def randomize_shapes(self, countries_multi_polygons):
        for country_multi_polygon in countries_multi_polygons:
            shape = Shape(country_multi_polygon)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            c = shape.get_polygon().centroid
            shape.set_pos(x - c.x, y - c.y)
            self.shapes.append(shape)

    def center_shapes(self, target_polygon, countries_multi_polygons):
        for country_multi_polygon in countries_multi_polygons:
            shape = Shape(country_multi_polygon)
            shape.center_to(target_polygon) 
            self.shapes.append(shape)
    
    def copy_with_mutation(self):
        shapes = []
        for shape in self.shapes:
           new_shape = Shape(shape.get_polygon(), shape.angle)
           rate = self.change_rate

           percent = random.randint(1, 100)
           if percent <= 1:
              rate *= 120  
           elif percent <= 2:
              rate *= 60 
           elif percent <= 5:
              rate *= 40 
           elif percent <= 7:
              rate *= 20 
           elif percent <= 12:
              rate *= 5
           else:
              rate = 0
           
           if rate > 0:
               wild_x = random.randint(new_shape.get_x() - rate, new_shape.get_x() + rate)
               wild_y = random.randint(new_shape.get_y() - rate, new_shape.get_y() + rate)

               x = min(self.width ,max(0, wild_x)) 
               y = min(self.height, max(0, wild_y))

               dx =  x - shape.get_polygon().centroid.x
               dy =  y - shape.get_polygon().centroid.y

               new_shape.set_pos(dx, dy)

           angle_percent = random.randint(1, 100)
           angle_change_rate = 0
           if angle_percent <= 1:
               angle_change_rate = 30
           elif angle_percent <= 2:
               angle_change_rate = 15
           elif angle_percent <= 4:
               angle_change_rate = 5
           elif angle_percent <= 9:
               angle_change_rate = 2
            
           if angle_change_rate > 0:
                angle_change = random.randint(-angle_change_rate, angle_change_rate)
                new_angle = shape.angle + angle_change

                new_shape.set_angle(new_angle)
                
           shapes.append(new_shape)
            
        return Sample(self.target_area, shapes)

        


class Shape:
    def __init__(self, multi_polygon, angle=0):
       self.multi_polygon = multi_polygon
       self.angle = angle

    def set_pos(self,x, y):
        self.multi_polygon = translate(self.multi_polygon, xoff=x, yoff=y)

    def set_angle(self, angle):
        self.multi_polygon = rotate(self.multi_polygon, angle, origin='centroid', use_radians=False)
        self.angle = angle

    def center_to(self, target):
        current = self.multi_polygon.centroid
        target = target.centroid

        self.set_pos( target.x - current.x, target.y - current.y) 

    def get_polygon(self):
        return self.multi_polygon

    def get_x(self):
        return int(self.multi_polygon.centroid.x)

    def get_y(self):
        return int(self.multi_polygon.centroid.y)
    