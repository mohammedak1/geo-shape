import matplotlib.pyplot as plt
from sample import Sample
from shapely.ops import unary_union
from matplotlib.patches import Polygon as MplPolygon
from shapes import get_shape_polygon, Countires
import math
import multiprocessing as multi
from area import fit_function

class Arena:
    samples_per_generation = 20
    take_top = 3
    def __init__(self) -> None:
        self.samples = []
        self.target_polygon = get_shape_polygon("temp/img.png") 
        self.target_area = int(self.target_polygon.area)

        coutnries = Countires(250)
        selected = coutnries.get_scaled_countries(["Iraq", "Iran (Islamic Republic of)", "United Arab Emirates"], self.target_area)
        
        for _ in range(0, self.samples_per_generation):
            sample = Sample(self.target_area)
            sample.center_shapes(self.target_polygon, selected)
            self.samples.append(sample)

    def mutate_closer_to_fittests(self):
        top_sampls = self.__get_top_intersections()
        self.samples = self.__mutate_based_on_top(top_sampls)
    
    def get_most_fit(self):
        return self.__get_top_intersections()[0]

    def __mutate_based_on_top(self, top_sampls):
        new_samples = [] 
        each_sample_legnth = math.floor(self.samples_per_generation / self.take_top)  
        for i in range(0, self.take_top):
            number_of_sampls = each_sample_legnth
            if i == self.take_top - 1:
               number_of_sampls += self.samples_per_generation % self.take_top 

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
        for sample in self.samples:
            index_sampls[sample.id] = sample
            proc = multi.Process(target=self.__get_top_intersection_multi, args=(sample, self.target_polygon, intersection_areas)) 
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        top = sorted(intersection_areas.items(), key= lambda x: x[1], reverse=True)[:self.take_top] 
        top_ids = list(map(lambda x: x[0], top))
        return list(map(lambda x: index_sampls[x], top_ids)) 

    def __get_top_intersection_multi(self,sample, target, areas):
        sample_fit = fit_function(sample, target)
        areas[sample.id] = sample_fit
