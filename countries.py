import cv2
from sample import Sample
import numpy as np
import json
from shapely import Polygon, MultiPolygon
from shapely.affinity import scale

class Countires:
    def __init__(self, gride_side: int = None):
        self.grid_side_length = gride_side

        self.polygons = {}
        self.areas = {}
        file = open("countries.json", "r")
        content = json.load(file)
        for value in content:
            if not is_country_accepted(value['name']):
                continue    
            name = value['name']
            geo_shape = value["geo_shape"] 
            geo_metray = geo_shape["geometry"]
            coords = geo_metray["coordinates"]

            multi_polygon_coords = self.__coords_to_multipolygon(coords)
            polygons = list(multi_polygon_coords)
            biggest_area = 0
            chosen_polygon = None
            for polygon in polygons:
                area = polygon.area
                if area > biggest_area:
                    biggest_area = area
                    chosen_polygon = polygon
            self.polygons[name] = chosen_polygon
            
        self.__normlize() 
        file.close()  

    def __coords_to_multipolygon(self, coords):
        if not isinstance(coords[0][0], list):
            return [Polygon(coords)]
        
        polygones = [] 
        for c in coords:
            polygones += self.__coords_to_multipolygon(c)
        
        return polygones

    def __normlize(self):
        for country, multi_polygon in self.polygons.items():
            self.areas[country] = multi_polygon.area
            
            all_coords = multi_polygon.exterior.coords
            np_array = np.array(all_coords)

            long = np_array[:, 0]
            lat = np_array[:, 1]

            min_long, max_long = long.min(), long.max()
            min_lat, max_lat = lat.min(), lat.max()

            long_range = max_long - min_long
            lat_range = max_lat - min_lat

            aspect_ratio = long_range / lat_range

            if aspect_ratio > 1:
                x_scale = self.grid_side_length
                y_scale = self.grid_side_length / aspect_ratio
            else:
                y_scale = self.grid_side_length
                x_scale = self.grid_side_length * aspect_ratio
            
            coords = multi_polygon.exterior.coords
            np_coords = np.array(coords)
            np_coords[:, 0] = ((np_coords[:, 0] - min_long) / long_range) * x_scale
            np_coords[:, 1] = ((np_coords[:, 1] - min_lat) / lat_range) * y_scale

            self.polygons[country] = Polygon(np_coords)

    def get_scaled_countries(self, names, target_area):
        areas = np.array(list(map(lambda country: self.areas[country], names)))
        slice_areas = dict(zip(names, areas / areas.sum()))

        scaled_countries = []
        for name in names: 
            country_polygon = self.polygons[name]
            current = country_polygon.area
            desired = slice_areas[name] * target_area 
            factor = (desired / current) ** 0.5 
            changed = scale(country_polygon, factor, factor)
            coords_count = len(changed.exterior.coords)
            scaled_countries.append(changed) 
        
        return scaled_countries

    def arab_countires(self, target_area):
        arab_countries = [
         "Morocco",
         "Algeria",
         "Sudan",
         "Oman",
         "Syrian Arab Republic",
         "Yemen",
         "Western Sahara",
         "United Arab Emirates",
         "Kuwait",
         "Bahrain",
         "Somalia",
         "West Bank",
         "Saudi Arabia",
         "Egypt",
         "Jordan",
         "Qatar",
         "Gaza Strip",
         "Lebanon",
         "Mauritania",
         "Tunisia",
         "Iraq",
        ]

        return self.get_scaled_countries(arab_countries, target_area)

    def get_all_countires(self, target_area):
        names = list(self.polygons.keys())
        return self.get_scaled_countries(names, target_area)
            

def get_shape_polygon(image_path):
    shape = img_to_shape(image_path) 
    return shape_to_polygon(shape)
    

def img_to_shape(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE) 
    image = cv2.rotate(image, cv2.ROTATE_180 )
    resized_image = cv2.resize(image, (Sample.width, Sample.height))
    _, binary = cv2.threshold(resized_image, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    binary_image = np.zeros_like(image)
    cv2.drawContours(binary_image, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    return binary_image

def shape_to_polygon(binary_image):
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    polygons = []
    for contour in contours:
        if len(contour) > 2:  
            contour = contour.squeeze()
            polygon = Polygon(contour)
            polygons.append(polygon)
    if (len(polygons) == 0):
        raise ValueError("Polygons is empty")
    if len(polygons) > 1:
        return MultiPolygon(polygons)
    elif polygons:
        return polygons[0]
     

def is_country_accepted(country):
    #relax those not accepted because they are too big and have too many coordinates
    if country in ["Russian Federation", "Greenland", "Canada"]:
        return False
    return True