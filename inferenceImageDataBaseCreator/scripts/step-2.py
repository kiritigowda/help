import os
import getopt
import sys
from PIL import Image

opts, args = getopt.getopt(sys.argv[1:], 'd:f:')
 
directory = ''
fileName = ''

for opt, arg in opts:
    if opt == '-d':
        directory = arg
    elif opt == '-f':
        fileName = arg

if fileName == '' or directory == '':
    print('Invalid command line arguments. -d [input image directory] ' \
          '-f [Tag file name] are required')
    exit()


for image in sorted(os.listdir(directory)):
    print('Writing Tags Image ' + image)
    os.system('exiftool -m -filename -subject -s -s -s -t '+ directory + image + ' >> ' + fileName);


from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    print('Linux Detected')
    os.system('awk \'sub("\t", ",")\' ' + fileName +' >> ' + 'CSV_'+fileName)
elif _platform == "win32" or _platform == "win64":
    print('Windows Detected')
    os.system('gawk \'sub("\t", ",")\' ' + fileName +' >> ' + 'CSV_'+fileName)

print('Image Tag List Generation Complete.')
