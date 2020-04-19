"""A module for working with bitmap (BMP) images."""


def write_blue_scale(filename, pixel_data):
    range_1 = _linear(40, 100, 7, 0, 203, 107, 32)  # 40
    range_2 = _linear(66, 203, 107, 32, 255, 255, 237)  # 106
    range_3 = _linear(57, 255, 255, 237, 0, 170, 255)  # 163
    range_4 = _linear(55, 0, 170, 255, 0, 2, 0)  # 218
    range_5 = _linear(37, 0, 2, 0, 100, 7, 0)  # 255
    black = [bytes((0, 0, 0, 0))]  # 256

    colour_palette = range_1 + range_2 + range_3 + range_4 + range_5 + black
    write_8_bit(filename, pixel_data, colour_palette)


def write_greyscale(filename, pixel_data):
    # colour table (blue, green, red, 0x00)
    colour_palette = [bytes((c, c, c, 0)) for c in range(256)]
    write_8_bit(filename, pixel_data, colour_palette)


def write_8_bit(filename, pixel_data, colour_palette):
    """Creates and writes a BMP file.

    Args:

        filename: The name of the file to be created.

        pixel_data: A recangular image stored as a sequence of rows.
            Each row should be an integer between 0-255.

    Raises:

        ValueError: If any values are out of range.

        OSError: If the file could not be written.
    """

    height, width = get_dimensions(pixel_data)
    pixel_data = _scale_to_256(pixel_data)

    with open(filename, 'wb') as bmp:
        # BMP header
        bmp.write(b'BM')

        # file size
        size_position = bmp.tell()
        bmp.write(b'\x00\x00\x00\x00')  # dummy 0, to be replaced later

        # reserved bytes
        bmp.write(b'\x00\x00')
        bmp.write(b'\x00\x00')

        # offset for pixel data
        pixel_offset_position = bmp.tell()
        bmp.write(b'\x00\x00\x00\x00')  # dummy 0, to be replaced later

        # DIB header (BITMAPINFOHEADER)

        # size of this header (40)
        bmp.write(b'\x28\x00\x00\x00')
        # bitmap width in pixels (signed integer)
        bmp.write(_int_to_bytes(width))
        # bitmap height in pixels (signed integer)
        bmp.write(_int_to_bytes(height))
        # number of colour planes, must be 1
        bmp.write(b'\x01\x00')
        # number of bits per pixel, which is the colour depth of the image (8 bit)
        bmp.write(b'\x08\x00')
        # compression method being used (no compression)
        bmp.write(b'\x00\x00\x00\x00')
        # image size (dummy 0 for uncompressed image)
        bmp.write(b'\x00\x00\x00\x00')
        # horizontal resolution of the image (unused)
        bmp.write(b'\x00\x00\x00\x00')
        # vertical resolution of the image (unused)
        bmp.write(b'\x00\x00\x00\x00')
        # number of colours in the colour palette (0 for full palette)
        bmp.write(b'\x00\x00\x00\x00')
        # number of important colours used (0 for all colours)
        bmp.write(b'\x00\x00\x00\x00')

        # colour table
        for c in colour_palette:
            bmp.write(c)

        # pixel data
        pixel_data_position = bmp.tell()
        for row in reversed(pixel_data):
            bmp.write(bytes(row))
            padding = b'\x00' * ((4 - (len(row) % 4)) % 4)
            bmp.write(padding)

        eof_position = bmp.tell()

        # set file size
        bmp.seek(size_position)
        bmp.write(_int_to_bytes(eof_position))

        # set pixel offset
        bmp.seek(pixel_offset_position)
        bmp.write(_int_to_bytes(pixel_data_position))


def get_dimensions(array):
    """Get the height and width of a 2 dimensional array.

    Arguments:
        pixels {array} -- A 2 dimensional array

    Raises:
        ValueError: if pixels is not at least a 1x1 recangular array

    Returns:
        tuple -- the height and width of the array as a tuple
    """

    height = len(array)
    if height == 0:
        raise ValueError('array must have height > 0')

    width = len(array[0])
    if width == 0:
        raise ValueError('array must have width > 0')

    for row in array:
        if len(row) != width:
            raise ValueError('all rows of array must be the same length')

    return height, width


def _int_to_bytes(i):
    return i.to_bytes(4, byteorder='little')


def _scale_to_256(array):
    minimum = min([min(r) for r in array])
    maximum = max([max(r) for r in array])
    return [[int(255 * (x - minimum) / (maximum - minimum)) for x in line] for line in array]


def _linear(steps, blue_start, green_start, red_start, blue_end, green_end, red_end):
    blue_step = int((blue_end - blue_start) / steps)
    green_step = int((green_end - green_start) / steps)
    red_step = int((red_end - red_start) / steps)
    return [bytes((blue_start + step * blue_step,
                   green_start + step * green_step,
                   red_start + step * red_step,
                   0)) for step in range(steps)]


if __name__ == '__main__':
    print(_scale_to_256([[1, 2], [3, 4]]))
