import os
import getopt
import sys
 
opts, args = getopt.getopt(sys.argv[1:], 's:d:b:')
 
sudoPassword = ''
depsDir = ''
buildDir = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt == '-d':
    	depsDir = arg
    elif opt == '-b':
    	buildDir = arg

if sudoPassword == '':
    print('Invalid command line arguments. python RadeonInferenceInstaller.py -s [sudo password - required]'\
    	' -d [dependencies directory - optional] -b [build directory - optional]')
    exit()

# set defaults
if depsDir == '':
	depsDir = '~/'
if buildDir == '':
	buildDir = '~/'

# run step 1, 2, & 3 scripts to generate the dataBase
os.system('python inference-setup.py -s '+sudoPassword+' -d '+depsDir);
os.system('python inference-build.py -s '+sudoPassword+' -d '+buildDir);