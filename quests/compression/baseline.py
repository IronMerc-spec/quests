import itertools
import random
from typing import List

import numpy as np


def random_sample(
    descriptors: List[np.ndarray], entropies: np.ndarray, size: int
) -> List[int]:
    indices = np.arange(len(descriptors)).tolist()
    selected = random.sample(indices, size)
    return selected


def mean_fps(
    descriptors: List[np.ndarray], entropies: np.ndarray, size: int
) -> List[int]:
    import fpsample

    avg_descriptors = np.array([x.mean(0) for x in descriptors])
    selected = fpsample.bucket_fps_kdtree_sampling(avg_descriptors, size)
    return selected

def k_means(
    descriptors: List[np.ndarray], entropies: np.ndarray, size: int
) -> List[int]:
    from sklearn.cluster import KMeans
    
    avg_descriptors = np.array([x.mean(0) for x in descriptors])
    kmeans = KMeans(n_clusters=size, n_init="auto").fit(avg_descriptors)
    selected = []
    for num in range(size):
        selected.append(np.random.choice(np.where(kmeans.labels_ == num)[0]))
    return selected        

# TODO: Ben, please implement
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN
def dbscan_sample(
    descriptors: List[np.ndarray], entropies: np.ndarray, size: int
) -> List[int]:
    from sklearn.cluster import DBSCAN
    from bayes_opt import BayesianOptimization 
    
    avg_descriptors = np.array([x.mean(0) for x in descriptors])
    
    def cost_fn(x):
        dbscan = DBSCAN(eps = x, min_samples=1).fit(avg_descriptors)
        return -abs(size-dbscan.labels_.max())
    bounds = {'x': (0.0001, 0.05)}
    
    optimizer = BayesianOptimization(f=cost_fn, pbounds=bounds, random_state=1)
    optimizer.maximize(init_points=5, n_iter=15)
    
    dbscan = DBSCAN(eps=optimizer.max['params']['x'], min_samples=1).fit(avg_descriptors)
    
    selected = []
    for num in range(dbscan.labels_.max()):
        selected.append(np.random.choice(np.where(dbscan.labels_ == num)[0]))
    return selected 
    