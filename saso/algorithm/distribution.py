import numpy as np


def distribution(value, length: int, mid_offset: int = 0) -> []:
    """
    Generate a length-defined value distribution similar to the bell curve (e.g. Gaussian Distribution).
    The sum of the distribution is equal to the input value.
    The center of the distribution is definitely the greatest value in the distribution
    :param value: the value to distribute to
    :param length: the length of the distribution
    :param mid_offset: change the center of the distribution relatively to the middle element (0 - center; 0< - left hand center; 0> - right hand center)
    :return: list of a length-defined value distribution
    """
    mu = np.linspace(0, length - 1, length) - mid_offset
    sigma = length / 6.0
    values = np.exp(-0.5 * ((mu - (length - 1) / 2.0) / sigma) ** 2)
    values = values / np.sum(values) * value

    return values.tolist()
