import os
import mandelbrot
import bmp


def generate_mandelbrot(filename='mandelbrot.bmp', factor=64):
    pixels = mandelbrot.mandelbrot(7*factor, 4*factor)
    _remove_file(filename)
    bmp.write_greyscale(filename, pixels)

def _remove_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def main():
    generate_mandelbrot()

if __name__ == '__main__':
    main()
