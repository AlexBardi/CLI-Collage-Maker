import pyheif
from PIL import Image

def main():
    # pyheif.open_container("./../img/IMG_7157.HEIC")
    heif_file = pyheif.read("./../img/IMG_2328.heic")
    image = Image.frombytes(
    heif_file.mode, 
    heif_file.size, 
    heif_file.data,
    "raw",
    heif_file.mode,
    heif_file.stride,
    )

if __name__=="__main__":
    main()
