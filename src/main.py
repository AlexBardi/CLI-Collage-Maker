from contextlib import nullcontext
import re
import pyheif
import os, os.path
from PIL import Image
import argparse
import os

def import_pics(path, same_size=False, resize_param=False, new_size=(100,100)):
    imgs = []
    names = []
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        name = os.path.splitext(f)[0]
        ext = os.path.splitext(f)[1]

        if len(name) > 1 and same_size:
            continue

        if ext.lower() == ".heic":
            heif_file = pyheif.read(path + f)
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )

            if resize_param:
                image = image.resize(new_size)

            elif len(imgs) > 0 and same_size:
                image = image.resize(imgs[0].size)

            imgs.append(image)

        elif ext.lower() in valid_images:
            image = Image.open(os.path.join(path,f))

            if resize_param:
                image = image.resize(new_size)

            elif len(imgs) > 0 and same_size:
                image = image.resize(imgs[0].size)

            imgs.append(image)

        else:
            print("Warning:", name + ext, "is not one of the supported filetypes.")
            continue

        names.append(name) 

    return imgs, names

def singleCollage():

    print("This takes every image in your 'inputs' folder and makes a grid of each image")
    num_horiz = int(input("How many images across? "))
    num_vert = int(input("How many images tall? "))

    images, names = import_pics("./../inputs/")

    for image_single, name in zip(images, names):
        image_collage = Image.new("RGBA", (image_single.size[0] * num_horiz, image_single.size[1] * num_vert), "white")

        for i in range(num_horiz):
            for j in range(num_vert): 
                image_collage.paste(image_single, (i * image_single.size[0], j * image_single.size[1]))

        image_collage.save("./../outputs/" + name + "-" + str(num_horiz) + "x" + str(num_vert) + ".png")
    
    return


def multiCollage(args):
    grid = []

    if args.file == None:
        print("Put the files that you want to collage in the 'inputs' file.")
        print("Give them all single letter names.")
        print("If you type 'x', that space will be left blank.")
        print("Write out the pattern of letters that defines your grid:")

        while (line := input("> ")) != '':
            grid.append(line)
            if len(line) != len(grid[0]):
                print("Each row must have the same dimensions")
                return
    else: 
        pattern_file = open(args.file[0])
        for line in pattern_file:
            grid.append(line.strip())
        

    if args.size == None:
        images, names = import_pics("./../inputs/", same_size=True)
    else:
        images, names = import_pics("./../inputs/", resize_param=True, new_size=args.size)

    if len(grid) == 0:
        return

    num_horiz = len(grid[0])
    num_vert = len(grid)

    image_collage = Image.new("RGBA", (images[0].size[0] * num_horiz, images[0].size[1] * num_vert), "white")

    for i in range(num_horiz):
        for j in range(num_vert): 
            img_name = grid[j][i]
            if img_name == 'x':
                continue
            idx = names.index(img_name)
            image_single = images[idx]
            image_collage.paste(image_single, (i * image_single.size[0], j * image_single.size[1]))

    image_collage.save("./../outputs/" + "custom-collage" + ".png")

    return

def main():

    parser = argparse.ArgumentParser(description = "A simple collage maker")
 
    parser.add_argument("-p", "--pattern", action='store_true',
                        help = "Creating a collage of multiple images")
    parser.add_argument("-s", "--size", type = int, nargs = 2,
                        metavar = ('height','width'), help = "The height and \
                        width of every image in the collage")
    parser.add_argument("-f", "--file", type = str, nargs = 1,
                        metavar = 'pattern_path', help = "A file containing \
                        a multiple image collage pattern")
    args = parser.parse_args()

    if args.pattern == True:
        multiCollage(args)
    else:
        singleCollage()

    
if __name__=="__main__":
    main()

