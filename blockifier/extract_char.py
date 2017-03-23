#!/usr/bin/python3

from __future__ import print_function
from PIL import Image, ImageDraw, ImageFont
from shutil import copyfile

import os, sys, subprocess
import re
import shlex


# Format the file to .png to able to use imagemagick
def change_filetype(filename):
	newfilename, filetype = os.path.splitext(filename)
	error = False

	if (filetype != ".png"):
		try:
			Image.open(filename).save(newfilename+".png")
		except IOError:
			print("cannot convert", filename)
			success_changing_file = True
		filename = newfilename + ".png"
	return filename, error

# combines two bounding boxes into one bigger
def link_bounding_boxes(a, b):

	return (min(a[0],b[0]),min(a[1],b[1]),max(a[2],b[2]),max(a[3],b[3]))

# Runs the imagemagick script to obtain the bounding boxes
def run_imagemagick_script(filename):
	
	dir_path = os.path.dirname(os.path.realpath(__file__))
	out = subprocess.getoutput(shlex.quote(dir_path+"/imagemagick_script.sh") + " " + filename)
	cwd = os.getcwd()
	# png file created when running shell script, not necessary after that so it is removed
	os.remove(cwd+"/objects.png")
	return out 

# ToDo: add some conditions for bounding boxes, like not to long horizontally or vertically
def accept_bounding_box(bounding_box, black_pixels):
	
	# reject if to wide
	if(get_bounding_box_width(bounding_box) > 2*get_bounding_box_height(bounding_box)):
		return False;

	# reject if to high
	if(get_bounding_box_width(bounding_box)*20 < get_bounding_box_height(bounding_box)):
		return False;

	# reject if mostly whitespace
	if(float(black_pixels)/get_bounding_box_size(bounding_box) < 0.2):
		print("to much whitespace")
		return False;

	return True; 

def get_bounding_box_height(bounding_box):

	return bounding_box[3]-bounding_box[1]

def get_bounding_box_width(bounding_box):

	return bounding_box[2]-bounding_box[0]


def get_bounding_box_size(bounding_box):

	return (bounding_box[2]-bounding_box[0])*(bounding_box[3]-bounding_box[1])

# Extracts the bounding box from the shell script output
def get_bounding_box(shell_output):

	# The shell output = id: bounding-box centroid area
	boundry_list = []
	pixel_list = []

	# Optain list of bounding boxes and additional information
	split_up = re.split(":",shell_output)[1:]

	# Split the bounding box into tuple of rectangle coordinates: (left, upper, right, lower).
	# 0,0 is upper left corner.
	for sub in split_up[3:]:
		s = re.split("\s|x|\+",sub)[1:]
		item = (int(s[2]), int(s[3]), int(s[0]) + int(s[2]) , int(s[1]) + int(s[3]))

		if accept_bounding_box(item,int(s[7])):
			boundry_list.append(item)
			pixel_list.append(int(s[7]))

	boundry_list.sort(key=lambda x: get_bounding_box_size(x) ,reverse=True)
	boundry_list.sort(key=lambda x: x[0])
	boundry_list.sort(key=lambda x: x[1])

	return zip(boundry_list, pixel_list)

# Returns a list of pictures. Each picture is cropped from image using bounding box in the list
def get_cropped_pics(bounding_list,image):
	
	pic_list = []
	new_bounding_list = []

	for bounding in bounding_list:
		temp = image.crop(bounding)

		# cannot remove pictures after newline file is created
		'''
		black_amount = 0.0
		for i in range(0,temp.width):
			for j in range(0,temp.height):
				pixel = temp.getpixel((i,j))

				if(type(pixel) == tuple):
					if pixel[0] < 10:
						black_amount += 1
				else:
					if temp.getpixel((i,j)) < 10:
						black_amount += 1
					

		if black_amount / float(temp.height * temp.width) > 0.85:
			continue

		new_bounding_list.append(bounding)
		'''

		pic_list.append(temp)

	return pic_list, bounding_list

# Resize picture based on width and height
def resize_pic(pic,width,height):

	old_size = pic.size
	new_size = (max(old_size),max(old_size))
	new_pic = Image.new("RGB", new_size, color = (255,255,255))

	new_pic.paste(pic, (int((new_size[0]-old_size[0])/2),int((new_size[1]-old_size[1])/2)))

	return new_pic.resize((width,height));

# ToDo: Use thres in function
def threshold(pic,thres):

	# 0.5 is 127
	if(thres > 1):
		thres = 1
	if(thres < 0):
		thres = 0

	# remember that white is 255 and black is 0
	value = int(255*thres)
	gray = pic.convert('L')
	bw = gray.point(lambda x: 0 if x<value else 255, '1')

	return bw


def get_float(pic):

	gray = list(pic.convert('L').getdata())

	return [round(1.0-(g/255.0),1) for g in gray]

def get_float_list(picture_list,width,height):

	float_list = []
	for l in picture_list:
		float_list.append(get_float(resize_pic(l,width,height)))

	return float_list


# Gets binary value of one picture
def get_binary(pic, tresh_value=0.5):
	binary = list(threshold(pic,tresh_value).getdata())

	# black has the value 0, white has the value 255
	# binary values get 1 if black, 0 if white
	return [(1 if (b==0) else 0) for b in binary]

def print_binary(binary,width,height):
	
	for i in range(0,width*height,width):
		print(binary[i:i+width])

	return


# Gets binary value of every picture in list after resizing
def get_binary_list(picture_list,threshold,width,height):

	binary_lst = []
	for l in picture_list:
		binary_lst.append(get_binary(resize_pic(l,width,height),threshold))

	return binary_lst


