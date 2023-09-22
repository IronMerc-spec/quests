import math

import numba as nb
import numpy as np


@nb.njit(fastmath=True)
def logsumexp(X):
    """logsumexp optimized for numba. Can lead to numerical
        instabilities, but it's really fast.

    Arguments:
        X (np.ndarray): an (N, d) matrix with the values. The
            summation will happen over the axis 1.

    Returns:
        logsumexp (np.ndarray): log(sum(exp(X), axis=1))
    """
    result = np.empty(X.shape[0], dtype=X.dtype)
    for i in range(X.shape[0]):
        _sum = 0.0
        for j in range(X.shape[1]):
            _sum += math.exp(X[i, j])

        result[i] = _sum

    return np.log(result)


@nb.njit(fastmath=True)
def cdist(A, B):
    """Optimized distance calculation using numba.

    Arguments:
        A (np.ndarray): an (N, d) matrix with the descriptors
        B (np.ndarray): an (M, d) matrix with the descriptors

    Returns:
        dist (float): entropy of the dataset given by `x`.
    """
    # Computing the dot product
    dist = np.dot(A, B.T)

    # Computing the norm of A
    norm_A = np.empty(A.shape[0], dtype=A.dtype)
    for i in range(A.shape[0]):
        _sum = 0.0
        for j in range(A.shape[1]):
            _sum += A[i, j] ** 2
        norm_A[i] = _sum

    # Computing the norm of B
    norm_B = np.empty(B.shape[0], dtype=A.dtype)
    for i in range(B.shape[0]):
        _sum = 0.0
        for j in range(B.shape[1]):
            _sum += B[i, j] ** 2
        norm_B[i] = _sum

    # computes the distance using the dot product
    # | a - b | ** 2 = <a, a> + <b, b> - 2<a, b>
    for i in range(A.shape[0]):
        for j in range(B.shape[0]):
            d = -2.0 * dist[i, j] + norm_A[i] + norm_B[j]

            # numerical stability
            if d < 0:
                dist[i, j] = 0
            else:
                dist[i, j] = math.sqrt(d)

    return dist


@nb.njit(fastmath=True)
def pdist(A):
    """Optimized distance matrix calculation using numba.

    Arguments:
        A (np.ndarray): an (N, d) matrix

    Returns:
        dm (np.ndarray): an (N, N) matrix with the distances
    """
    N, d = A.shape
    dm = np.empty((N, N), dtype=A.dtype)
    for i in range(N):
        dm[i, i] = 0

    # compute only the off-diagonal terms
    for i in range(N):
        for j in range(i + 1, N):
            dist = 0
            for k in range(d):
                diff = A[i, k] - A[j, k]
                dist += diff * diff

            dist = np.sqrt(dist)
            dm[i, j] = dist
            dm[j, i] = dist

    return dm


@nb.njit(fastmath=True)
def argsort(X: np.ndarray, sort_max: int = -1) -> np.ndarray:
    M, N = X.shape
    if sort_max > 0:
        M = sort_max

    # Adapting argsort
    sorter = np.empty((M, N), dtype=np.int64)
    for i in range(M):
        line_sorter = np.argsort(X[i])
        for j in range(N):
            sorter[i, j] = line_sorter[j]

    return sorter


@nb.njit(fastmath=True)
def inverse_3d(matrix: np.ndarray):
    bx = np.cross(matrix[1], matrix[2])
    by = np.cross(matrix[2], matrix[0])
    bz = np.cross(matrix[0], matrix[1])

    det = matrix[0, 0] * bx[0] + matrix[0, 1] * bx[1] + matrix[0, 2] * bx[2]

    inv = np.empty((3, 3))
    for i in range(3):
        inv[i, 0] = bx[i] / det
        inv[i, 1] = by[i] / det
        inv[i, 2] = bz[i] / det

    return inv


@nb.njit(fastmath=True)
def stack_xyz(arrays: list):
    n = len(arrays)
    stacked = np.empty((n, 3))
    for i in range(n):
        row = arrays[i]
        for j in range(3):
            stacked[i, j] = row[j]

    return stacked