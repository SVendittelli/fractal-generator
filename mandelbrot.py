"""Generate the mandelbrot set."""

from  math import log, sqrt
import numpy as np

# https://linas.org/art-gallery/escape/escape.html
def mandel(real, imaginary, max_iterations=256):
    x, y = 0, 0
    for i in range(max_iterations):
        if (x*x + y*y > 4):
            break
        x, y = real + x*x - y*y, imaginary + 2 * x * y

    if i == max_iterations - 1:
        return max_iterations

    try:
        return i + 1 - log(log(sqrt(x*x + y*y))) / log(2)
    except (ValueError):
        return i


def mandelbrot(width, height, max_iterations=256):
    try:
        x_factor = (3.5 / width)
        y_factor = (2.5 / height)

        return [[mandel(x * x_factor - 2.5, y * y_factor - 1.25, max_iterations=max_iterations) for x in range(width)] for y in range(height)]
    except (ZeroDivisionError):
        raise ValueError('height and width must be at least 1')
