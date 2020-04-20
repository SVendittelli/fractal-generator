"""Generate the mandelbrot set."""

import math


def mandel(real, imaginary, max_iterations=256):
    """For a given complex number, calculate how quickly it grows to infinity.

    Arguments:
        real {number} -- The real component of the complex number.
        imaginary {number} -- The imaginary component of the complex number.

    Keyword Arguments:
        max_iterations {int} -- How many iterations to check that the growth is bounded. (default: {256})

    Returns:
        float between [0, 1] -- How long before the complex number grows to infinity as a fraction of the
            max_iterations on a logarithmic scale. The lower the number, the faster it grows.
    """
    x, y = 0, 0
    for i in range(max_iterations):
        if (x*x + y*y > 4):
            break
        x, y = real + x*x - y*y, imaginary + 2 * x * y

    return math.log(i) / math.log(max_iterations)


def mandelbrot(width, height, max_iterations=256):
    """A 2D array of floats for the mandelbrot set on the complex plane from -2.5 to 1 and -1.25 to 1.25.

    Arguments:
        width {int} -- The width of the output array.
        height {int} -- The height of the output array.

    Keyword Arguments:
        max_iterations {int} -- How many iterations to check that the growth of each complex number is bounded.
            (default: {256})

    Raises:
        ValueError: If the height or width are less than 1.

    Returns:
        2D array of floats between [0, 1] -- Array of numbers representing the growth rate of numbers on the
            complex plane. The lower the number, the faster it grows.
    """
    try:
        x_factor = (3.5 / width)
        y_factor = (2.5 / height)

        return [[mandel(x * x_factor - 2.5, y * y_factor - 1.25, max_iterations=max_iterations) for x in range(width)] for y in range(height)]
    except (ZeroDivisionError):
        raise ValueError('height and width must be at least 1')
