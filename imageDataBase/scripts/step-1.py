import os
import getopt
import sys
from PIL import Image


def make_square_image(img, width, height, padVal):
    x, y = img.size
    fill_color=(padVal, padVal, padVal, padVal)
    min_size=224
    size = max(min_size, x, y)
    new_img = Image.new('RGBA', (size, size), fill_color)
    new_img.paste(img, ((size - x) / 2, (size - y) / 2))
    new_img = new_img.resize((width, height), Image.BILINEAR)
    new_img = new_img.convert("RGB")
    return new_img

opts, args = getopt.getopt(sys.argv[1:], 'd:o:f:w:h:p:c:')
 
directory = ''
outputDir = ''
fileName = ''
width = -1
height = -1
padVal = -1
userCount = -1

for opt, arg in opts:
    if opt == '-d':
        directory = arg
    elif opt == '-o':
        outputDir = arg
    elif opt == '-f':
        fileName = arg
    elif opt == '-w':
        width = int(arg)
    elif opt == '-h':
        height = int(arg)
    elif opt == '-p':
        padVal = int(arg)
    elif opt == '-c':
        userCount = int(arg)

if fileName == '' or directory == '' or outputDir == '':
    print('Invalid command line arguments. -d [input image directory] ' \
          '-o [output image directory] -f [new image file name] are required '\
	      '-w [resize width] -h [resize height] -p [padding value] -c [image start count]are optional')
    exit()

count = 0
if userCount != -1:
    count = userCount

size = width, height 

for image in sorted(os.listdir(directory)):
    print('Processing Image ' + image)
 
    img = Image.open(os.path.join(directory, image))

    if width != -1 and height != -1:
        if padVal != -1:
            img = make_square_image(img,width,height,padVal)
        else:
            img = img.resize((width, height), Image.BILINEAR)


    if count < 10:
        img.save( outputDir + fileName + '_000' + str(count) + '.JPEG')
        os.system('exiftool -m -TagsFromFile '+ directory + image + ' ' + outputDir + fileName + '_000' + str(count) + '.JPEG');
    elif count > 9 and count < 100:
        img.save( outputDir + fileName + '_00' + str(count) + '.JPEG')
        os.system('exiftool -m -TagsFromFile '+ directory + image + ' ' + outputDir + fileName + '_00' + str(count) + '.JPEG');
    elif count > 99 and count < 1000:
        img.save( outputDir + fileName + '_0' + str(count) + '.JPEG')
        os.system('exiftool -m -TagsFromFile '+ directory + image + ' ' + outputDir + fileName + '_0' + str(count) + '.JPEG');
    elif count > 999 and count < 10000:
        img.save( outputDir + fileName + '_' + str(count) + '.JPEG')
        os.system('exiftool -m -TagsFromFile '+ directory + image + ' ' + outputDir + fileName + '_' + str(count) + '.JPEG');

    count += 1


from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    print('Linux Detected')
    os.system('rm -rf '+ outputDir + '*.JPEG_original');
elif _platform == "win32" or _platform == "win64":
    print('Windows Detected')
    os.system('DEL '+ outputDir + '*.JPEG_original');
    os.system('rm -rf '+ outputDir + '*.JPEG_original');

print('Image resize and name change complete.')
