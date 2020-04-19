import os
import mandelbrot
import bmp


def generate_mandelbrot(factor=512):
    pixels = mandelbrot.mandelbrot(7*factor, 5*factor, max_iterations=1024)
    _remove_file('mandelbrot_grey.bmp')
    bmp.write_greyscale('mandelbrot_grey.bmp', pixels)
    _remove_file('mandelbrot_colour.bmp')
    bmp.write_blue_scale('mandelbrot_colour.bmp', pixels)


def _remove_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def main():
    generate_mandelbrot()


if __name__ == '__main__':
    main()
