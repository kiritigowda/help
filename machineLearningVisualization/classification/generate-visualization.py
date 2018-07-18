__author__      = "Kiriti Nagesh Gowda"
__copyright__   = "Copyright 2018, AMD Dataset Analysis Tool"
__credits__     = ["Mike Schmit"]
__license__     = "MIT"
__version__     = "0.9.0"
__maintainer__  = "Kiriti Nagesh Gowda"
__email__       = "Kiriti.NageshGowda@amd.com"
__status__      = "Alpha"

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
# copy images and icons
from distutils.dir_util import copy_tree
fromDirectory = inputImageDirectory;
toDirectory = toolKit_Dir+'/images';
copy_tree(fromDirectory, toDirectory)

dir_path = os.path.dirname(os.path.realpath(__file__))
fromDirectory = dir_path+'/icons';
toDirectory = toolKit_Dir+'/icons';
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


topKPassFail = []
topKHierarchyPassFail = []
for i in xrange(100):
    topKPassFail.append([])
    topKHierarchyPassFail.append([])
    for j in xrange(2):
        topKPassFail[i].append(0)
    for k in xrange(12):
        topKHierarchyPassFail[i].append(0)


topLabelMatch = []
for i in xrange(1000):
    topLabelMatch.append([])
    for j in xrange(7):
        topLabelMatch[i].append(0)

# Generate Comphrehensive Results
print "resultsComphrehensive.csv generation .."
orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/resultsComphrehensive.csv','w')
print(  'FileName,outputLabel-1,outputLabel-2,outputLabel-3,outputLabel-4,outputLabel-5,'\
        'groundTruthLabel,Matched,outputLabelText-1,outputLabelText-2,outputLabelText-3,outputLabelText-4,outputLabelText-5,'\
        'groundTruthLabelText,Prob-1,Prob-2,Prob-3,Prob-4,Prob-5' );
imageDataSize = numElements;
for x in range(numElements):
    truth = int(resultDataBase[x][1]);
    if truth >= 0:
        match = 0;
        label_1 = int(resultDataBase[x][2]);
        label_2 = int(resultDataBase[x][3]);
        label_3 = int(resultDataBase[x][4]);
        label_4 = int(resultDataBase[x][5]);
        label_5 = int(resultDataBase[x][6]);
        prob_1 = float(resultDataBase[x][7]);
        prob_2 = float(resultDataBase[x][8]);
        prob_3 = float(resultDataBase[x][9]);
        prob_4 = float(resultDataBase[x][10]);
        prob_5 = float(resultDataBase[x][11]);

        if(truth == label_1):
            match = 1; 
            top1Count+= 1;
            top1TotProb += prob_1;
            topLabelMatch[truth][0]+= 1;
            topLabelMatch[truth][1]+= 1;

        elif(truth == label_2):
            match = 2; 
            top2Count+= 1;
            top2TotProb += prob_2;
            topLabelMatch[truth][0]+= 1;
            topLabelMatch[truth][2]+= 1;

        elif(truth == label_3):
            match = 3; 
            top3Count+= 1; 
            top3TotProb += prob_3;
            topLabelMatch[truth][0]+= 1;
            topLabelMatch[truth][3]+= 1;

        elif(truth == label_4):
            match = 4;
            top4Count+= 1;
            top4TotProb += prob_4;
            topLabelMatch[truth][0]+= 1;
            topLabelMatch[truth][4]+= 1;

        elif(truth == label_5):
            match = 5; 
            top5Count+= 1;
            top5TotProb += prob_5;
            topLabelMatch[truth][0]+= 1;
            topLabelMatch[truth][5]+= 1;

        else:
            totalMismatch+= 1;
            totalFailProb += prob_1;
            topLabelMatch[truth][0]+= 1;


        if(truth != label_1):
            topLabelMatch[label_1][6]+= 1;

        print(resultDataBase[x][0]+','+str(label_1)+','+str(label_2)+','+str(label_3)+','+str(label_4)+','+str(label_5)+','+str(truth)+','+str(match)+',"'\
            +(LabelLines[label_1].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_2].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_3].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_4].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_5].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[truth].split(' ', 1)[1].rstrip('\n'))+'",'\
            +str(prob_1)+','+str(prob_2)+','+str(prob_3)+','+str(prob_4)+','+str(prob_5));

        # Calculate hierarchy graph
        if hierarchyFile != '':
            if(truth == label_1): 
                count = 0;
                f = 0
                while f < 1:
                    if((prob_1 < (f + 0.01)) and prob_1 > f):
                        topKPassFail[count][0]+= 1;

                        topKHierarchyPassFail[count][0]+= 1;
                        topKHierarchyPassFail[count][2]+= 1;
                        topKHierarchyPassFail[count][4]+= 1;
                        topKHierarchyPassFail[count][6]+= 1;
                        topKHierarchyPassFail[count][8]+= 1;
                        topKHierarchyPassFail[count][10]+= 1;

                    count+= 1;
                    f+= 0.01;
            else:
                count = 0;
                f = 0
                while f < 1:
                    if((prob_1 < (f + 0.01)) and prob_1 > f):
                        topKPassFail[count][1]+= 1;

                        truthHierarchy = hierarchyDataBase[truth];
                        resultHierarchy = hierarchyDataBase[label_1];
                        token_result = '';
                        token_truth = '';
                        previousTruth = 0;
                        catCount = 0;
                        while catCount < 6:
                            token_truth = truthHierarchy[catCount];
                            token_result = resultHierarchy[catCount];
                            if((token_truth != '') and (token_truth == token_result)):
                                topKHierarchyPassFail[count][catCount*2]+= 1;
                                previousTruth = 1;
                            elif( (previousTruth == 1) and (token_truth == '' and token_result == '')):
                                topKHierarchyPassFail[count][catCount*2]+= 1;
                            else:
                                topKHierarchyPassFail[count][catCount*2 + 1]+= 1;
                                previousTruth = 0;
                            catCount+= 1;
                    count+= 1;
                    f+= 0.01;

    else: 
        match = -1;
        label_1 = int(resultDataBase[x][2]);
        label_2 = int(resultDataBase[x][3]);
        label_3 = int(resultDataBase[x][4]);
        label_4 = int(resultDataBase[x][5]);
        label_5 = int(resultDataBase[x][6]);
        prob_1 = float(resultDataBase[x][7]);
        prob_2 = float(resultDataBase[x][8]);
        prob_3 = float(resultDataBase[x][9]);
        prob_4 = float(resultDataBase[x][10]);
        prob_5 = float(resultDataBase[x][11]);
        print(resultDataBase[x][0]+','+str(label_1)+','+str(label_2)+','+str(label_3)+','+str(label_4)+','+str(label_5)+','+str(truth)+','+str(match)+',"'\
            +(LabelLines[label_1].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_2].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_3].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_4].split(' ', 1)[1].rstrip('\n'))+'","'\
            +(LabelLines[label_5].split(' ', 1)[1].rstrip('\n'))+'",Unknown,'\
            +str(prob_1)+','+str(prob_2)+','+str(prob_3)+','+str(prob_4)+','+str(prob_5));
                    
        totalNoGroundTruth+= 1;

