import random

from PIL import Image

from mosaic_frame import get_grid_spot_coords

test_frame_path = 'W:\Workspace\PD\Video Mosaicer\\frames\\frame-02468.bmp'
im = Image.open(fp=test_frame_path)
width, height = im.size
# Grid the frame
grid_coords = get_grid_spot_coords(width=width, height=height, number_of_rows=20, number_of_columns=40)
# Using co-ordinates of grid spots:
# TESTING GRID PLACING:
grid_image = Image.new('RGB', (width, height))
pixels = grid_image.load()
for top_left, top_right, bottom_left, bottom_right in grid_coords:
    random_colour = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )
    for x in range(int(top_left[0]), int(top_right[0])):
        for y in range(int(top_left[1]), int(bottom_left[1])):
            pixels[x, y] = random_colour
grid_image.save('grid_test.jpg')
