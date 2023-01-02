import numpy as np
import warnings
from numpy.linalg import norm



def euclidean(matrix_one, matrix_two):
    lengths = -2 * matrix_one @ matrix_two.T + np.sum(matrix_two ** 2, axis=1) + \
              np.sum(matrix_one ** 2, axis=1)[:, np.newaxis]
    return np.sqrt(np.abs(lengths))


def manhattan(matrix_one, matrix_two):
    lengths = np.abs(matrix_one[:, np.newaxis] - matrix_two).sum(axis=-1)

    return lengths


def chebyshev(matrix_one, matrix_two):
    lengths = np.abs(matrix_one[:, np.newaxis] - matrix_two).max(axis=-1)

    return lengths


def cosine(matrix_one, matrix_two):
    norm_matrix_one = matrix_one / np.linalg.norm(matrix_one, axis=1, keepdims=True)
    norm_matrix_two = matrix_two / np.linalg.norm(matrix_two, axis=1, keepdims=True)

    return np.matmul(norm_matrix_one, norm_matrix_two.T)  # 1-
