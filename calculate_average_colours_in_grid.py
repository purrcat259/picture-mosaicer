from PIL import Image

from calculate_average_colour import calculate_average_colour
from mosaic_frame import get_grid_spot_coords


def calculate_average_colours_per_grid_spot(file_path, number_of_rows, number_of_columns):
    print('Calculating average colours for {} grid spots'.format(number_of_rows * number_of_columns))
    im = Image.open(fp=file_path)
    width, height = im.size
    # Grid the frame
    grid_coords = get_grid_spot_coords(width=width, height=height, number_of_rows=number_of_rows, number_of_columns=number_of_columns)
    # image pixels
    grid_average_colours = []
    for top_left, top_right, bottom_left, bottom_right in grid_coords:
        # For each grid spot
        grid_spot_pixels = []
        for x in range(int(top_left[0]), int(top_right[0])):
            for y in range(int(top_left[1]), int(bottom_left[1])):
                grid_spot_pixels.append(im.getpixel((x, y)))
        average_colour = calculate_average_colour(grid_spot_pixels)
        grid_average_colours.append(
            {
                'spot': (top_left, top_right, bottom_left, bottom_right),
                'average_colour': average_colour
            }
        )
    return grid_average_colours


if __name__ == '__main__':
    test_file_path = 'test.png'
    calculate_average_colours_per_grid_spot(test_file_path, 20, 40)
