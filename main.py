import multiprocessing
from multiprocessing.dummy import freeze_support
from draw import full_draw, sample_draw, progress_draw
from arena import Arena
from config import NUM_OF_GENERATIONS, TARGET
from dalle_2d_image import get_2d_image

if __name__ == '__main__':
    progress = []
    freeze_support()
    print("CPUS:", multiprocessing.cpu_count())
    #get_2d_image(TARGET) 
    arena = Arena()
    for i in range(1, NUM_OF_GENERATIONS):
        print(f"---------------------------------------")
        arena.pass_one_generation()
        area = int(arena.get_top_area())
        target_area = arena.target_area

        percentage = (area/target_area) * 100
        progress.append(percentage)
        print(f"Generation: {i}  Area: ({area}/ {target_area}) {percentage:.1f}% \n")
    print("DONE")


    most_fit = arena.get_most_fit().get_shapes_as_polygons()
    full_draw(most_fit, arena.target_polygon) 
    sample_draw(most_fit)
    progress_draw(progress)

    
#TODO:
#*. clean the code
#*. create samples
#*. do a blog on it on github
#*. share it with the world
 
 
#Done:
#*. fix a bug in mutation overflow