sys.stdout = orig_stdout
print "resultsComphrehensive.csv generated"

# Generate Comphrehensive Results
print "resultsSummary.txt generation .."
orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/resultsSummary.txt','w')
print("\n\n ***************** INFERENCE SUMMARY ***************** \n\n");
import numpy as np
netSummaryImages =  imageDataSize - totalNoGroundTruth;
passProb = top1TotProb+top2TotProb+top3TotProb+top4TotProb+top5TotProb;
passCount = top1Count+top2Count+top3Count+top4Count+top5Count;
avgPassProb = float(passProb/passCount);

print('Images with Ground Truth -- '+str(netSummaryImages));
print('Images without Ground Truth -- '+str(totalNoGroundTruth));
print('Total image set for Inference -- '+str(imageDataSize));
print("\n");
print('Total Top K match -- '+str(passCount));
accuracyPer = float(passCount);
accuracyPer = (accuracyPer / netSummaryImages) * 100;
print('Inference Accuracy on Top K -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Average Pass Probability for Top K -- '+str(np.around(avgPassProb,decimals=4)));
print("\n");    
print('Total mismatch -- '+str(totalMismatch));
accuracyPer = float(totalMismatch);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Inference mismatch Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Average mismatch Probability for Top 1 -- '+str(np.around(totalFailProb/totalMismatch,decimals=4)));

print("\n*****Top1*****\n");
print('Top1 matches -- '+str(top1Count));  
accuracyPer = float(top1Count);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Top1 match Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');          
print('Avg Top1 pass prob -- '+str(np.around(top1TotProb/top1Count,decimals=4)));
         
print("\n*****Top2*****\n");   
print('Top2 matches -- '+str(top2Count));
accuracyPer = float(top2Count);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Top2 match Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Avg Top2 pass prob -- '+str(np.around(top2TotProb/top2Count,decimals=4)));

print("\n*****Top3*****\n");
print('Top3 matches -- '+str(top3Count));
accuracyPer = float(top3Count);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Top3 match Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Avg Top3 pass prob -- '+str(np.around(top3TotProb/top3Count,decimals=4)));

print("\n*****Top4*****\n");
print('Top4 matches -- '+str(top4Count));
accuracyPer = float(top4Count);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Top4 match Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Avg Top4 pass prob -- '+str(np.around(top4TotProb/top4Count,decimals=4)));

print("\n*****Top5*****\n");
print('Top5 matches -- '+str(top5Count));
accuracyPer = float(top5Count);
accuracyPer = (accuracyPer/netSummaryImages) * 100;
print('Top5 match Percentage -- '+str(np.around(accuracyPer,decimals=2))+' %');
print('Avg Top5 pass prob -- '+str(np.around(top5TotProb/top5Count,decimals=4)));
print("\n\n");
sys.stdout = orig_stdout
print "resultsSummary.txt generated"

# Hierarchy Summary
print "hierarchySummary.csv generation .."
orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/hierarchySummary.csv','w')
print("Probability,Pass,Fail,cat-1 pass,cat-1 fail,cat-2 pass, cat-2 fail,"
      "cat-3 pass,cat-3 fail,cat-4 pass,cat-4 fail,cat-5 pass,cat-5 fail,cat-6 pass,cat-6 fail\n");
i = 99;
f=0.99;
while i >= 0:
    print( (np.around(f,decimals=2)),topKPassFail[i][0],topKPassFail[i][1],topKHierarchyPassFail[i][0],topKHierarchyPassFail[i][1],
        topKHierarchyPassFail[i][2],topKHierarchyPassFail[i][3],topKHierarchyPassFail[i][4],topKHierarchyPassFail[i][5],
        topKHierarchyPassFail[i][6],topKHierarchyPassFail[i][7],topKHierarchyPassFail[i][8],topKHierarchyPassFail[i][9],
        topKHierarchyPassFail[i][10],topKHierarchyPassFail[i][11]);
    f = f - 0.01;
    i = i - 1;
    
sys.stdout = orig_stdout;
print "hierarchySummary.csv generated .."


