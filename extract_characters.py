#!/usr/bin/python3

import os
import sys
import argparse
from blockifier.extract_char import *

show_marked_boxes = False;
threshold = 0.5;


def main(source_directory,output_directory):

	set_width = 30
	set_height = 30

	files_to_ignore = []

	for img_path in os.listdir(source_directory):
		period_pos = img_path.rfind('.')
		char = img_path[period_pos-1:period_pos]
		img_path = os.path.join(source_directory, img_path)


		# Make sure that we are not taking the same file twice in case we change format
		file_name, filetype = os.path.splitext(img_path)
		if file_name in files_to_ignore:
			continue

		# Format file
		filepath, error = change_filetype(img_path)

		if(error):
			print("picture file not found or failed changing format")
			exit()
		files_to_ignore.append(file_name)

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
	parser.add_argument("source_dir", help="source directory")
	parser.add_argument("dest_dir", help="destination directory")
	args = parser.parse_args()

	print("Do you want to save images with bounding boxes? (y/n)")
	answer = input()

	if answer == "y" or answer == "Y":
		show_marked_boxes = True

	main(args.source_dir, args.dest_dir)