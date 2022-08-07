import os
from PIL import Image

path = os.getcwd()
filename = os.listdir(path)
# print(filename)
width = 295
height = 413

for img in filename:
    if (img[-4:]) == '.JPG':
        print(img)
        pic = Image.open(img)
        print(pic)
        newpic = pic.resize((width, height), Image.ANTIALIAS)
        print(newpic)
        newpic.save(img,dpi=(300.0,300.0))
        # image = Image.open(base_dir + img)
        # image_size = image.resize((size_m, size_n), Image.ANTIALIAS)
