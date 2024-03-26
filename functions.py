import numpy as np


def mean_square(y, n):
    y = np.array(y, dtype=np.float64)
    window = np.ones(n) / n
    return np.convolve(y ** 2, window)


def root_mean_square(y, n):
    return np.sqrt(mean_square(y, n))


def structure_function(y, tau, m=1):
    t = np.arange(len(y) - np.max(tau))
    y_diff = np.abs(y[t + tau[:, None]] - y[t])
    return np.mean(y_diff ** m, axis=1)


def empirical_flatness(y, tau):
    # tau must not start at zero
    return structure_function(y, tau, 4) / structure_function(y, tau, 2) ** 2


def normalize(y):
    y_norm = y[y != None] / np.max(y[y != None])
    return y_norm


def delta_n(n, dt):
    t = np.arange(len(n) - dt)
    return n[t + dt] - n[t]
