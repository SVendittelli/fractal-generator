"""Generate fractal image files."""

import os
import mandelbrot
import bmp


def generate_mandelbrot(factor=512):
    """Generate a greyscale and coloured mandelbrot set image.

    Keyword Arguments:
        factor {int} -- The images are in a 7:5 aspect ratio, the factor is the multiplier of these for the final
            image dimensions. (default: {512})
    """
    pixels = mandelbrot.mandelbrot(7*factor, 5*factor, max_iterations=256)
    _remove_file('mandelbrot_grey.bmp')
    bmp.write_greyscale('mandelbrot_grey.bmp', pixels)
    _remove_file('mandelbrot_colour.bmp')
    bmp.write_blue_scale('mandelbrot_colour.bmp', pixels)


def _remove_file(filename):
    """Delete a file if it exists.

    Arguments:
        filename {string} -- The file to delete.
    """
    if os.path.isfile(filename):
        os.remove(filename)


def main():
    generate_mandelbrot()


if __name__ == '__main__':
    main()
