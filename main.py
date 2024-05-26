
from shapes import full_draw, sample_draw, Countires
from area import fit_function
from arena import Arena
from dalle_2d_image import get_2d_image


arena = Arena()
full_draw(arena.samples[0].get_shapes_polygons(), arena.target_polygon) 
for i in range(1, 6):
    arena.mutate_closer_to_fittests()
    sample = arena.get_most_fit()
    target_area = arena.target_area
    most_fit = arena.get_most_fit().get_shapes_polygons()
    full_draw(most_fit, arena.target_polygon) 

    area = fit_function(sample, arena.target_polygon)
    print(f"Generation: {i} Area: ({area}/ {target_area})")
print("DONE")

most_fit = arena.get_most_fit().get_shapes_polygons()
full_draw(most_fit, arena.target_polygon) 
sample_draw(most_fit)