# Label Summary
print "labelSummary.csv generation .."
orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/labelSummary.csv','w')
print("Label,Images in DataBase, Matched with Top1, Matched with Top2, Matched with Top3, Matched with Top4, Matched with Top5,Top1 Label Match, Label Description");
for i in xrange(1000):
    print ( str(i)+','+str(topLabelMatch[i][0])+','+str(topLabelMatch[i][1])+','+str(topLabelMatch[i][2])
        +','+str(topLabelMatch[i][3])+','+str(topLabelMatch[i][4])+','+str(topLabelMatch[i][5])
        +','+str(topLabelMatch[i][6])+',"'+(LabelLines[i].split(' ', 1)[1].rstrip('\n'))+'"')
sys.stdout = orig_stdout
print "labelSummary.csv generated"

# generate detailed results.csv
print "index.html generation .."
#orig_stdout = sys.stdout
sys.stdout = open(toolKit_dir+'/index.html','w')

print ("<!DOCTYPE HTML PUBLIC \" -//W3C//DTD HTML 4.0 Transitional//EN\">\n");
print ("\n<html>\n");
print ("<head>\n");
print ("\n\t<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\"/>\n");
print ("\t<title>AMD Dataset Analysis Tool</title>\n");
print ("\t<link rel=\"icon\" href=\"icons/vega_icon_150.png\"/>\n");

# page style
print ("\n\t<style type=\"text/css\">\n");
print ("\t\n");
print ("\tbody,div,table,thead,tbody,tfoot,tr,th,td,p { font-family:\"Liberation Sans\"; font-size:x-small }\n");
print ("\ta.comment-indicator:hover + comment { background:#ffd; position:absolute; display:block; border:1px solid black; padding:0.5em;  }\n");
print ("\ta.comment-indicator { background:red; display:inline-block; border:1px solid black; width:0.5em; height:0.5em;  }\n");
print ("\tcomment { display:none;  } tr:nth-of-type(odd) { background-color:#f2f2f2;}\n");
print ("\t\n");
print ("\t#myImg { border-radius: 5px; cursor: pointer; transition: 0.3s; }\n");
print ("\t#myImg:hover { opacity: 0.7; }\n");
print ("\t.modal{ display: none; position: fixed; z-index: 8; padding-top: 100px; left: 0; top: 0;width: 100%;\n");
print ("\t       height: 100%; overflow: auto; background-color: rgb(0,0,0); background-color: rgba(0,0,0,0.9); }\n");
print ("\t.modal-content { margin: auto; display: block; width: 80%; max-width: 500px; }\n");
print ("\t#caption { margin: auto; display: block; width: 80%; max-width: 700px; text-align: center; color: white;font-size: 18px; padding: 10px 0; height: 150px;}\n");
print ("\t.modal-content, #caption {  -webkit-animation-name: zoom;  -webkit-animation-duration: 0.6s;\n");
print ("\t                           animation-name: zoom; animation-duration: 0.6s; }\n");
print ("\t@-webkit-keyframes zoom {  from { -webkit-transform:scale(0) }  to { -webkit-transform:scale(1) }}\n");
print ("\t@keyframes zoom {    from {transform:scale(0)}     to {transform:scale(1) }}\n");
print ("\t.close { position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; transition: 0.3s; }\n");
print ("\t.close:hover,.close:focus { color: #bbb; text-decoration: none; cursor: pointer; }\n");
print ("\t@media only screen and (max-width: 400px){ .modal-content {     width: 100%; } }\n");
print ("\t\n");
print ("\tbody { font-family: \"Lato\", sans-serif;}\n");
print ("\t.sidenav { height: 100%; width: 0; position: fixed; z-index: 7; top: 0; left: 0; background-color: #111;\n");
print ("\t\t overflow-x: hidden;    transition: 0.5s; padding-top: 60px;}\n");
print ("\t.sidenav a { padding: 8px 8px 8px 32px; text-decoration: none; font-size: 25px; color: #818181; display: block; transition: 0.3s;}\n");
print ("\t.sidenav a:hover { color: #f1f1f1;}\n");
print ("\t.sidenav .closebtn {  position: absolute; top: 0; right: 25px; font-size: 36px; margin-left: 50px;}\n");
print ("\t#main {  transition: margin-left .5s;  padding: 16px; }\n");
print ("\t@media screen and (max-height: 450px) { .sidenav {padding-top: 15px;} .sidenav a {font-size: 18px;} }\n");
print ("\t\n");
print ("\tbody {margin:0;}\n");
print ("\t.navbar {  overflow: hidden;  background-color: #333;  position: fixed; z-index: 6;  top: 0;  width: 100%;}\n");
print ("\t.navbar a {  float: left;  display: block;  color: #f2f2f2;  text-align: center;  padding: 14px 16px;  text-decoration: none;  font-size: 17px; }\n");
print ("\t.navbar a:hover {  background: #ddd;  color: black;}\n");
print ("\t.main {  padding: 16px;  margin-top: 30px; }\n");
print ("\t\n");
print ("\tselect {-webkit-appearance: none; -moz-appearance: none; text-indent: 0px; text-overflow: ''; color:maroon; }\n");
print ("\t\n");
print ("\t.tooltip { position: relative; display: inline-block;}\n");
print ("\t.tooltip .tooltiptext { visibility: hidden; width: 150px; background-color: black; color: gold;\n");
print ("\t\ttext-align: center;  border-radius: 6px;  padding: 5px; position: absolute; z-index: 3;}\n");
print ("\t.tooltip:hover .tooltiptext { visibility: visible;}\n");
print ("\t\n");
print ("\t\t.footer { position: fixed; left: 0;    bottom: 0;  width: 100%;    background-color: #333;  color: white;  text-align: center;}\n");
print ("\t\n");
print ("\t</style>\n");
print ("\n</head>\n");
print ("\n\n<body>\n");
print ("\t\n");
print ("\t<div id=\"myModal\" class=\"modal\"> <span class=\"close\">&times;</span>  <img class=\"modal-content\" id=\"img01\">  <div id=\"caption\"></div> </div>\n");
print ("\t\n");

