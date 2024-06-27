from shapely import  MultiPolygon, union_all


def fit_function(polygon, shape_polygon) :
    connected_sample_polygons = union_all(polygon)

    intersection = None
    if connected_sample_polygons.geom_type == "Polygon":
        intersection = shape_polygon.intersection(connected_sample_polygons)
        return intersection.area
    intersection = shape_polygon.intersection(connected_sample_polygons.geoms)
    clean = clean_intersection(intersection) 
    return clean.area 

def clean_intersection(intersection):
    res = list(filter(
         lambda polygon: (
             polygon.is_valid and not polygon.is_empty and
             polygon.geom_type not in {
                 "GeometryCollection", "LineString", "Point", 
                 "MultiLineString", "MultiPoint", "MultiPolygon"}
         ), 
         intersection
    ))
    return MultiPolygon(res)