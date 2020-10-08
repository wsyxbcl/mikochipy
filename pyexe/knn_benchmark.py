from functools import wraps
import numpy as np
from scipy.spatial.distance import cdist
from time import time

def timing(func):
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print("Run time: {} s".format(end - start))
        return result
    return _time_it

@timing
def distance_for(test_x, train_x, metric):
    distances = []
    if metric == "Manhattan":
        print("Manhattan dist using for...")
        for row in test_x:
            distance = np.sum(np.abs(train_x - row), axis=1)
            distances.append(distance)
        return np.array(distances)
    elif metric == "Euclidean":
        print("Euclidean dist using for...")
        for row in test_x:
            distance = np.sqrt(np.sum(np.power(train_x - row, 2), axis=1))
            distances.append(distance)
        return np.array(distances)
    elif metric == "Chebyshev":
        print("Chebyshev dist using for...")
        for row in test_x:
            distance = np.max(np.abs(train_x - row), axis=1)
            distances.append(distance)
        return np.array(distances)

@timing
def distance_scipy_cdist(test_x, train_x, metric):
    if metric == "Manhattan":
        print("Manhattan dist using cdist...")
        distances = cdist(test_x, train_x, 'cityblock')
    elif metric == "Euclidean":
        print("Eulidean dist using cdist...")
        distances = cdist(test_x, train_x, "euclidean")
    elif metric == "Chebyshev":
        print("Chebyshev dist using cdist...")
        distances = cdist(test_x, train_x, "chebyshev")
    return distances

@timing
def distance_broadcasting(test_x, train_x, metric):
    dx = x_test[:, 0][..., np.newaxis] - x_train[:, 0][np.newaxis, ...]
    dy = dy = x_test[:, 1][..., np.newaxis] - x_train[:, 1][np.newaxis, ...]
    dist = np.array([dx, dy])

    if metric == "Euclidean":
        print("Euclidean dist using broadcasting")
        return (dist ** 2).sum(axis=0) ** 0.5
        

if __name__ == '__main__':
    x_test = np.random.rand(100, 2)
    x_train = np.random.rand(1000000, 2)
    dist_for_e = distance_for(x_test, x_train, metric="Euclidean")
    dist_cdist_e = distance_scipy_cdist(x_test, x_train, metric="Euclidean")
    dist_broadcasting_e = distance_broadcasting(x_test, x_train, metric="Euclidean")

    # dist_for_m = distance_for(x_test, x_train, metric="Manhattan")
    # dist_cdist_m = distance_scipy_cdist(x_test, x_train, metric="Manhattan")

    # dist_for_c = distance_for(x_test, x_train, metric="Chebyshev")
    # dist_cdist_c = distance_scipy_cdist(x_test, x_train, metric="Chebyshev")

    #print(dist_for_e==dist_cdist_e, dist_for_e==dist_broadcasting_e)
