import math
import os

from PIL import Image, ImageChops

from calculate_average_colours_in_grid import calculate_average_colours_per_grid_spot


def average_two_rgb_colours(rgb_a, rgb_b):
    squares_r = pow(rgb_a[0], 2) + pow(rgb_b[0], 2)
    squares_g = pow(rgb_a[1], 2) + pow(rgb_b[1], 2)
    squares_b = pow(rgb_a[2], 2) + pow(rgb_b[2], 2)
    return int(math.sqrt(squares_r)), int(math.sqrt(squares_g)), int(math.sqrt(squares_b))


def tint_image(image, tint_color):
    tint_color = (math.ceil(tint_color[0]), math.ceil(tint_color[1]), math.ceil(tint_color[2]))
    return ImageChops.multiply(image, Image.new('RGB', image.size, tint_color))


def mosaic_frame_using_grid_colours(frame_file_path, target_file_path, number_of_rows, number_of_columns, files_and_average_colours):
    file_paths_by_creation_time = [file['file_path'] for file in files_and_average_colours]
    file_paths_by_creation_time.sort(key=lambda x: int(os.path.getctime(x)))
    print('Mosaicing: {}'.format(frame_file_path))
    current_file_index = 0
    im = Image.open(fp=frame_file_path)
    image_pixels = im.load()
    width, height = im.size
    mosaiced_image = Image.new('RGB', (int(width), int(height)))
    mosaiced_image_pixels = mosaiced_image.load()
    # Grid the frame and get its average colours of each splot
    grid_coords_and_average_colour = calculate_average_colours_per_grid_spot(
        file_path=frame_file_path,
        number_of_rows=number_of_rows,
        number_of_columns=number_of_columns
    )
    # Using co-ordinates of grid spots:
    # Replace each grid spot with closest average frame
    replacements = 0
    for grid_data in grid_coords_and_average_colour:
        grid_coords = grid_data['spot']
        grid_average_colour = grid_data['average_colour']
        top_left = grid_coords[0]
        top_right = grid_coords[1]
        bottom_left = grid_coords[2]
        replacements += 1
        print('{}/{} complete'.format(replacements, len(grid_coords_and_average_colour)))
        # Get grid pixels
        grid_pixels = []
        for x in range(int(math.floor(top_left[0])), int(math.floor(top_right[0]))):
            for y in range(int(math.floor(top_left[1])), int(math.floor(bottom_left[1]))):
                grid_pixels.append(
                    image_pixels[x, y]
                )
        # grid_spot_average_colour_lab = convert_rgb_to_lab(grid_average_colour)
        # # Find closest average frame
        # closest_file_path = find_image_with_closest_average_colour(grid_spot_average_colour_lab, files_and_average_colours)
        file_path = file_paths_by_creation_time[current_file_index]
        current_file_index += 1
        if current_file_index == len(files_and_average_colours):
            current_file_index = 0

        # Load in closest average frame
        closest_image = Image.open(file_path)
        # Resize the closest image to the target grid spot size
        grid_width = width // number_of_columns
        grid_height = height // number_of_rows
        resized_image = closest_image.resize((grid_width, grid_height), Image.ANTIALIAS)

        # Tint the image with the average colour
        tinted_image = tint_image(resized_image, grid_average_colour)

        # Replace grid spot in target frame with closest average frame
        for x in range(0, grid_width):
            for y in range(0, grid_height):
                x_actual = top_left[0] + x
                y_actual = top_left[1] + y
                tinted_image_pixel = tinted_image.getpixel((x, y))
                new_colour = average_two_rgb_colours(tinted_image_pixel,  mosaiced_image_pixels[x_actual, y_actual])
                mosaiced_image_pixels[x_actual, y_actual] = new_colour
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
    photos_for_mosaic_dir = ''
    test_frame_path = 'G:\Dropbox\Personal\R&S\Photos Together\G0034204.JPG'
    test_path = 'mosaic_test.jpg'
    test_colours_path = 'average_colours.csv'
    # results = calculate_all_average_colours_in_directory('G:\Dropbox\Personal\R&S\Photos Together')
    # save_average_colours_to_file(file_path=test_colours_path, results=results)
    files_and_average_colours = get_video_average_colours(average_colours_file_path=test_colours_path)
    mosaic_frame_using_grid_colours(
        frame_file_path=test_frame_path,
        target_file_path=test_path,
        number_of_rows=60,
        number_of_columns=60,
        files_and_average_colours=files_and_average_colours
    )
