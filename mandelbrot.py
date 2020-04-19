import math


def mandel(real, imaginary, max_iterations=256):
    x, y = 0, 0
    for i in range(max_iterations):
        if (x*x + y*y > 4):
            break
        x, y = real + x*x - y*y, imaginary + 2 * x * y

    return math.log(i) / math.log(max_iterations)


def mandelbrot(width, height, max_iterations=256):
    try:
        x_factor = (3.5 / width)
        y_factor = (2.5 / height)

        return [[mandel(x * x_factor - 2.5, y * y_factor - 1.25, max_iterations=max_iterations) for x in range(width)] for y in range(height)]
    except (ZeroDivisionError):
        print('height and width must be at least 1')
