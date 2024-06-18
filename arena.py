import multiprocessing
import matplotlib.pyplot as plt
from sample import Sample
from shapely.ops import unary_union
from matplotlib.patches import Polygon as MplPolygon
from shapes import get_shape_polygon, Countires
import math
import multiprocess as multi
from area import fit_function
from config import SAMPLES_PER_GENERATION, TAKE_TOP

class Arena:
    def __init__(self) -> None:
        self.samples = []
        self.target_polygon = get_shape_polygon("temp/img.png") 
        self.target_area = int(self.target_polygon.area)

        coutnries = Countires(gride_side=250)
        selected = coutnries.arab_countires(self.target_area * 1)
        
        for _ in range(0, SAMPLES_PER_GENERATION):
            sample = Sample(self.target_area)
            sample.center_shapes(self.target_polygon, selected)
            self.samples.append(sample)

    def mutate_closer_to_fittests(self):
        print("Getting top samples")
        top_sampls = self.__get_top_intersections()
        print("Mutating based on top samples")
        self.samples = self.__mutate_based_on_top(top_sampls)
    
    def get_most_fit(self):
        return self.__get_top_intersections()[0]

    def __mutate_based_on_top(self, top_sampls):
        new_samples = [] 
        each_sample_legnth = math.floor(SAMPLES_PER_GENERATION / TAKE_TOP)  
        for i in range(0, TAKE_TOP):
            number_of_sampls = each_sample_legnth
            if i == TAKE_TOP - 1:
               number_of_sampls += SAMPLES_PER_GENERATION % TAKE_TOP

            sample = top_sampls[i]
            for _ in range(0, number_of_sampls):
                mutated_sample = sample.copy_with_mutation()
                new_samples.append(mutated_sample)

        return new_samples

    def __get_top_intersections(self):
        manager =  multi.Manager()
        intersection_areas = manager.dict()
        index_sampls = {}

        procs = []
        number_of_cpus = multiprocessing.cpu_count()
        sampls_clusters = devide_based_on_cpus(number_of_cpus, self.samples)
        for samples in sampls_clusters:
            for sample in samples:
                index_sampls[sample.id] = sample
            proc = multi.Process(target=self.get_top_intersection_multi, args=(samples, self.target_polygon, intersection_areas)) 
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        top = sorted(intersection_areas.items(), key= lambda x: x[1], reverse=True)[:TAKE_TOP] 
        top_ids = list(map(lambda x: x[0], top))
        return list(map(lambda x: index_sampls[x], top_ids)) 

    def get_top_intersection_multi(self,samples, target, areas):
        for sample in samples:
            sample_fit = fit_function(sample, target)
            areas[sample.id] = sample_fit


def devide_based_on_cpus(cpus, samples):
    n = len(samples)
    base_size = n // cpus  

    subarrays = []
    start = 0

    for i in range(cpus):
        if i < cpus - 1:
            end = start + base_size
        else:
            end = n  # Include all remaining elements in the last subarray

        subarrays.append(samples[start:end])
        start = end

    return subarrays
            
        


## N_Samples / N_Threads = 2000 / 8 = 250
## Process Them Then Return Rres as a packages 
