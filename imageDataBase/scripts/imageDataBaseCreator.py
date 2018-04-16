import os
import getopt
import sys
from PIL import Image

opts, args = getopt.getopt(sys.argv[1:], 'd:o:f:w:h:p:')
 
directory = ''
outputDir = ''
fileName = ''
width = -1
height = -1
padVal = -1

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

if fileName == '' or directory == '' or outputDir == '':
    print('Invalid command line arguments. -d [input image directory] ' \
          '-o [output image directory] -f [new image file name] are required '\
	      '-w [resize width] -h [resize height] -p [padding value] are optional')
    exit()

width = str(width)
height = str(height)
padVal = str(padVal)

os.system('python step-1.py -d '+directory+' -o '+outputDir+' -f '+fileName +' -w '+ width +' -h '+height+' -p' +padVal);
os.system('python step-2.py -d '+outputDir+' -f tag_file_name.txt');
os.system('python step-3.py -l script-labels.txt -t CSV_tag_file_name.txt >> '+fileName+'-val.txt');

from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    print('Linux Detected')
    os.system('rm -rf tag_file_name.txt CSV_tag_file_name.txt');
elif _platform == "win32" or _platform == "win64":
    print('Windows Detected')
    os.system('DEL tag_file_name.txt CSV_tag_file_name.txt');
    os.system('rm -rf tag_file_name.txt CSV_tag_file_name.txt');