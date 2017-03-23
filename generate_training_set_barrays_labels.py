#!/usr/bin/python3

import os
import sys
from blockifier import extract_char
from PIL import Image

def images_to_binary_arrays(source_directory, barrays_file, labels_file):

    b_file = open(barrays_file, 'w')
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

if len(sys.argv) < 4:
    print("Not enough arguements")
    print("Usage: python file (source dir) (barrays file) (character file)")
    exit()

sys.argv[1] = sys.argv[1][:-1] if sys.argv[1][-1] == '/' else sys.argv[1]
sys.argv[2] = sys.argv[2][:-1] if sys.argv[2][-1] == '/' else sys.argv[2]
sys.argv[3] = sys.argv[3][:-1] if sys.argv[3][-1] == '/' else sys.argv[3]
images_to_binary_arrays(sys.argv[1], sys.argv[2], sys.argv[3])