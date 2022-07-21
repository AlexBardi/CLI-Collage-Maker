import pyheif
from PIL import Image

def main():
    images = []

    images.append(Image.open("./../img/IMG_7156.PNG"))

    names = ["IMG_4164", "IMG_7157 2"]

    for name in names:
        fullpath = "./../img/" + name + ".heic"

        heif_file = pyheif.read(fullpath)
        image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )

        images.append(image)

    num_horiz = 5
    num_vert = 10

    for image_single in images:
        image_collage = Image.new("RGB", (image_single.size[0] * num_horiz, image_single.size[1] * num_vert), "white")

        for i in range(num_horiz):
            for j in range(num_vert): 
                image_collage.paste(image_single, (i * image_single.size[0], j * image_single.size[1]))

        image_collage.show()


if __name__=="__main__":
    main()
