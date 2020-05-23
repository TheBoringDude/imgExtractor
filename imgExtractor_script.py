from PIL import Image
from PIL.ExifTags import TAGS

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

exif = get_exif('test.jpg') # change the filename
labeled = get_labeled_exif(exif)
labeled.pop('UserComment', None)
print(type(labeled))
for x in labeled:
    try:
        if isinstance(labeled[x], (bytes, bytearray)):
            labeled[x] = labeled[x].decode()
        print(x, ":" , labeled[x])
    except UnicodeDecodeError:
        pass