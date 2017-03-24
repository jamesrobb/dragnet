#!/bin/bash

# arguments are:
# source_imgs_dir
# matrices_lables_output_dir
# final_documents_dir

if [ "$#" -ne 3 ]; then
	echo "usage: [source_imgs_dir] [matrices_lables_output_dir] [final_documents_dir]"
	exit
fi

if ! [ -d "$2" ]; then
	mkdir "$2"
fi

if ! [ -d "$2/matrices" ]; then
	mkdir "$2/matrices"
fi

if ! [ -d "$2/newline" ]; then
	mkdir "$2/newline"
fi

if ! [ -d "$3" ]; then
	mkdir "$3"
fi

if ! [ -d "$3/output_labels" ]; then
	mkdir "$3/output_labels"
fi

echo "extracting characters"

for file in "$1"/*; do
	if [ -f "$file" ]; then
		echo $file
		./extract_characters.py "$file" "$2"
	fi
done

echo "feeding extractions to neural network"

for file in "$2/matrices/"*; do
	if [ -f "$file" ]; then
		echo $file
		file_base=$(basename "$file")
		./dragnet_nn_solve.py "$file" "$3/output_labels/$file_base"
		./generate_document_from_labels.py "$3/output_labels/$file_base" "$2/newline/$file_base" "$3/$file_base"
	fi
done	