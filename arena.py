import multiprocessing
from sample import Sample
from shapely.ops import unary_union
from matplotlib.patches import Polygon as MplPolygon
from shapes import get_shape_polygon, Countires
import math
import multiprocess as multi
from fit import fit_function
from config import SAMPLES_PER_GENERATION, TAKE_TOP
import numpy as np
from shapely import Polygon, MultiPolygon
from scipy.spatial import ConvexHull
from joblib import Parallel, delayed
import time

class Arena:
    def __init__(self):
        self.target_polygon = get_shape_polygon("temp/img.png") 
        self.target_area = int(self.target_polygon.area)

        coutnries = Countires(gride_side=250)
        selected = coutnries.all_countries(self.target_area)
        
        samples = []
        for _ in range(0, SAMPLES_PER_GENERATION):
            seq = np.zeros(shape=(58, 5, 2),  dtype=np.int32,)  
            side = 20
            seq[:, 0, 0] = 140 #(x1)
            seq[:, 0, 1] = 100 #(y1)

            seq[:, 1, 0] = 140 #(x1)
            seq[:, 1, 1] = 100 + side #(y1)

            seq[:, 2, 0] = 140 + side #(x1)
            seq[:, 2, 1] = 100 + side #(y1)

            seq[:, 3, 0] = 140 + side #(x1)
            seq[:, 3, 1] = 100 #(y1)

            seq[:, 4, 0] = 140 #(x1)
            seq[:, 4, 1] = 100 #(y1)

            samples.append(seq)
        self.samples = np.array(samples)
        self.top_area = 0

    def pass_one_generation(self):
        print("Mutiting")
        self.__mutate()
        print("Eliminting")
        self.__update_if_found_better()

    def __mutate(self):
        shape = self.samples.shape
        mutations = np.random.randint(-4000, 2, size=(shape[0], shape[1], shape[3]))
        mutations =  np.where(mutations < -2, 0, np.clip(mutations, -2, 2))
        big_mutations = np.random.randint(-12000, 40, size=(shape[0], shape[1], shape[3]))
        big_mutations =  np.where(big_mutations < -40, 0, np.clip(big_mutations, -40, 40))
        self.temp_samples = self.samples + mutations[:, :, np.newaxis, :] + big_mutations[:, :, np.newaxis, :]

        x_overflow_max_pos = np.where(self.temp_samples[:, :, :, 0] > 250)
        x_overflow_min_pos = np.where(self.temp_samples[:, :, :, 0] < 0)
        y_overflow_max_pos = np.where(self.temp_samples[:, :, :, 1] > 250)
        y_overflow_min_pos = np.where(self.temp_samples[:, :, :, 1] < 0)

        self.temp_samples[x_overflow_max_pos[0], x_overflow_max_pos[1], :, 0] -= 20
        self.temp_samples[x_overflow_min_pos[0], x_overflow_min_pos[1], :, 0] += 20
        self.temp_samples[y_overflow_max_pos[0], y_overflow_max_pos[1], :, 1] -= 20
        self.temp_samples[y_overflow_min_pos[0], y_overflow_min_pos[1], :, 1] += 20

        
    def __update_if_found_better(self):
        init_mill = time.time() * 1000
        areas = Parallel(n_jobs=-1)(delayed(self._evaluate_sample)(sample) for sample in self.temp_samples)
        areas = np.array(areas) 

        after_mill = time.time() * 1000

        print("Time taken to evaluate", int(after_mill - init_mill), " ms")
        top_n_indices = np.argpartition(-areas, TAKE_TOP)[:TAKE_TOP]
        top_n_areas = areas[top_n_indices]

        arrays = []
        shape = self.temp_samples.shape
        for index in top_n_indices:
            sample = self.temp_samples[index]
            arrays.append(np.full((shape[0] // TAKE_TOP, shape[1], shape[2], shape[3]), sample))
        if np.mean(top_n_areas) > self.top_area:
            self.top_area = np.mean(top_n_areas)
            self.samples = np.concatenate(arrays)
        

    def _evaluate_sample(self, sample):
        polygons = list(map(lambda x: Polygon(x), sample)) 
        return fit_function(polygons, self.target_polygon)

    def get_most_fit(self):
        most = 0
        sample = None
        for value in self.samples:
            area = self._evaluate_sample(value)
            if area > most:
                sample = value
                most = area
        return Sample(sample)

    def get_top_area(self):
        return self.top_area