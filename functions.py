import numpy as np
from spacepy.coordinates import Coords
from spacepy.time import Ticktock


def mean_square(y, n):
    """
    Mean square function
    :param y: Electron Density (array)
    :param n: window size (int)
    :return: MS (array)
    """
    y = np.array(y, dtype=np.float64)
    window = np.ones(n) / n
    return np.convolve(y ** 2, window)


def root_mean_square(y, n):
    """
    Root mean square function
    :param y: Electron Density (array)
    :param n: window size (int)
    :return: RMS (array)
    """
    return np.sqrt(mean_square(y, n))


def _structure_function(y, tau, m=2):
    """
    Structure Function A
    Fast but inaccurate
    Vectorized
    :param y: Electron Density (array)
    :param tau: time lag (array)
    :param m: structure function order (int)
    :return: structure function (array)
    """
    t = np.arange(len(y) - np.max(tau))
    y_diff = np.abs(y[t + tau[:, None]] - y[t])
    return np.mean(np.array(y_diff) ** m, axis=1)


def structure_function(y, tau, m=2):
    """
    Structure Function A
    Slow but accurate
    Partially Vectorized
    :param y: Electron Density (array)
    :param tau: time lag (array)
    :param m: structure function order (int)
    :return: structure function (array)
    """
    t = np.arange(0, len(y) - 1)
    y_difference = []
    for n in range(0, len(tau)):
        #Loop necessary to always use maximum available data points
        y_tau_shifted = y[(t[:(len(t) - n)] + tau[:, None])[n]]
        y_original_time = y[t[:(len(t) - n)]]
        y_difference.append(np.mean(np.abs(y_tau_shifted - y_original_time) ** m))
    return np.array(y_difference)


def empirical_flatness(y, tau):
    """

    :param y: Electron Density (array)
    :param tau: time lag (array)
    :return: empirical flatness (array)
    """
    # tau must not start at zero
    return structure_function(y, tau, 4) / structure_function(y, tau, 2) ** 2


def empirical_flatness_alt(m4, m2):
    """
    Alternate empirical flatness so structure function calculations
    doesn't have to be repeated
    :param m4: strucuture function for m=4 (array)
    :param m2: strucuture function for m=2 (array)
    :return: empirical flatness (array)
    """
    return m4 / m2 ** 2


def normalize(y):
    """

    :param y: array
    :return: normalized by dividing maximum value (array)
    """
    y_norm = y[y != None] / np.max(y[y != None])
    return y_norm


def delta_n(n, dt):
    """
    dN/dt
    :param n: electron density (array)
    :param dt: time shift (int)
    :return: (array)
    """
    if dt == 0:
        return n
    dt = int(dt)
    t = np.arange(len(n) - dt)
    return n[t + dt] - n[t]


# https://stackoverflow.com/questions/7948450/conversion-from-geographic-to-geomagnetic-coordinates
def geographic_to_magnetic(altitude, latitude, longitude, time):
    """
    Slow
    :param altitude: int
    :param latitude: int
    :param longitude: int
    :param time: datetime
    :return: array
    """
    data = np.array([altitude, latitude, longitude])
    data = np.squeeze(data, axis=1)

    cvals = Coords(data.T, 'GEO', 'sph')

    new_time = time.astype(np.datetime64)
    even_newer_time = np.squeeze(np.datetime_as_string(new_time), axis=0)
    cvals.ticks = Ticktock(even_newer_time, 'UTC')
    print('ok')
    return cvals.convert('MAG', 'sph')
