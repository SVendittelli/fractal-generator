"""A module for working with bitmap (BMP) images."""


def write_greyscale(filename, pixel_data):
    """Writes an 8-bit greyscale BMP file.

    Arguments:
        filename {string} -- The name of the file to be created.
        pixel_data {[2D array of numbers]} -- A recangular image stored as a sequence of rows.

    Raises:
        ValueError: If the pixel_data is not a rectangular array.
        OSError: If the file could not be written.
    """

    colour_palette = [bytes((c, c, c, 0))
                      for c in range(1, 256)] + [bytes((0, 0, 0, 0))]
    write_8_bit(filename, pixel_data, colour_palette)


def write_8_bit(filename, pixel_data, colour_palette):
    """Creates and writes an 8-bit BMP file.

    Arguments:
        filename {string} -- The name of the file to be created.
        pixel_data {[2D array of numbers]} -- A recangular image stored as a sequence of rows.
        colour_palette {array of bytes} -- The colour palette stored as an array length 256 of bytes of
            blue, green, red, 0x00.

    Raises:
        ValueError: If the pixel_data is not a rectangular array.
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
    """Convert an integer to a little endian 4 byte array.

    Arguments:
        i {integer} -- The integer to convert.

    Returns:
        byte array -- The integer converted to 4 bytes.
    """
    return i.to_bytes(4, byteorder='little')


def _scale_to_256(array):
    """Rescale a 2D array of numbers to a same sized array with the numbers projected onto members of range(256).

    Arguments:
        array {2D array of numbers} -- The array to be rescaled.

    Returns:
        2D array of integers -- The input array rescaled to 0-255.
    """
    minimum = min([min(r) for r in array])
    maximum = max([max(r) for r in array])
    return [[int(255 * (x - minimum) / (maximum - minimum)) for x in line] for line in array]

