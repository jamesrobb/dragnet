#!/usr/bin/python3
# Given a file that contains labels from dragnet, translate to a document

import argparse

alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя1234567890"

def main(labels_file,newline_file,destination_file):

	fh = open(labels_file)
	nf = open(newline_file)
	
	new_line_array = []
	while True:

		char_in_line = nf.readline().rstrip("\n")
		if char_in_line == "":
			break

		new_line_array.append([int(c) for c in char_in_line.split(",")])

	string = ""
	while True:

		label = fh.readline().rstrip("\n")
		if label == "":
			break

		string += alphabet[int(label)]

	fh.close()
	nf.close()

	char_lines = []
	k = 0
	for line in new_line_array:
		for i in line:
			print(string[k:k+i])
			char_lines.append(string[k:k+i]+ " ")
			k += i
		char_lines.append("\n")

	fn_output = open(destination_file, 'w')

	for l in char_lines:
		fn_output.write(l)

	fn_output.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("labels_file", help="source of labels")
	parser.add_argument("newline_file", help="source of document layout")
	parser.add_argument("destination_file", help="destination of document")
	args = parser.parse_args()

	main(args.labels_file,args.newline_file,args.destination_file)