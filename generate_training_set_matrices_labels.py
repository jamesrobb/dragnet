#!/usr/bin/python3

import os
import sys
import argparse
from blockifier import extract_char
from PIL import Image

def main(source_directory, matrices_file, labels_file):

    b_file = open(matrices_file, 'w')
    l_file = open(labels_file, 'w')

    alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя1234567890"
    alphabet_dict = {}
    
    for i in range(0, len(alphabet)):
        alphabet_dict[alphabet[i]] = i

    for img_path in os.listdir(source_directory):
        period_pos = img_path.rfind('.')
        char = img_path[period_pos-1:period_pos]
        img_path = os.path.join(source_directory, img_path)
        img = Image.open(img_path)
        
        binary_to_write = ",".join([str(x) for x in extract_char.get_float(img)])
        label = [0] * len(alphabet)
        label[alphabet_dict[char]] = 1
        label_to_write = ",".join([str(x) for x in label])

        b_file.write(binary_to_write + "\n")
        l_file.write(label_to_write + "\n")
        #binary = extract_char.get_binary(img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_directory", help="source of images")
    parser.add_argument("matrices_file", help="file to write matrices to")
    parser.add_argument("labels_file", help="file to write labels to")
    args = parser.parse_args()

    main(args.source_directory, args.matrices_file, args.labels_file)