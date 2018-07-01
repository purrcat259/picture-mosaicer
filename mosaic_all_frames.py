import os

from mosaic_frame import get_video_average_colours, mosaic_frame
from multiprocessing import Pool


def mosaic_all_frames(source_directory, target_directory, colour_averages_file_path, number_of_rows, number_of_columns, number_of_simultaneous_threads=3):
    files_and_average_colours = get_video_average_colours(colour_averages_file_path)
    source_frames = os.listdir(source_directory)
    already_mosaiced_frames = os.listdir(target_directory)
    already_mosaiced_frames = [frame.replace('_mosaic.png', '') for frame in already_mosaiced_frames]
    job_list = []
    for source_frame in source_frames:
        if source_frame.replace('.bmp', '') in already_mosaiced_frames:
            print('Skipping:', source_frame)
            continue
        source_frame_path = os.path.join(source_directory, source_frame)
        target_frame_path = os.path.join(target_directory, source_frame.replace('.bmp', '_mosaic.png'))
        job_list.append((source_frame, source_frame_path, target_frame_path, number_of_rows, number_of_columns, files_and_average_colours))
    with Pool(number_of_simultaneous_threads) as p:
        p.map(mosaic_current_frame, job_list)


def mosaic_current_frame(data):
    source_frame, source_frame_path, target_frame_path, number_of_rows, number_of_columns, files_and_average_colours = data
    print('Mosaicing:', source_frame)
    mosaic_frame(
        frame_file_path=source_frame_path,
        target_file_path=target_frame_path,
        number_of_rows=number_of_rows,
        number_of_columns=number_of_columns,
        files_and_average_colours=files_and_average_colours
    )

if __name__ == '__main__':
    test_directory = 'W:\Workspace\PD\Video Mosaicer\\frames\\'
    test_target_directory = 'W:\Workspace\PD\Video Mosaicer\\mosaics\\'
    test_colour_averages_path = 'average_colours.csv'
    mosaic_all_frames(
        source_directory=test_directory,
        target_directory=test_target_directory,
        colour_averages_file_path=test_colour_averages_path,
        number_of_rows=40,
        number_of_columns=80
    )
