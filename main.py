import multiprocessing
from multiprocessing.dummy import freeze_support
from shapes import full_draw, sample_draw, Countires
from area import fit_function
from arena import Arena
from dalle_2d_image import get_2d_image
import multiprocess as multi


if __name__ == '__main__':
    freeze_support()
    print("CPUS:", multiprocessing.cpu_count())
    #get_2d_image("cat playing with a ball") 
    arena = Arena()
    for i in range(1, 5):
        arena.mutate_closer_to_fittests()
        sample = arena.get_most_fit()
        target_area = arena.target_area

        area = int(fit_function(sample, arena.target_polygon))
        percentage = (area/target_area) * 100
        print(f"Generation: {i}  Area: ({area}/ {target_area}) {percentage:.1f}%")
    print("DONE")

    most_fit = arena.get_most_fit().get_shapes_polygons()
    full_draw(most_fit, arena.target_polygon) 
    sample_draw(most_fit)