# table content order
print ("\t<div id=\"mySidenav\" class=\"sidenav\">\n");
print ("\t<a href=\"javascript:void(0)\" class=\"closebtn\" onclick=\"closeNav()\">&times;</a>\n");
print ("\t<A HREF=\"#table0\"><font size=\"5\">Summary</font></A><br>\n");
print ("\t<A HREF=\"#table1\"><font size=\"5\">Graphs</font></A><br>\n");
print ("\t<A HREF=\"#table2\"><font size=\"5\">Hierarchy</font></A><br>\n");
print ("\t<A HREF=\"#table3\"><font size=\"5\">Labels</font></A><br>\n");
print ("\t<A HREF=\"#table4\"><font size=\"5\">Image Results</font></A><br>\n");
print ("\t<A HREF=\"#table5\"><font size=\"5\">Compare</font></A><br>\n");
print ("\t<A HREF=\"#table6\"><font size=\"5\">Model Score</font></A><br>\n");
print ("\t<A HREF=\"#table7\"><font size=\"5\">Help</font></A><br>\n");
print ("\t</div>\n");
print ("\t\n");

# scripts
print ("\t<script>\n");
print ("\t\tfunction openNav() {\n");
print ("\t\t\tdocument.getElementById(\"mySidenav\").style.width = \"250px\";\n");
print ("\t\t\tdocument.getElementById(\"main\").style.marginLeft = \"250px\";}\n");
print ("\t\tfunction closeNav() {\n");
print ("\t\t\tdocument.getElementById(\"mySidenav\").style.width = \"0\";\n");
print ("\t\t\tdocument.getElementById(\"main\").style.marginLeft= \"0\";}\n");
print ("\t\tfunction myreload() { location.reload();}\n");
print ("\t\n");
print ("\t\tfunction sortTable(coloum,descending) {\n");
print ("\t\tvar table, rows, switching, i, x, y, shouldSwitch;\n");
print ("\t\ttable = document.getElementById(id=\"resultsTable\"); switching = true;\n");
print ("\t\twhile (switching) {  switching = false; rows = table.getElementsByTagName(\"TR\");\n");
print ("\t\t\tfor (i = 1; i < (rows.length - 1); i+= 1) { shouldSwitch = false;\n");
print ("\t\t\t\tx = rows[i].getElementsByTagName(\"TD\")[coloum];\n");
print ("\t\t\t\ty = rows[i + 1].getElementsByTagName(\"TD\")[coloum];\n");
print ("\t\t\t\tif(descending){if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {\n");
print ("\t\t\t\t\tshouldSwitch= true;    break;}}\n");
print ("\t\t\t\telse{if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {\n");
print ("\t\t\t\t\tshouldSwitch= true;    break;}}}\n");
print ("\t\t\t\tif (shouldSwitch) {  rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);\n");
print ("\t\t\t\t\tswitching = true;}}}\n");
print ("\t\n");
print ("\t\n");
print ("\t\tfunction sortLabelsTable(coloum,descending) {\n");
print ("\t\tvar table, rows, switching, i, x, y, shouldSwitch;\n");
print ("\t\ttable = document.getElementById(id=\"labelsTable\"); switching = true;\n");
print ("\t\twhile (switching) {  switching = false; rows = table.getElementsByTagName(\"TR\");\n");
print ("\t\t\tfor (i = 1; i < (rows.length - 1); i+= 1) { shouldSwitch = false;\n");
print ("\t\t\t\tx = rows[i].getElementsByTagName(\"TD\")[coloum];\n");
print ("\t\t\t\ty = rows[i + 1].getElementsByTagName(\"TD\")[coloum];\n");
print ("\t\t\t\tif(descending){if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {\n");
print ("\t\t\t\t\tshouldSwitch= true;    break;}}\n");
print ("\t\t\t\telse{if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {\n");
print ("\t\t\t\t\tshouldSwitch= true;    break;}}}\n");
print ("\t\t\t\tif (shouldSwitch) {  rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);\n");
print ("\t\t\t\t\tswitching = true;}}}\n");
print ("\t\n");
print ("\t</script>\n");
print ("\t<script src=\"https://www.kryogenix.org/code/browser/sorttable/sorttable.js\"></script>\n");
print ("\t\n");
print ("\t<script>\n");
print ("\t\tfunction filterResultTable(rowNum, DataVar) {\n");
print ("\t\tvar input, filter, table, tr, td, i;\n");
print ("\t\tinput = document.getElementById(DataVar);\n");
print ("\t\tfilter = input.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"resultsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttd = tr[i].getElementsByTagName(\"td\")[rowNum];\n");
print ("\t\tif (td) { if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {tr[i].style.display = \"\"; }\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\t</script>\n");
print ("\t\n");
print ("\t\n");
print ("\t<script>\n");
print ("\t\tfunction filterLabelTable(rowNum, DataVar) {\n");
print ("\t\tvar input, filter, table, tr, td, i;\n");
print ("\t\tinput = document.getElementById(DataVar);\n");
print ("\t\tfilter = input.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"labelsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttd = tr[i].getElementsByTagName(\"td\")[rowNum];\n");
print ("\t\tif (td) { if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {tr[i].style.display = \"\"; }\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\t</script>\n");
print ("\t\n");
print ("\n");
print ("\t<script>\n");
print ("\t\tfunction clearLabelFilter() {\n");
print ("\t\tdocument.getElementById('Label ID').value = ''\n");
print ("\t\tdocument.getElementById('Label Description').value = ''\n");
print ("\t\tdocument.getElementById('Images in DataBase').value = ''\n");
print ("\t\tdocument.getElementById('Matched Top1 %').value = ''\n");
print ("\t\tdocument.getElementById('Matched Top5 %').value = ''\n");
print ("\t\tdocument.getElementById('Matched 1st').value = ''\n");
print ("\t\tdocument.getElementById('Matched 2nd').value = ''\n");
print ("\t\tdocument.getElementById('Matched 3th').value = ''\n");
print ("\t\tdocument.getElementById('Matched 4th').value = ''\n");
print ("\t\tdocument.getElementById('Matched 5th').value = ''\n");
print ("\t\tdocument.getElementById('Misclassified Top1 Label').value = ''\n");
print ("\t\tfilterLabelTable(0,'Label ID') }\n");
print ("\t</script>\n");
print ("\n");
print ("\n");
print ("\t<script>\n");
print ("\t\tfunction clearResultFilter() {\n");
print ("\t\tdocument.getElementById('GroundTruthText').value = ''\n");
print ("\t\tdocument.getElementById('GroundTruthID').value = ''\n");
print ("\t\tdocument.getElementById('Matched').value = ''\n");
print ("\t\tdocument.getElementById('Top1').value = ''\n");
print ("\t\tdocument.getElementById('Top1Prob').value = ''\n");
print ("\t\tdocument.getElementById('Text1').value = ''\n");
print ("\t\tdocument.getElementById('Top2').value = ''\n");
print ("\t\tdocument.getElementById('Top2Prob').value = ''\n");
print ("\t\tdocument.getElementById('Top3').value = ''\n");
print ("\t\tdocument.getElementById('Top3Prob').value = ''\n");
print ("\t\tdocument.getElementById('Top4').value = ''\n");
print ("\t\tdocument.getElementById('Top4Prob').value = ''\n");
print ("\t\tdocument.getElementById('Top5').value = ''\n");
print ("\t\tdocument.getElementById('Top5Prob').value = ''\n");
print ("\t\tfilterResultTable(2,'GroundTruthText') }\n");
print ("\t</script>\n");
print ("\n");
print ("\t<script>\n");
print ("\t\tfunction findGroundTruthLabel(label,labelID) {\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('GroundTruthText').value = label;\n");
print ("\t\tdocument.getElementById('GroundTruthID').value = labelID;\n");
print ("\t\tandResultFilter();\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction findMisclassifiedGroundTruthLabel(label) {\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('Text1').value = label;\n");
print ("\t\tfilterResultTable(10,'Text1');\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction highlightRow(obj){\n");
print ("\t\tvar tr=obj; while (tr.tagName.toUpperCase()!='TR'&&tr.parentNode){  tr=tr.parentNode;}\n");
print ("\t\tif (!tr.col){tr.col=tr.bgColor; } if (obj.checked){  tr.bgColor='#d5f5e3';}\n");
print ("\t\telse {  tr.bgColor=tr.col;}}\n");
print ("\n");
print ("\t\tfunction goToImageResults() { window.location.href = '#table4';}\n");
print ("\n");
print ("\t\tfunction findImagesWithNoGroundTruthLabel() {\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('GroundTruthID').value = '-1';\n");
print ("\t\tfilterResultTable(3,'GroundTruthID');\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction findImageMisMatch() {\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('Matched').value = '0';\n");
print ("\t\tfilterResultTable(9,'Matched');\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction findTopKMatch() {\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('Matched').value = '0';\n");
print ("\t\tnotResultFilter();\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction filterResultTableInverse(rowNum, DataVar) {\n");
print ("\t\tvar input, filter, table, tr, td, i;\n");
print ("\t\tinput = document.getElementById(DataVar);\n");
print ("\t\tfilter = input.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"resultsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttd = tr[i].getElementsByTagName(\"td\")[rowNum];\n");
print ("\t\tif (td) { if (td.innerHTML.toUpperCase().indexOf(filter) <= -1) {tr[i].style.display = \"\"; }\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\t\tfunction findImagesWithGroundTruthLabel(){\n");
print ("\t\tclearResultFilter();\n");
print ("\t\tdocument.getElementById('Matched').value = '-1';\n");
print ("\t\tfilterResultTableInverse(9, 'Matched')\n");
print ("\t\twindow.location.href = '#table4';\n");
print ("\t\t}\n");
print ("\n");
print ("\t\tfunction notResultFilter( ) {\n");
print ("\t\tvar input, filter, table, tr, td, i, rowNum, count;\n");
print ("\t\tcount=0;\n");
print ("\t\tif(document.getElementById('GroundTruthText').value != ''){\n");
print ("\t\tinput = document.getElementById('GroundTruthText');  rowNum = 2;count+= 1;}\n");
print ("\t\tif(document.getElementById('GroundTruthID').value != ''){\n");
print ("\t\tinput = document.getElementById('GroundTruthID'); rowNum = 3;count+= 1;}\n");
print ("\t\tif(document.getElementById('Matched').value != ''){\n");
print ("\t\tinput = document.getElementById('Matched');  rowNum = 9;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top1').value != ''){\n");
print ("\t\tinput = document.getElementById('Top1'); rowNum = 4;count+= 1; }\n");
print ("\t\tif(document.getElementById('Top1Prob').value != ''){\n");
print ("\t\tinput = document.getElementById('Top1Prob');rowNum = 15;count+= 1;}\n");
print ("\t\tif(document.getElementById('Text1').value != ''){\n");
print ("\t\tinput = document.getElementById('Text1');rowNum = 10;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top2').value != ''){\n");
print ("\t\tinput = document.getElementById('Top2');rowNum = 5;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top2Prob').value != ''){\n");
print ("\t\tinput = document.getElementById('Top2Prob');rowNum = 16;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top3').value != ''){\n");
print ("\t\tinput = document.getElementById('Top3');rowNum = 6;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top3Prob').value != ''){\n");
print ("\t\tinput = document.getElementById('Top3Prob');rowNum = 17;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top4').value != ''){\n");
print ("\t\tinput = document.getElementById('Top4');rowNum = 7;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top4Prob').value != ''){\n");
print ("\t\tinput = document.getElementById('Top4Prob');rowNum = 18;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top5').value != ''){\n");
print ("\t\tinput = document.getElementById('Top5');rowNum = 8;count+= 1;}\n");
print ("\t\tif(document.getElementById('Top5Prob').value != ''){\n");
print ("\t\tinput = document.getElementById('Top5Prob');rowNum = 19;count+= 1;}\n");
print ("\t\tif(count == 0){alert(\"Not Filter ERROR: No filter variable entered\");}\n");
print ("\t\telse if(count > 1){\n");
print ("\t\talert(\"Not Filter ERROR: Only one variable filtering supported. Use Clear Filter and enter one filter variable\");}\n");
print ("\t\tfilter = input.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"resultsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttd = tr[i].getElementsByTagName(\"td\")[rowNum];\n");
print ("\t\tif (td) { if (td.innerHTML.toUpperCase().indexOf(filter) <= -1) {tr[i].style.display = \"\"; }\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\n");
print ("\t\tfunction andResultFilter( ) {\n");
print ("\t\tvar inputOne, inputTwo, filterOne, filterTwo, table, tr, tdOne, tdTwo, i, rowNumOne, rowNumTwo,count;\n");
print ("\t\tcount=0;\n");
print ("\t\trowNumOne=0;\n");
print ("\t\tif(document.getElementById('GroundTruthText').value != ''){\n");
print ("\t\tinputOne = document.getElementById('GroundTruthText');   rowNumOne = 2;count+= 1;}\n");
print ("\t\telse if(document.getElementById('GroundTruthID').value != ''){\n");
print ("\t\tinputOne = document.getElementById('GroundTruthID'); rowNumOne = 3;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Matched').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Matched');   rowNumOne = 9;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top1').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top1'); rowNumOne = 4;count+= 1; }\n");
print ("\t\telse if(document.getElementById('Top1Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top1Prob');rowNumOne = 15;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Text1').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Text1');rowNumOne = 10;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top2');rowNumOne = 5;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top2Prob');rowNumOne = 16;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top3');rowNumOne = 6;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top3Prob');rowNumOne = 17;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top4');rowNumOne = 7;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top4Prob');rowNumOne = 18;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top5');rowNumOne = 8;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top5Prob');rowNumOne = 19;count+= 1;}\n");
print ("\t\tif(document.getElementById('GroundTruthText').value != '' && rowNumOne  != 2){\n");
print ("\t\tinputTwo = document.getElementById('GroundTruthText');   rowNumTwo = 2;count+= 1;}\n");
print ("\t\telse if(document.getElementById('GroundTruthID').value != '' && rowNumOne  != 3){\n");
print ("\t\tinputTwo = document.getElementById('GroundTruthID'); rowNumTwo = 3;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Matched').value != '' && rowNumOne  != 9){\n");
print ("\t\tinputTwo = document.getElementById('Matched');   rowNumTwo = 9;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top1').value != '' && rowNumOne  != 4){\n");
print ("\t\tinputTwo = document.getElementById('Top1'); rowNumTwo = 4;count+= 1; }\n");
print ("\t\telse if(document.getElementById('Top1Prob').value != '' && rowNumOne  != 215){\n");
print ("\t\tinputTwo = document.getElementById('Top1Prob');rowNumTwo = 15;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Text1').value != '' && rowNumOne  != 10){\n");
print ("\t\tinputTwo = document.getElementById('Text1');rowNumTwo = 10;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2').value != '' && rowNumOne  != 5){\n");
print ("\t\tinputTwo = document.getElementById('Top2');rowNumTwo = 5;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2Prob').value != '' && rowNumOne  != 16){\n");
print ("\t\tinputTwo = document.getElementById('Top2Prob');rowNumTwo = 16;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3').value != '' && rowNumOne  != 6){\n");
print ("\t\tinputTwo = document.getElementById('Top3');rowNumTwo = 6;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3Prob').value != '' && rowNumOne  != 17){\n");
print ("\t\tinputTwo = document.getElementById('Top3Prob');rowNumTwo = 17;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4').value != '' && rowNumOne  != 7){\n");
print ("\t\tinputTwo = document.getElementById('Top4');rowNumTwo = 7;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4Prob').value != '' && rowNumOne  != 18){\n");
print ("\t\tinputTwo = document.getElementById('Top4Prob');rowNumTwo = 18;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5').value != '' && rowNumOne  != 8){\n");
print ("\t\tinputTwo = document.getElementById('Top5');rowNumTwo = 8;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5Prob').value != '' && rowNumOne  != 19){\n");
print ("\t\tinputTwo = document.getElementById('Top5Prob');rowNumTwo = 19;count+= 1;}\n");
print ("\t\tif(count == 0){alert(\"AND Filter ERROR: No filter variable entered\");}\n");
print ("\t\telse if(count == 1){alert(\"AND Filter ERROR: Enter two variables\");}\n");
print ("\t\telse if(count > 2){\n");
print ("\t\talert(\"AND Filter ERROR: Only two variable filtering supported. Use Clear Filter and enter two filter variable\");}\n");
print ("\t\tfilterOne = inputOne.value.toUpperCase();\n");
print ("\t\tfilterTwo = inputTwo.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"resultsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttdOne = tr[i].getElementsByTagName(\"td\")[rowNumOne];\n");
print ("\t\ttdTwo = tr[i].getElementsByTagName(\"td\")[rowNumTwo];\n");
print ("\t\tif (tdOne && tdTwo) { \n");
print ("\t\tif (tdOne.innerHTML.toUpperCase().indexOf(filterOne) > -1 && tdTwo.innerHTML.toUpperCase().indexOf(filterTwo) > -1) \n");
print ("\t\t{tr[i].style.display = \"\";}\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\n");
print ("\t\tfunction orResultFilter( ) {\n");
print ("\t\tvar inputOne, inputTwo, filterOne, filterTwo, table, tr, tdOne, tdTwo, i, rowNumOne, rowNumTwo, count;\n");
print ("\t\tcount=0;\n");
print ("\t\trowNumOne=0;\n");
print ("\t\tif(document.getElementById('GroundTruthText').value != ''){\n");
print ("\t\tinputOne = document.getElementById('GroundTruthText');   rowNumOne = 2;count+= 1;}\n");
print ("\t\telse if(document.getElementById('GroundTruthID').value != ''){\n");
print ("\t\tinputOne = document.getElementById('GroundTruthID'); rowNumOne = 3;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Matched').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Matched');   rowNumOne = 9;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top1').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top1'); rowNumOne = 4;count+= 1; }\n");
print ("\t\telse if(document.getElementById('Top1Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top1Prob');rowNumOne = 15;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Text1').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Text1');rowNumOne = 10;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top2');rowNumOne = 5;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top2Prob');rowNumOne = 16;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top3');rowNumOne = 6;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top3Prob');rowNumOne = 17;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top4');rowNumOne = 7;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top4Prob');rowNumOne = 18;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top5');rowNumOne = 8;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5Prob').value != ''){\n");
print ("\t\tinputOne = document.getElementById('Top5Prob');rowNumOne = 19;count+= 1;}\n");
print ("\t\tif(document.getElementById('GroundTruthText').value != '' && rowNumOne  != 2){\n");
print ("\t\tinputTwo = document.getElementById('GroundTruthText');   rowNumTwo = 2;count+= 1;}\n");
print ("\t\telse if(document.getElementById('GroundTruthID').value != '' && rowNumOne  != 3){\n");
print ("\t\tinputTwo = document.getElementById('GroundTruthID'); rowNumTwo = 3;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Matched').value != '' && rowNumOne  != 9){\n");
print ("\t\tinputTwo = document.getElementById('Matched');   rowNumTwo = 9;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top1').value != '' && rowNumOne  != 4){\n");
print ("\t\tinputTwo = document.getElementById('Top1'); rowNumTwo = 4;count+= 1; }\n");
print ("\t\telse if(document.getElementById('Top1Prob').value != '' && rowNumOne  != 215){\n");
print ("\t\tinputTwo = document.getElementById('Top1Prob');rowNumTwo = 15;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Text1').value != '' && rowNumOne  != 10){\n");
print ("\t\tinputTwo = document.getElementById('Text1');rowNumTwo = 10;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2').value != '' && rowNumOne  != 5){\n");
print ("\t\tinputTwo = document.getElementById('Top2');rowNumTwo = 5;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top2Prob').value != '' && rowNumOne  != 16){\n");
print ("\t\tinputTwo = document.getElementById('Top2Prob');rowNumTwo = 16;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3').value != '' && rowNumOne  != 6){\n");
print ("\t\tinputTwo = document.getElementById('Top3');rowNumTwo = 6;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top3Prob').value != '' && rowNumOne  != 17){\n");
print ("\t\tinputTwo = document.getElementById('Top3Prob');rowNumTwo = 17;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4').value != '' && rowNumOne  != 7){\n");
print ("\t\tinputTwo = document.getElementById('Top4');rowNumTwo = 7;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top4Prob').value != '' && rowNumOne  != 18){\n");
print ("\t\tinputTwo = document.getElementById('Top4Prob');rowNumTwo = 18;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5').value != '' && rowNumOne  != 8){\n");
print ("\t\tinputTwo = document.getElementById('Top5');rowNumTwo = 8;count+= 1;}\n");
print ("\t\telse if(document.getElementById('Top5Prob').value != '' && rowNumOne  != 19){\n");
print ("\t\tinputTwo = document.getElementById('Top5Prob');rowNumTwo = 19;count+= 1;}\n");
print ("\t\tif(count == 0){alert(\"OR Filter ERROR: No filter variable entered\");}\n");
print ("\t\telse if(count == 1){alert(\"OR Filter ERROR: Enter two variables\");}\n");
print ("\t\telse if(count > 2){\n");
print ("\t\talert(\"OR Filter ERROR: Only two variable filtering supported. Use Clear Filter and enter two filter variable\");}\n");
print ("\t\tfilterOne = inputOne.value.toUpperCase();\n");
print ("\t\tfilterTwo = inputTwo.value.toUpperCase();\n");
print ("\t\ttable = document.getElementById(\"resultsTable\");\n");
print ("\t\ttr = table.getElementsByTagName(\"tr\");\n");
print ("\t\tfor (i = 1; i < tr.length; i+= 1) {\n");
print ("\t\ttdOne = tr[i].getElementsByTagName(\"td\")[rowNumOne];\n");
print ("\t\ttdTwo = tr[i].getElementsByTagName(\"td\")[rowNumTwo];\n");
print ("\t\tif (tdOne && tdTwo) { \n");
print ("\t\tif (tdOne.innerHTML.toUpperCase().indexOf(filterOne) > -1 || tdTwo.innerHTML.toUpperCase().indexOf(filterTwo) > -1) \n");
print ("\t\t{tr[i].style.display = \"\";}\n");
print ("\t\telse { tr[i].style.display = \"none\";}}}}\n");
print ("\n");
print ("\t</script>\n");
print ("\n");

#TBD: Graph CODE

#Top view header
print ("\t<div class=\"navbar\">\n");
print ("\t<a href=\"#\">\n");
print ("\t<div id=\"main\">\n");
print ("\t<span style=\"font-size:30px;cursor:pointer\" onclick=\"openNav()\">&#9776; Views</span>\n");
print ("\t</div></a>\n");
print ("\t<a href=\"https://www.amd.com/en\" target=\"_blank\">\n");
print ("\t<img \" src=\"icons/small_amd_logo.png\" alt=\"AMD\" /></a>\n");
print ("\t<a href=\"https://gpuopen.com/\" target=\"_blank\">\n");
print ("\t<img \" src=\"icons/small_radeon_logo.png\" alt=\"GPUopen\" /></a>\n");
print ("\t<a href=\"https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules#amd-openvx-modules-amdovx-modules\" target=\"_blank\">\n");
print ("\t<img \" src=\"icons/small_github_logo.png\" alt=\"AMD GitHub\" /></a>\n");
print ("\t<img \" src=\"icons/ADAT_500x100.png\" alt=\"AMD Inference ToolKit\" hspace=\"100\" height=\"90\"/> \n");
print ("\t</div>\n");
print ("\t\n");

#TBD: Sections






# HELP
print ("\t<!-- HELP -->\n");
print ("<A NAME=\"table7\"><h1 align=\"center\"><font color=\"DodgerBlue\" size=\"6\"><br><br><br><em>HELP</em></font></h1></A>\n");
print ("\t\n");
print ("\t<table align=\"center\" style=\"width: 50%\">\n");
print ("\t<tr><td>\n");
print ("\t<h1 align=\"center\">AMD Neural Net ToolKit</h1>\n");
print ("\t</td></tr><tr><td>\n");
print ("\t<p>AMD Neural Net ToolKit is a comprehensive set of help tools for neural net creation, development, training and\n");
print ("\tdeployment. The ToolKit provides you with help tools to design, develop, quantize, prune, retrain, and infer your neural\n");
print ("\tnetwork work in any framework. The ToolKit is designed help you deploy your work to any AMD or 3rd party hardware, from \n");
print ("\tembedded to servers.</p>\n");
print ("\t<p>AMD Neural Net ToolKit provides you with tools for accomplishing your tasks throughout the whole neural net life-cycle,\n");
print ("\tfrom creating a model to deploying them for your target platforms.</p>\n");
print ("\t<h2 >List of Features Available in this release</h2>\n");
print ("\t<ul>\n");
print ("\t<li>Overall Summary</li>\n");
print ("\t<li>Graphs</li>\n");
print ("\t<li>Hierarchy</li>\n");
print ("\t<li>Labels</li>\n");
print ("\t<li>Image Results</li>\n");
print ("\t<li>Compare</li>\n");
print ("\t<li>Help</li>\n");
print ("\t</ul>\n");
print ("\t<h3 >Overall Summary</h3>\n");
print ("\t<p>This section summarizes the results for the current session, with information on the dataset and the model.\n");
print ("\tThe section classifies the dataset into images with or without ground truth and only considers the images with ground truth \n");
print ("\tfor analysis to avoid skewing the results.</p>\n");
print ("\t<p>The summary calculates all the metrics to evaluate the current run session, helps evaluate the quality of the data set,\n");
print ("\taccuracy of the current version of the model and links all the high level result to individual images to help the user to \n");
print ("\tquickly analyze and detect if there are any problems.</p>\n");
print ("\t<p>The summary also timestamps the results to avoid confusion with different iterations.</p>\n");
print ("\t<h3>Graphs</h3>\n");
print ("\t<p>The graph section allows the user to visualize the dataset and model accurately. The graphs can help detect any\n");
print ("\tanomalies with the data or the model from a higher level. The graphs can be saved or shared with others.</p>\n");
print ("\t<h3 >Hierarchy</h3>\n");
print ("\t<p>This section has AMD proprietary hierarchical result analysis. Please contact us to get more information.</p>\n");
print ("\t<h3 >Labels</h3>\n");
print ("\t<p>Label section is the summary of all the classes the model has been trained to detect. The Label Summary presents the\n");
print ("\thighlights of all the classes of images available in the database. The summary reports if the classes are found or not \n");
print ("\tfound.</p>\n");
print ("\t<p>Click on any of the label description and zoom into all the images from that class in the database.</p>\n");
print ("\t<h3 >Image Results</h3>\n");
print ("\t<p>The Image results has all the low level information about each of the individual images in the database. It reports on \n");
print ("\tthe results obtained for the image in the session and allows quick view of the image.</p>\n");
print ("\t<h3 >Compare</h3>\n");
print ("\t<p>This section compares the results of a database or the model between different sessions. If the database was tested with\n");
print ("\tdifferent models, this section reports and compares results among them.</p>\n");
print ("\t</td></tr>\n");
print ("\t</table>\n");
print ("\t<br><br><br>\n");
#TBD: symbol
print ("\t\t<div class=\"footer\"> <p>2018 Advanced Micro Devices, Inc</p></div>\n");
print ("\t\n");
print ("\n</body>\n");
print ("\n</html>\n");

sys.stdout = orig_stdout
print "index.html generated"
exit (0)