#!/usr/bin/python3

import os
import sys
import argparse
from blockifier.extract_char import *

show_marked_boxes = True;
threshold = 0.5;


def main(source_file,output_directory):

	set_width = 30
	set_height = 30

	# Format file
	filepath, error = change_filetype(source_file)

	if(error):
		print("picture file not found or failed changing format")
		exit()

	# Get output from shell script
	shell_out = run_imagemagick_script(filepath)

	# Get a list of bounding boxes and number of black pixels from the shell script output
	bounding_pixel_list = get_bounding_box(shell_out)

	# Obtain the document image
	document = Image.open(filepath)

	# get rid of unwanted bounding boxes and remove pixel count
	bounding_list = sieve_unwanted(bounding_pixel_list,document.size)

	# sort the bounding list
	bounding_list = sort_bounding_list(bounding_list)

	# Get a list of pictures using the bounding boxes
	picture_list,bounding_list = get_cropped_pics(bounding_list,document)

	# sorts the bounding boxes based on location and saves that setup to filename
	save_newline_to_file(bounding_list,filepath,output_directory)

	if(show_marked_boxes):
		mark_bounding_boxes(filepath,bounding_list,output_directory)

	document.close()

	# Get a list of matrix files from the picture list after resizing every picture.
	float_list = get_float_list(picture_list, set_width, set_height)

	save_matrices_to_file(float_list,filepath,output_directory)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("source_file", help="source file")
	parser.add_argument("dest_dir", help="destination directory")
	args = parser.parse_args()

	main(args.source_file, args.dest_dir)