import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:d:')
 
sudoPassword = ''
buildDir = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt == '-d':
    	buildDir = arg

if sudoPassword == '':
    print('Invalid command line arguments. usage python inference-setup.py -s [sudo password - required] -d [build directory - optional] ')
    exit()

if buildDir == '':
	buildDir_AMDOVX = '~/AMDOVX'
else:
	buildDir_AMDOVX = buildDir+'AMDOVX'

# AMDOVX Work Flow
buildMain_dir = os.path.expanduser(buildDir_AMDOVX)
buildGIT_dir = os.path.expanduser(buildDir_AMDOVX+'/amdovx-modules')
buildMake_dir = os.path.expanduser(buildDir_AMDOVX+'/build')
if(os.path.exists(buildGIT_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd '+buildGIT_dir+'; git pull; git submodule init; git submodule update --recursive )');
else:
	os.system('rm -rf '+buildMain_dir);
	os.system('(cd ; mkdir '+buildMain_dir+')');
	os.system('(cd '+buildMain_dir+'; git clone --recursive -b develop http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules )');
	os.system('(cd '+buildGIT_dir+'; git submodule init; git submodule update --recursive  )');

# AMDOVX Build
if(os.path.exists(buildMake_dir)):
	os.system('(cd '+buildMain_dir+'; rm -rf build)');
	os.system('(cd '+buildMain_dir+'; mkdir build)');
else:
	os.system('(cd '+buildMain_dir+'; mkdir build)');

os.system('(cd '+buildMake_dir+'; cmake -DCMAKE_BUILD_TYPE=Release ../amdovx-modules )');
os.system('(cd '+buildMake_dir+'; make -j8 )');
from subprocess import call
cmd='(cd '+buildMake_dir+'; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd '+buildMake_dir+'; ls -l bin )');
