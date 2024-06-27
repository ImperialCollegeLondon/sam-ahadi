import numpy as np


def calc_mag(vector):
    mag_BB = np.sqrt(pow(vector[0, :], 2) + pow(vector[1, :], 2) + pow(vector[2, :], 2))
    return mag_BB
