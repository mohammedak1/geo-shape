import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon

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


