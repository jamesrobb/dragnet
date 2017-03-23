#!/usr/bin/python3

import os
import sys
from PIL import ImageFont

from training_set_generator.training_set_generator import *

if len(sys.argv) < 3:
    print("Not enough arguements")
    print("Usage: python file (dir of fonts) (dir of img of characters)")
    exit();

sys.argv[1] = sys.argv[1][:-1] if sys.argv[1][-1] == '/' else sys.argv[1]
sys.argv[2] = sys.argv[2][:-1] if sys.argv[2][-1] == '/' else sys.argv[2]

print("Do you want to delete everything in ", sys.argv[2], " and refill it with character images? (y/n)")
delete = input()

if delete == "y":
    os.popen("rm "+sys.argv[2]+"/*.png")
    fontlist = []
    for font in os.listdir(sys.argv[1]):
        if not font.endswith((".ttf", ".ttc", ".otf")):
            continue
        periodPos = font.rfind(".")
        actualFont = sys.argv[1]+"/"+font
        fontNoTtf = font[:periodPos]
        fontlist.append((fontNoTtf, ImageFont.truetype(actualFont, 64)))
    generate_from_ttf_list(fontlist, sys.argv[2])

shear_directory(sys.argv[2])
remove_whitespace_from_directory(sys.argv[2])
rotate_directory(sys.argv[2])
blur_directory(sys.argv[2])
