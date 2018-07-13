import os
import getopt
import sys
import random
import collections
import csv
import numpy

opts, args = getopt.getopt(sys.argv[1:], 'i:d:l:h:o:f:')

inputCSVFile = '';
inputImageDirectory = '';
labelFile = '';
hierarchyFile = '';
outputDirectory = '';
fileName = '';

for opt, arg in opts:
    if opt == '-i':
        inputCSVFile = arg;
    elif opt == '-d':
        inputImageDirectory = arg;
    elif opt == '-l':
        labelFile = arg;
    elif opt == '-h':
        hierarchyFile = arg;
    elif opt == '-o':
        outputDirectory = arg;
    elif opt == '-f':
        fileName = arg;

# report error
if inputCSVFile == '' or inputImageDirectory == '' or labelFile == '' or outputDirectory == '' or fileName == '':
    print('Invalid command line arguments.\n'
        '\t\t\t\t-i [input Result CSV File - required](File Format:ImgFileName, GroundTruth, L1, L2, L3, L4, L5, P1, P2, P3, P4, P5)[L:Label P:Probability]\n'\
        '\t\t\t\t-d [input Image Directory - required]\n'\
        '\t\t\t\t-l [input Label File - required]\n'\
        '\t\t\t\t-h [input Hierarchy File - optional]\n'\
        '\t\t\t\t-o [output Directory - required]\n'\
        '\t\t\t\t-f [output file name - required]\n')
    exit();

if not os.path.exists(inputImageDirectory):
    print "ERROR Invalid Input Image Directory";
    exit();

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory);

# read results.csv
numElements = 0;
with open(inputCSVFile) as resultFile:
    resultCSV = csv.reader(resultFile)
    next(resultCSV) # skip header
    resultDataBase = [r for r in resultCSV]
    numElements = len(resultDataBase)

# read labels.txt
labelElements = 0
with open(labelFile) as labels:
    LabelLines = labels.readlines()
    labelElements = len(LabelLines)

# read hieararchy.csv
hierarchySection = 0
if hierarchyFile != '':
    hierarchySection = 1
    hierarchyElements = 0
    with open(hierarchyFile) as hierarchy:
        hierarchyCSV = csv.reader(hierarchy)
        hierarchyDataBase = [r for r in hierarchyCSV]
        hierarchyElements = len(hierarchyDataBase)

    if hierarchyElements != labelElements:
        print "ERROR Invalid Hierarchy file / label File";
        exit();

# create toolkit with icons and images
toolKit_Dir = outputDirectory +'/'+ fileName + '-toolKit'
toolKit_dir = os.path.expanduser(toolKit_Dir)
if not os.path.exists(toolKit_dir):
    os.makedirs(toolKit_dir);

from distutils.dir_util import copy_tree
# copy subdirectory example
fromDirectory = inputImageDirectory;
toDirectory = toolKit_Dir+'/images';
copy_tree(fromDirectory, toDirectory)

# generate detailed results.csv
print "results.csv generation .."
orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/results.csv','w')
print 'Image,Ground Truth, Top 1 Label, Match, Top 1 Confidence, Ground Truth Text, Top 1 Label Text'
for x in range(numElements):
    gt = int(resultDataBase[x][1]);
    lt = int(resultDataBase[x][2]);
    matched = 'no';
    if gt == lt:
         matched = 'yes';

    print ''+(resultDataBase[x][0])+','+(resultDataBase[x][1])+','+(resultDataBase[x][2])+','+(matched)+','\
            +(resultDataBase[x][7])+',"'+(LabelLines[int(resultDataBase[x][1])].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[int(resultDataBase[x][2].rstrip('\n'))].split(' ', 1)[1].rstrip('\n'))+'"'

sys.stdout = orig_stdout
print "results.csv generated"

# generate results summary.csv
top1TotProb = top2TotProb = top3TotProb = top4TotProb = top5TotProb = totalFailProb = 0;
top1Count = top2Count = top3Count = top4Count = top5Count = 0;
totalNoGroundTruth = totalMismatch = 0;

topKPassFail = [];
topKHierarchyPassFail = [];
topLabelMatch = [];
w, h = 100, 2;
topKPassFail = [[0 for x in range(w)] for y in range(h)]
w, h = 100, 12;
topKHierarchyPassFail = [[0 for x in range(w)] for y in range(h)]
w, h = 1000, 7;
topLabelMatch = [[0 for x in range(w)] for y in range(h)] 

exit(0)
