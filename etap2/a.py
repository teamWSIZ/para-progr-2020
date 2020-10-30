# https://github.com/VingtCinq/python-resize-image
from PIL import Image
from resizeimage import resizeimage


def shrink(path, file, file_small, width=600):
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_width(image, width)
            cover.save(path + file_small, image.format)


shrink('./', 'image.png', 'sm_image.png', 300)
