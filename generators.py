from PIL import Image, ImageDraw
from scipy.interpolate import pchip
import mandelbrot
import bmp


def generate_mandelbrot_8_bit(width, height, max_iterations=40):
    """Generate a mandelbrot set image using 8 bit greyscale.

    Keyword Arguments:
        factor {int} -- The images are in a 7:5 aspect ratio, the factor is the multiplier of these for the final
            image dimensions. (default: {512})
    """
    pixels = mandelbrot.mandelbrot(width, height, max_iterations=max_iterations)
    bmp.write_greyscale('mandelbrot_8_bit.bmp', pixels)


def generate_mandelbrot(width, height, colour_points, max_iterations=80):
    """Generate a mandelbrot set image using a custom colour scale.

    Arguments:
        width {[type]} -- [description]
        height {[type]} -- [description]
        colour_points {array} -- an array of 3-tuples for the RGB colour scale

    Keyword Arguments:
        max_iterations {int} -- [description] (default: {80})
    """
    colour_palette = colour_points + [(0, 0, 0)]
    colour_detail = len(colour_palette) - 1

    pixels = mandelbrot.mandelbrot(width, height, max_iterations=max_iterations)

    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)

    for y in range(len(pixels)):
        for x in range(len(pixels[y])):
            colour = colour_palette[
                int(colour_detail * pixels[y][x] / max_iterations)
            ]
            draw.point([x, y], colour)

    im.save('mandelbrot.bmp')


def _mono_cubic_smoothed(steps, colour_points):
    """Create a smooth colour gradient between points.

    Arguments:
        steps {int} -- the number of colour points to output
        colour_points {array} -- an array of 4-tuples representing the control points on the scale. Each tuple is
                                 formed of: (red, green, blue, position).

    Returns:
        array -- an array of 3-tuples for the RGB colour scale
    """
    points_r, points_g, points_b, points_x = zip(*colour_points)
    scaled_x = [x * (steps - 1) for x in points_x]

    p_r = pchip(scaled_x, points_r)
    p_g = pchip(scaled_x, points_g)
    p_b = pchip(scaled_x, points_b)

    return [(int(p_r(x)), int(p_g(x)), int(p_b(x))) for x in range(steps)]


def main():
    # Based on the colour scale used by Ultra Fractal
    colour_points = _mono_cubic_smoothed(1023, [
        (0, 7, 100, 0.0),
        (32, 107, 203, 0.16),
        (237, 255, 255, 0.42),
        (255, 170, 0, 0.6425),
        (0, 2, 0, 0.8575),
        (0, 7, 100, 1.0)
    ])
    # The mandelbrot fractal looks best in a ratio of 7:5
    factor = 512
    generate_mandelbrot_8_bit(7*factor, 5*factor)
    generate_mandelbrot(7*factor, 5*factor, colour_points)


if __name__ == '__main__':
    main()
