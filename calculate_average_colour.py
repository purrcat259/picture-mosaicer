from PIL import Image

test_file_path = 'W:\Workspace\PD\Video Mosaicer\\frames\\frame-00001.bmp'


def get_average_colour_of_file(file_path):
    # Load in image
    im = Image.open(fp=file_path)
    return calculate_average_colour(pixels=im.getdata())


def calculate_average_colour(pixels):
    # Calculate average for each channel
    average_red = 0
    average_green = 0
    average_blue = 0
    number_of_pixels = len(pixels)
    # Get pixel values
    for pixel in pixels:
        # This returns a tuple of (RED, GREEN, BLUE)
        average_red += pixel[0]
        average_green += pixel[1]
        average_blue += pixel[2]
    average_red /= number_of_pixels
    average_blue /= number_of_pixels
    average_green /= number_of_pixels
    # print('File path: {}'.format(file_path))
    # print('Average Red: {}'.format(average_red))
    # print('Average Green: {}'.format(average_green))
    # print('Average Blue: {}'.format(average_blue))
    # Return as a single colour
    return average_red, average_green, average_blue


# Reference: https://github.com/antimatter15/rgb-lab/blob/master/color.js
def convert_rgb_to_lab(rgb_colour):
    # Normalise the values from 0 -> 255 to 0 -> 1
    normalised_red = rgb_colour[0] / 255.0
    normalised_green = rgb_colour[1] / 255.0
    normalised_blue = rgb_colour[2] / 255.0
    red = pow((normalised_red + 0.055) / 1.055, 2.4) if normalised_red > 0.04045 else normalised_red / 12.92
    green = pow((normalised_green + 0.055) / 1.055, 2.4) if normalised_green > 0.04045 else normalised_green / 12.92
    blue = pow((normalised_blue + 0.055) / 1.055, 2.4) if normalised_blue > 0.04045 else normalised_blue / 12.92

    x = (red * 0.4124 + green * 0.3576 + blue * 0.1805) / 0.95047
    y = (red * 0.2126 + green * 0.7152 + blue * 0.0722) / 1.00000
    z = (red * 0.0193 + green * 0.1192 + blue * 0.9505) / 1.08883

    x = pow(x, 1 / 3) if x > 0.008856 else 7.787 * x + 16 / 116
    y = pow(y, 1 / 3) if y > 0.008856 else 7.787 * y + 16 / 116
    z = pow(z, 1 / 3) if z > 0.008856 else 7.787 * z + 16 / 116
    return [(116 * y) - 16, 500 * (x - y), 200 * (y - z)]


if __name__ == '__main__':
    rgb_average_colour = calculate_average_colour(pixels=[(0.0, 0.0, 0.0), (255.0, 255.0, 255.0)])
    print(rgb_average_colour)
    lab_average_colour = convert_rgb_to_lab(rgb_average_colour)
    print(lab_average_colour)
    average_colour = get_average_colour_of_file(test_file_path)
    print(average_colour)
