#!/usr/bin/python3

import os
import sys
from blockifier.extract_char import *

show_marked_boxes = False;
threshold = 0.5;

if len(sys.argv) < 3:
    print(sys.argv)
    print("Not enough arguements")
    print("Usage: python (image file)")# (output directory) (width) (height)")
    exit()

print("Do you want to save images with bounding boxes? (y/n)")
answer = input()

if answer == "y" or answer == "Y":
	show_marked_boxes = True


# Get relevant cmd input
cmd_inputs = sys.argv[1:]

source_directory = cmd_inputs[0]
output_directory = cmd_inputs[1]
set_width = 30 #int(cmd_inputs[2])
set_height = 30 #int(cmd_inputs[3])

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

	# sorts the bounding boxes based on location and saves that setup to filename
	bounding_list = save_newline_to_file(bounding_list,filepath,output_directory)

	# Get a list of pictures using the bounding boxes
	picture_list,bounding_list = get_cropped_pics(bounding_list,document)

	if(show_marked_boxes):
		mark_bounding_boxes(filepath,bounding_list,output_directory)

	document.close()

	# Get a list of binary files from the picture list after resizing every picture.
	float_list = get_float_list(picture_list, set_width, set_height)

	save_binary_to_file(float_list,filepath,output_directory)


