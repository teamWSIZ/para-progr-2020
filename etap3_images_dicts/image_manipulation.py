# https://github.com/VingtCinq/python-resize-image
from PIL import Image, ImageEnhance
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
            # res = res.convert('LA')
            res = res.rotate(45)
            res.save(path + file_small, image.format)

def sharpness(file):
    # preserves ratio, no crop, trying best to match height/width
    with open(file, 'r+b') as f:
        with Image.open(f) as image:
            print(image.size)
            enhancer = ImageEnhance.Sharpness(image)
            for i in range(8):
                factor = i / 4.0
                res = enhancer.enhance(factor)
                res.save(f's{factor}.png', image.format)



# cover('../etap3_images_dicts/', 'plasma.png', 'sm_plasma.png', 300, 300)
# fix_width('../etap3_images_dicts/', 'plasma.png', 'sm_plasma.png', 200)
# thumb('../etap3_images_dicts/', 'plasma.png', 'sm_plasma.png', 320, 200)

sharpness('/plasma.png')

