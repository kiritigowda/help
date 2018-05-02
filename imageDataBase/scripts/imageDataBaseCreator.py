import os
import getopt
import sys
from PIL import Image

opts, args = getopt.getopt(sys.argv[1:], 'd:o:f:w:h:p:c:')
 
directory = ''
outputDir = ''
fileName = ''
width = ''
height = ''
padVal = ''
count = ''

for opt, arg in opts:
    if opt == '-d':
        directory = arg
    elif opt == '-o':
        outputDir = arg
    elif opt == '-f':
        fileName = arg
    elif opt == '-w':
        width = arg
    elif opt == '-h':
        height = arg
    elif opt == '-p':
        padVal = arg
    elif opt == '-c':
        count = arg

if width == '':
    width = '-1'
if height == '':
    height = '-1'
if padVal == '':
    padVal = '-1'
if count == '':
    count = '-1'

if fileName == '' or directory == '' or outputDir == '':
    print('Invalid command line arguments. -d [input image directory] ' \
          '-o [output image directory] -f [new image file name] are required '\
	      '-w [resize width] -h [resize height] -p [padding value] -c [image start number] are optional')
    exit()

logDir = fileName+'-scriptOutput'

os.system('python step-1.py -d '+directory+' -o '+outputDir+' -f '+fileName +' -w '+ width +' -h '+height+' -p ' +padVal+' -c ' +count);
os.system('python step-2.py -d '+outputDir+' -f tag_file_name.txt');
os.system('python step-3.py -l script-labels.txt -t CSV_tag_file_name.txt >> '+fileName+'-val.txt');

from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    print('Linux Detected')
    os.system('rm -rf tag_file_name.txt output.log');
    os.system('mv CSV_tag_file_name.txt '+logDir+'/CSV_tag_file_name.csv');
    os.system('cp '+fileName+'-val.txt '+logDir+'/'+fileName+'-val.txt');
elif _platform == "win32" or _platform == "win64":
    print('Windows Detected')
    os.system('DEL tag_file_name.txt output.log');
    os.system('rm -rf tag_file_name.txt output.log');
    os.system('mv CSV_tag_file_name.txt '+logDir+'/CSV_tag_file_name.csv');
    os.system('cp '+fileName+'-val.txt '+logDir+'/'+fileName+'-val.txt');

# generate error reports
orig_stdout = sys.stdout
sys.stdout = open(logDir+'/'+fileName+'-fileNameWithLabels.csv','a')
print('Old FileName, New FileName, Labels')
sys.stdout = open(logDir+'/'+fileName+'-fileNameErrors.csv','a')
print('Old FileName, New FileName')
sys.stdout = open(logDir+'/'+fileName+'-filesWithMultipleLabels.csv','a')
print('Old FileName, New FileName, Labels')

# generate reports for images with and without labels
with open(logDir+'/'+fileName+'-Translation.csv') as orig_filename:
    for file in orig_filename:
        fileList = file.strip().split(",")
        imgFileCount = 0
        sys.stdout = open(logDir+'/'+fileName+'-fileNameWithLabels.csv','a')
        with open(logDir+'/CSV_tag_file_name.csv') as tagFile:
            for tag in tagFile:
                tagList = tag.strip().split(",")
                #print(fileList[1], tagList[0] )
                fileList[1] = fileList[1].strip()
                tagList[0] = tagList[0].strip()
                
                if fileList[1] == tagList[0]:
                    imgFileCount += 1
                    tag = tag.strip()
                    print(fileList[0]+','+tag)

        if imgFileCount == 0:
            sys.stdout = open(logDir+'/'+fileName+'-fileNameErrors.csv','a')
            print(fileList[0]+','+fileList[1])

# generate report for multiple labels for single image
with open(logDir+'/'+fileName+'-Translation.csv') as orig_filename:
    for file in orig_filename:
        fileList = file.strip().split(",")
        multipleLabelFlag = 0
        imgFileCount = 0
        sys.stdout = open(logDir+'/'+fileName+'-fileNameWithLabels.csv','a')
        with open(logDir+'/'+fileName+'-val.txt') as tagFile:
            for tag in tagFile:
                tagList = tag.strip().split(" ")
                fileList[1] = fileList[1].strip()
                tagList[0] = tagList[0].strip()

                if fileList[1] == tagList[0]:
                    imgFileCount += 1

                if imgFileCount > 1:
                    imgFileCount = 0
                    sys.stdout = open(logDir+'/'+fileName+'-filesWithMultipleLabels.csv','a')
                    print(fileList[0]+','+tagList[0]+','+tagList[1])
