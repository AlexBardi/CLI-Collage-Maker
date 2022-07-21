import pyheif
from PIL import Image

def main():
    image_single = Image.open("./../img/car.png") 

    num_horiz = 5
    num_vert = 10

    image_collage = Image.new("RGB", (image_single.size[0] * num_horiz, image_single.size[1] * num_vert), "white")

    for i in range(num_horiz):
        for j in range(num_vert): 
            image_collage.paste(image_single, (i * image_single.size[0], j * image_single.size[1]))

    image_collage.show()


if __name__=="__main__":
    main()