def contains_box(containing_box, contained_box):
	if containing_box[0] < contained_box[0] and containing_box[1] < contained_box[1] and containing_box[2] > contained_box[2] and containing_box[3] > contained_box[3]:
		return True;
	return False;

def contained_in_box(bounding_box, bounding_list):
	for b in bounding_list:
		if contains_box(b,bounding_box):
			return True;

	return False;

def count_contained(bounding_box, bounding_list):
	contains = 0
	for b in bounding_list:
		if(contains_box(bounding_box,b)):
			contains += 1;
	return contains

def sieve_unwanted(bounding_pixel_list, document_size):

	new_list = []
	pixel_list = []

	for bounding_pixel in bounding_pixel_list:
		new_list.append(bounding_pixel[0])
		pixel_list.append(bounding_pixel[1])

	temp_list = new_list
	new_list = []

	for bounding in temp_list:
		contains = count_contained(bounding, temp_list)
		if(contains < 3):
			new_list.append(bounding)

	temp_list, new_list = new_list, []

	size_list = [get_bounding_box_size(t) for t in temp_list]
	average_size = sum(size_list)/len(size_list)

	for bounding in temp_list:
		if(not contained_in_box(bounding, temp_list) and (average_size*0.4 < get_bounding_box_size(bounding) and get_bounding_box_size(bounding) < average_size*9)):
			new_list.append(bounding)

	return new_list

def mark_bounding_boxes(filepath, bounding_list,directory):

	directory = directory + "/b_box"

	# check if directory exists and create one if not
	if not os.path.exists(directory):	
		os.makedirs(directory)

	path, filename = os.path.split(filepath)
	
	newfilename, filetype = os.path.splitext(filename)
	newfilename = directory + "/" + newfilename + ".png"

	copyfile(filepath,newfilename)

	im = Image.open(newfilename)
	im = im.convert('RGB',palette=Image.ADAPTIVE)
	
	drawing = ImageDraw.Draw(im)
	

	font = ImageFont.truetype(os.path.dirname(os.path.realpath(__file__)) + "/arial_cyr.ttf", 10)

	counter = 0
	for bounding_box in bounding_list:
		counter = counter + 1
		drawing.rectangle(bounding_box, fill=None, outline=(255,0,0))
		drawing.text((bounding_box[0],bounding_box[1]), str(counter), fill=(0,0,255), font=font)
	im.save(newfilename)

	im.close()

	return

def save_binary_to_file(binary_lst,filepath,directory):

	directory = directory+"/binary"

	# check if directory exists and create one if not
	if not os.path.exists(directory):	
		os.makedirs(directory)

	path, filename = os.path.split(filepath)
	newfilename, filetype = os.path.splitext(filename)

	bin_list = []
	for binary in binary_lst:
		bin_list.append(",".join(str(b) for b in binary))

	with open(os.path.join(directory,newfilename) + '.txt', mode='wt', encoding='utf-8') as myfile:
 		myfile.write('\n'.join(bin_list))

	return

def sort_bounding_list(bounding_list):

	bounding_list.sort(key=lambda x: get_bounding_box_size(x) ,reverse=True)
	bounding_list.sort(key=lambda x: x[0])
	bounding_list.sort(key=lambda x: x[1])

	box_left = 0
	ind_counter = 0
	index = []

	box_bottom = bounding_list[0][3]

	for b in bounding_list:
		if(b[1] > box_bottom):
			index.append(ind_counter)
			box_left = 0
			box_bottom = b[3]
		else:
			box_left = b[0]
		ind_counter += 1

	index.append(ind_counter)

	sublist_start = 0
	for i in index:
		sorted_list = sorted(bounding_list[sublist_start:i],key=lambda x: x[0])
		bounding_list = bounding_list[:sublist_start] + sorted_list + bounding_list[i:]
		sublist_start = i

	return bounding_list


def save_newline_to_file(bounding_list,filepath,directory):
	#Sort first by size, then by vertical position, then by horizontal position,

	#bounding box is tuple constisting of rectangle coordinates: (left, upper, right, lower)

	directory = directory+"/newline"

	# check if directory exists and create one if not
	if not os.path.exists(directory):	
		os.makedirs(directory)

	path, filename = os.path.split(filepath)
	newfilename, filetype = os.path.splitext(filename)
	
	box_left = 0
	ind_counter = 0
	index = []

	box_bottom = bounding_list[0][3]

	for b in bounding_list:
		if(b[1] > box_bottom):
			index.append(ind_counter)
			box_left = 0
			box_bottom = b[3]
		else:
			box_left = b[0]
		ind_counter += 1

	index.append(ind_counter)

	spaced_lines = []
	sublist_start = 0
	for i in index:
		sub_list = bounding_list[sublist_start:i]

		word_per_line = []
		word_len = 1
		for s in range(len(sub_list)-1):
			if get_bounding_box_width(sub_list[s])*0.5 < (sub_list[s+1][0] - sub_list[s][2]):  
				word_per_line.append(word_len)
				word_len = 0
			word_len += 1
		word_per_line.append(word_len)
		spaced_lines.append(word_per_line)

		sublist_start = i

	list_to_write = []
	for line in spaced_lines:
		list_to_write.append(",".join(str(l) for l in line))

	with open(os.path.join(directory,newfilename) + '.txt', mode='wt', encoding='utf-8') as myfile:
 		myfile.write('\n'.join(list_to_write))

	#return bounding_list