import random

import math
from PIL import Image

from calculate_average_colour import calculate_average_colour, convert_rgb_to_lab


def mosaic_frame(frame_file_path, target_file_path, number_of_rows, number_of_columns, files_and_average_colours):
    im = Image.open(fp=frame_file_path)
    image_pixels = im.load()
    width, height = im.size
    mosaiced_image = Image.new('RGB', (int(width), int(height)))
    mosaiced_image_pixels = mosaiced_image.load()
    # Grid the frame
    grid_coords = get_grid_spot_coords(width=width, height=height, number_of_rows=number_of_rows, number_of_columns=number_of_columns)
    # Using co-ordinates of grid spots:
    # Replace each grid spot with closest average frame
    replacements = 0
    for top_left, top_right, bottom_left, bottom_right in grid_coords:
        replacements += 1
        print('{}/{} complete'.format(replacements, len(grid_coords)))
        # Get grid pixels
        grid_pixels = []
        for x in range(int(top_left[0]), int(top_right[0])):
            for y in range(int(top_left[1]), int(bottom_left[1])):
                grid_pixels.append(
                    image_pixels[x, y]
                )
        # Calculate average colour of grid spot
        grid_spot_average_colour_rgb = calculate_average_colour(grid_pixels)
        grid_spot_average_colour_lab = convert_rgb_to_lab(grid_spot_average_colour_rgb)
        # Find closest average frame
        closest_file_path = find_image_with_closest_average_colour(grid_spot_average_colour_lab, files_and_average_colours)
        # Load in closest average frame
        closest_image = Image.open(closest_file_path)
        # Resize the closest image to the target grid spot size
        grid_width = width // number_of_columns
        grid_height = height // number_of_rows
        resized_image = closest_image.resize((grid_width, grid_height), Image.ANTIALIAS)
        # Replace grid spot in target frame with closest average frame
        for x in range(0, grid_width):
            for y in range(0, grid_height):
                x_actual = top_left[0] + x
                y_actual = top_left[1] + y
                mosaiced_image_pixels[x_actual, y_actual] = resized_image.getpixel((x, y))
    mosaiced_image.save(fp=target_file_path)


def find_image_with_closest_average_colour(target_image_colour, files_and_average_colours):
    closest_file_path = None
    closest_distance = 1000000
    for data in files_and_average_colours:
        # file = data['file_name']
        file_path = data['file_path']
        average_lab = data['lab_average']
        # find distance between target_image_colour and current_colour
        distance = calculate_lab_colour_distance(average_lab, target_image_colour)
        if distance < closest_distance:
            closest_distance = distance
            closest_file_path = file_path
    return closest_file_path


# Simple Eucledian distance
def calculate_lab_colour_distance(colour_a, colour_b):
    return math.sqrt(pow(colour_a[0] - colour_b[0], 2) + pow(colour_a[1] - colour_b[1], 2) + pow(colour_a[2] - colour_b[2], 2))


def get_video_average_colours(average_colours_file_path):
    files_and_average_colours = []
    with open(average_colours_file_path) as average_colours_file:
        for line in average_colours_file:
            line = line.replace('\n', '')
            data = line.split(',')
            files_and_average_colours.append(
                {
                    'file_name': data[0],
                    'file_path': data[1],
                    'lab_average': (float(data[2]), float(data[3]), float(data[4]))
                }
            )
    return files_and_average_colours


# Assumption:
# Number of columns and number of rows will always be a factor of the width and the height
# If not, then the last grid spot will not be in line with the image, but will overflow
def get_grid_spot_coords(width, height, number_of_rows, number_of_columns):
    grid_width = width / number_of_columns
    grid_height = height / number_of_rows
    grid_spot_coords = []
    for row_index in range(0, number_of_rows):
        for column_index in range(0, number_of_columns):
            grid_spot_coords.append(
                (
                    (column_index * grid_width, row_index * grid_height),
                    ((column_index * grid_width) + grid_width, row_index * grid_height),
                    (column_index * grid_width, (row_index * grid_height) + grid_height),
                    ((column_index * grid_width) + grid_width, (row_index * grid_height) + grid_height)
                )
            )
    return grid_spot_coords


if __name__ == '__main__':
    test_frame_path = 'W:\Workspace\PD\Video Mosaicer\\frames\\frame-02468.bmp'
    test_path = 'test.png'
    test_colours_path = 'average_colours.csv'
    files_and_average_colours = get_video_average_colours(average_colours_file_path=test_colours_path)
    mosaic_frame(
        frame_file_path=test_frame_path,
        target_file_path=test_path,
        number_of_rows=10,
        number_of_columns=20,
        files_and_average_colours=files_and_average_colours
    )
