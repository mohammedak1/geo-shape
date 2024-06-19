from shapely import  MultiPolygon, union_all


def fit_function(sample, shape_polygon) :
    sample_polygons = sample.get_shapes_polygons()
    connected_sample_polygons = union_all(sample_polygons)

    intersection = None
    if connected_sample_polygons.geom_type == "Polygon":
        intersection = shape_polygon.intersection(connected_sample_polygons)
        return intersection.area
    intersection = shape_polygon.intersection(connected_sample_polygons.geoms)
    clean = clean_intersection(intersection) 
    return clean.area 

def clean_intersection(intersection):
    res = []
    for polygon in intersection:
        if ( polygon.is_valid and not polygon.is_empty and
             polygon.geom_type != "GeometryCollection" and
             polygon.geom_type != "LineString"  and 
             polygon.geom_type != "Point" and
             polygon.geom_type != "MultiLineString" and 
             polygon.geom_type != "MultiPoint" and 
             polygon.geom_type != "MultiPolygon"
           ):
             res.append(polygon)
    return MultiPolygon(res)