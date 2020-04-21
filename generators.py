from PIL import Image, ImageDraw
from scipy.interpolate import pchip
import mandelbrot


def generate_mandelbrot(colour_points, factor=256, max_iterations=96):
    colour_palette = colour_points + [(0, 0, 0)]
    colour_detail = len(colour_palette) - 1

    pixels = mandelbrot.mandelbrot(7*factor, 5*factor, max_iterations=max_iterations)

    im = Image.new('RGB', (7*factor, 5*factor), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(len(pixels)):
        for y in range(len(pixels[x])):
            colour = colour_palette[int(colour_detail * pixels[x][y] / max_iterations)]
            draw.point([y, x], colour)

    im.save('mandelbrot.bmp')


def _mono_cubic_smoothed(steps, colour_points):
    list_r, list_g, list_b, list_x = zip(*colour_points)
    list_x = [x * (steps - 1) for x in list_x]

    p_r = pchip(list_x, list_r)
    p_g = pchip(list_x, list_g)
    p_b = pchip(list_x, list_b)

    return [(int(p_r(x)), int(p_g(x)), int(p_b(x))) for x in range(steps)]


if __name__ == '__main__':
    colour_points = _mono_cubic_smoothed(511, [(0, 7, 100, 0.0), (32, 107, 203, 0.16), (237, 255, 255, 0.42), (255, 170, 0, 0.6425), (0, 2, 0, 0.8575), (0, 7, 100, 1.0)])
    generate_mandelbrot(colour_points, factor=512)
