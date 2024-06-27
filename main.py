import multiprocessing
from multiprocessing.dummy import freeze_support
from draw import full_draw, sample_draw, progress_draw
from fit import fit_function
from arena import Arena
from config import NUM_OF_GENERATIONS
from shapely import Polygon

if __name__ == '__main__':
    progress = []
    freeze_support()
    print("CPUS:", multiprocessing.cpu_count())
    #get_2d_image(TARGET) 
    arena = Arena()
    for i in range(1, NUM_OF_GENERATIONS):
        arena.pass_one_generation()
        area = int(arena.get_top_area())
        target_area = arena.target_area

        percentage = (area/target_area) * 100
        progress.append(percentage)
        print(f"Generation: {i}  Area: ({area}/ {target_area}) {percentage:.1f}%")
    print("DONE")


    most_fit = arena.get_most_fit().get_shapes_as_polygons()
    full_draw(most_fit, arena.target_polygon) 
    sample_draw(most_fit)
    progress_draw(progress)

    
#TODO:
#1. center the shapes to take a head start
#2. take the values from the coutnries and pased them as a single polygon
#3. clean the code
#4. create samples
#5. do a blog on it on github
#6. share it with the world