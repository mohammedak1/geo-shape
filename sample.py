import uuid
from shapely import Polygon

class Sample:
    width = 250
    height = 250 

    def __init__(self, shapes=None):
        if shapes is None:
            raise ValueError("Shapes Cant't Be None")

        self.shapes = shapes
        self.id = str(uuid.uuid1())
        
    def get_shapes_as_polygons(self):
        return [Polygon(shape) for shape in self.shapes]