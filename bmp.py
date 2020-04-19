"""A module for working with bitmap (BMP) images."""


def write_greyscale(filename, pixel_data):
    """Creates and writes a BMP file.

    Args:

        filename: The name of the file to be created.

        pixel_data: A recangular image stored as a sequence of rows.
            Each row should be an integer between 0-255.

    Raises:

        ValueError: If any values are out of range.

        OSError: If the file could not be written.
    """

    # height, width = get_dimensions(pixel_data)
    height = len(pixel_data)
    width = len(pixel_data[0])

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
        for c in range(256):
            bmp.write(bytes((c, c, c, 0)))  # blue, green, red, 0x00

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
