# https://github.com/VingtCinq/python-resize-image
from PIL import Image
from resizeimage import resizeimage


def fix_width(path, file, file_small, width=600):
    # height auto-adjusted, ratio preserved
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            res = resizeimage.resize_width(image, width)
            res.save(path + file_small, image.format)


def cover(path, file, file_small, height=320, width=200):
    # will resample if needed to get required size, ratio preserved
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            print(image.size)
            res = resizeimage.resize_cover(image, (height, width))
            print(res.size)
            res.save(path + file_small, image.format)


def thumb(path, file, file_small, height=320, width=200):
    # preserves ratio, no crop, trying best to match height/width
    with open(path + file, 'r+b') as f:
        with Image.open(f) as image:
            print(image.size)
            res = resizeimage.resize_thumbnail(image, (height, width))
            print(res.size)
            res.save(path + file_small, image.format)


# cover('../etap2/', 'plasma.png', 'sm_image.png', 320, 200)
# fix_width('../etap3/', 'plasma.png', 'sm_plasma.png', 200)
thumb('../etap3/', 'plasma.png', 'sm_plasma.png', 320, 200)
