import random
from shapely.affinity import translate, rotate
import uuid
import numpy as np
from shapely import Polygon, MultiPolygon


class Sample:
    width = 250
    height = 250 
    change_rate = 1

    def __init__(self, shapes=None):
        if shapes is None:
            raise ValueError("Shapes Cant't Be None")

        self.shapes = shapes
        self.id = str(uuid.uuid1())
        
    def get_shapes_as_polygons(self):
        return [Polygon(shape) for shape in self.shapes]
    
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
        shapes = np.copy(self.shapes)
        length = len(shapes)
        x_translate = np.random.uniform(-2, 2, length).astype(np.int32)
        y_translate = np.random.uniform(-2, 2, length).astype(np.int32)

        shapes[:, :, 0] += x_translate[:, np.newaxis]
        shapes[:, :, 1] += y_translate[:, np.newaxis]

        shapes[:, :, 0] = np.clip(shapes[:, :, 0], 0, 255)
        shapes[:, :, 1] = np.clip(shapes[:, :, 1], 0, 255)
        print(shapes[:, :, 0])


        return Sample(shapes)

class Shape:
    def __init__(self, multi_polygon, angle=0):
       print("shape", multi_polygon.shape)
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
    