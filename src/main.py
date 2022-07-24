import pyheif
import os, os.path
from PIL import Image

def import_pics(path):
    imgs = []
    names = []
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        name = os.path.splitext(f)[0]
        ext = os.path.splitext(f)[1]
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
            imgs.append(image)
        elif ext.lower() not in valid_images:
            continue
        else:
            imgs.append(Image.open(os.path.join(path,f)))

        names.append(name) 
    return imgs, names

def main():
    images, names = import_pics("./../inputs/")

    num_horiz = int(input("How many images across? "))
    num_vert = int(input("How many images tall? "))

    for image_single, name in zip(images, names):
        image_collage = Image.new("RGBA", (image_single.size[0] * num_horiz, image_single.size[1] * num_vert), "white")

        for i in range(num_horiz):
            for j in range(num_vert): 
                image_collage.paste(image_single, (i * image_single.size[0], j * image_single.size[1]))

        image_collage.save("./../outputs/" + name + "-" + str(num_horiz) + "x" + str(num_vert) + ".png")


if __name__=="__main__":
    main()
