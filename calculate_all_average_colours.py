import os

from calculate_average_colour import convert_rgb_to_lab, get_average_colour_of_file

test_directory = 'W:\Workspace\PD\Video Mosaicer\\frames\\'
test_average_colours_file_path = 'G:\Documents\GitHub\\video-mosaicer\\average_colours.csv'
# test_average_colours_file_path = 'W:\Workspace\PD\Video Mosaicer\\average_colours.csv'


def calculate_all_average_colours(directory):
    file_names = os.listdir(directory)
    results = []
    for file in file_names:
        file_path = os.path.join(directory, file)
        rgb_average_colour = get_average_colour_of_file(file_path=file_path)
        lab_average_colour = convert_rgb_to_lab(rgb_colour=rgb_average_colour)
        results.append({
            'file_name': file,
            'file_path': file_path,
            'lab_average': lab_average_colour
        })
        print('Processed: {}/{}, complete'.format(len(results), len(file_names)))
    return results


def save_average_colours_to_file(file_path, results):
    with open(file_path, 'w') as average_colours_file:
        for result in results:
            line = '{},{},{},{},{}\n'.format(
                result['file_name'],
                result['file_path'],
                result['lab_average'][0],
                result['lab_average'][1],
                result['lab_average'][2]
            )
            average_colours_file.write(line)


if __name__ == '__main__':
    all_average_colours = calculate_all_average_colours(directory=test_directory)
    print(all_average_colours)
    save_average_colours_to_file(file_path=test_average_colours_file_path, results=all_average_colours)
