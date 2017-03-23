import os
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageDraw

def generate_from_ttf_list(TTFList, directory):
    alphabet = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя1234567890"

    black = (0,0,0)
    for fontface in TTFList:
        for c in alphabet:
            img = Image.new('RGB', (120, 120), "white")
            draw = ImageDraw.Draw(img)
            csize = draw.textsize(c, font=fontface[1])
            draw.text(((img.size[0]-csize[0])/2, (img.size[1]-csize[1])/2 - 5), c, black, font=fontface[1])
            name = directory+"/"+fontface[0]+"-"+c+".png"
            img.save(name, "PNG")


def blur_directory(directory): 
    for imgpath in os.listdir(directory):
        if not imgpath.endswith(".png"):
            continue
        imgpath = directory+"/"+imgpath
        img = Image.open(imgpath)
        img = img.filter(ImageFilter.GaussianBlur(1))
        periodPos = imgpath.rfind('.')
        imgpath = imgpath[:periodPos-1] + "blurred-" + imgpath[periodPos-1:]
        img.save(imgpath)


def shear_directory(directory):
    for imgpath in os.listdir(directory):
        if not imgpath.endswith(".png"):
            continue
        imgpath = directory+"/" + imgpath
        img = Image.open(imgpath)
        sheares = [-0.5, 0.5]
        for k in sheares:
            img2 = img.convert("RGBA")
            width, height = img.size
            m = k
            xshift = width
            new_width = width + int(round(xshift))
            sheared = img2.transform((new_width, height), Image.AFFINE, (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BILINEAR)
            fff = Image.new("RGBA", sheared.size, (255,)*4)
            out = Image.composite(sheared, fff, sheared)
            periodPos = imgpath.rfind('.')
            imgpathsheared = imgpath[:periodPos-1] + "(" + str(k) + "sheared)-" + imgpath[periodPos-1:]
            out.convert(img.mode).save(imgpathsheared)


def rotate_directory(directory):
    for imgpath in os.listdir(directory):
        if not imgpath.endswith(".png"):
            continue
        imgpath = directory+"/"+imgpath
        img = Image.open(imgpath)
        rotations = [-15, -7, 7, 15]
        for rotation in rotations:
            # converted to have an alpha layer
            img2 = img.convert('RGBA')
            # rotated image
            rot = img2.rotate(rotation)
            # a white image same size as rotated image
            fff = Image.new('RGBA', rot.size, (255,)*4)
            # create a composite image using the alpha layer of rot as a mask
            out = Image.composite(rot, fff, rot)
            # fixing the name and saving
            periodPos = imgpath.rfind('.')
            imgpathrot = imgpath[:periodPos-1] +"("+ str(rotation)+ ")-" + imgpath[periodPos-1:]
            out.convert(img.mode).save(imgpathrot)
      

def remove_whitespace_from_directory(directory):
    white = (255,255,255)
    for imgpath in os.listdir(directory):
        if not imgpath.endswith(".png"):
            continue
        imgpath = directory+"/"+imgpath
        img = Image.open(imgpath)
        draw = ImageDraw.Draw(img)
        pixels = img.load()
        leftmost = 1000
        rightmost = -1
        topmost = 1000
        bottommost = -1
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                if(pixels[x, y] != white and topmost > y):
                    topmost = y
                if(pixels[x, y] != white and x < leftmost):
                    leftmost = x
                if(pixels[x, y] != white and x > rightmost):
                    rightmost = x
                if(pixels[x, y] != white and y > bottommost):
                    bottommost = y
        horizontal = (rightmost - leftmost)
        vertical = (bottommost - topmost)
        if(horizontal != vertical):
            bigside = max(horizontal, vertical)
            centerhor = leftmost + horizontal / 2
            centervert = topmost + vertical / 2
            toAdd = int(bigside/2)
            leftmost = centerhor - toAdd
            rightmost = centerhor + toAdd
            topmost = centervert - toAdd
            bottommost = centervert + toAdd
        img = img.crop((int(leftmost), int(topmost), int(rightmost), int(bottommost)))
        #draw.rectangle((leftmost,topmost, rightmost, bottommost), outline=128)
        name = imgpath
        img = img.resize((30,30), resample=Image.LANCZOS)
        img.save(name, "PNG")