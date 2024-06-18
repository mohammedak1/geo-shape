import cv2
from sample import Sample
import matplotlib.pyplot as plt
import numpy as np
import copy
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
            name = value['name']
            geo_shape = value["geo_shape"] 
            geo_metray = geo_shape["geometry"]
            coords = geo_metray["coordinates"]

            multi_polygon_coords = self.__coords_to_multipolygon(coords)
            if len(multi_polygon_coords) == 1:
                self.polygons[name] = MultiPolygon(multi_polygon_coords)
            else:
                self.polygons[name] = MultiPolygon(multi_polygon_coords)
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

            all_coords = []
            for polygon in multi_polygon.geoms:
                all_coords.extend(polygon.exterior.coords)
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
            
            normlized_polygons = [] 
            for polygon in multi_polygon.geoms:
                 coords = polygon.exterior.coords
                 np_coords = np.array(coords)
                 np_coords[:, 0] = ((np_coords[:, 0] - min_long) / long_range) * x_scale
                 np_coords[:, 1] = ((np_coords[:, 1] - min_lat) / lat_range) * y_scale
                 
                 normlized_polygons.append(Polygon(np_coords))

            self.polygons[country] = MultiPolygon(normlized_polygons)

    def get_scaled_countries(self, names, target_area):
        areas = np.array(list(map(lambda country: self.areas[country], names)))
        slice_areas = dict(zip(names, areas / areas.sum()))

        scaled_countries = []
        for name in names: 
            multi_polygon_country = self.polygons[name]
            current = multi_polygon_country.area
            desired = slice_areas[name] * target_area 
            factor = (desired / current) ** 0.5 
            changed = scale(multi_polygon_country, factor, factor)
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
     

def full_draw(sample_shapes_ployes, shape_poly):
    fig, ax = plt.subplots(constrained_layout=True)

    all_polyes = []
    for multi_polygon in sample_shapes_ployes:
       for poly in multi_polygon.geoms:
           all_polyes.append(poly)
           x, y = poly.exterior.xy
           ax.fill(x, y, alpha=0.5, fc='lightblue', edgecolor='blue', label='')
    
    if shape_poly.geom_type == "MultiPolygon":
        for poly in shape_poly.geoms:
            x, y = poly.exterior.xy 
            ax.fill(x, y, alpha=0.5, fc='lightcoral', edgecolor='red', label='')
        all_polyes += shape_poly.geoms
    else:
        x, y = shape_poly.exterior.xy
        ax.fill(x, y, alpha=0.5, fc='lightcoral', edgecolor='red', label='')
        all_polyes += [shape_poly]
    
    minx, miny, maxx, maxy = MultiPolygon(all_polyes).bounds
    ax.set_xlim(minx - 10, maxx + 10)
    ax.set_ylim(miny - 10, maxy + 10)
    ax.set_aspect('equal')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygons Visualization')
    plt.legend()
    plt.grid(True)
    plt.savefig("temp/res_full.png")

def sample_draw(sample_shapes_ployes):
    plt.close('all')
    fig, ax = plt.subplots(constrained_layout=True)
    gemos = []
    for multi_poly in sample_shapes_ployes:
        for poly in multi_poly.geoms:
            x, y = poly.exterior.xy
            ax.fill(x, y, alpha=0.5, fc='lightblue', edgecolor='blue', label='')
        gemos += multi_poly.geoms


    minx, miny, maxx, maxy = MultiPolygon(gemos).bounds
    ax.set_xlim(minx - 10, maxx + 10)
    ax.set_ylim(miny - 10, maxy + 10)
    ax.set_aspect('equal')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygons Visualization')
    plt.legend()
    plt.grid(True)
    plt.savefig("temp/res_sample.png")


        
def progress_draw(progress):
    plt.close('all')
    plt.plot(progress)
    plt.xlabel('Generation')
    plt.ylabel('Percentage')
    plt.savefig("temp/progress.png")