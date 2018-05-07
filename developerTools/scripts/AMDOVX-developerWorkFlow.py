import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:u:p:d:')
 
sudoPassword = ''
githubUserName = ''
githubPassword = ''
buildDir = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt == '-u':
        githubUserName = arg
    elif opt == '-p':
        githubPassword = arg
    elif opt == '-d':
    	buildDir = arg

if sudoPassword == '' or githubUserName == '' or githubPassword == '':
    print('Invalid command line arguments. Usage python AMDOVX-developerWorkFlow.py -s [sudo Password - required] ' \
          '-u [GitHub UserName  - required] -p [GitHub Password  - required] -d [valid developer directory - optional ]')
    exit()

if buildDir == '':
	buildDir_AMDOVX = '~/AMDOVX'
else:
	buildDir_AMDOVX = buildDir+'AMDOVX'

# AMDOVX Work Flow
buildMain_dir = os.path.expanduser(buildDir_AMDOVX)
buildGIT_dir = os.path.expanduser(buildDir_AMDOVX+'/amdovx-testscripts')

if(os.path.exists(buildGIT_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd '+buildGIT_dir+'; git pull; git submodule init; git submodule update --recursive )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-modules; git submodule init; git submodule update --recursive )');
else:
	os.system('rm -rf '+buildMain_dir);
	os.system('(cd ; mkdir '+buildMain_dir+')');
	os.system('(cd '+buildMain_dir+'; git clone --recursive http://'+githubUserName+':'+githubPassword+'@github.com/'+githubUserName+'/amdovx-testscripts )');
	os.system('(cd '+buildGIT_dir+'; git branch -m develop-personal )');
	os.system('(cd '+buildGIT_dir+'; git remote add amd http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-testscripts )');
	os.system('(cd '+buildGIT_dir+'; git fetch --all )');
	os.system('(cd '+buildGIT_dir+'; git checkout -b master --track amd/master )');
	os.system('(cd '+buildGIT_dir+'; git checkout -b develop --track amd/develop; git pull )');
	os.system('(cd '+buildGIT_dir+'/deps; rm -rf amdovx-testdata )');
	os.system('(cd '+buildGIT_dir+'/deps; git clone --recursive http://'+githubUserName+':'+githubPassword+'@github.com/'+githubUserName+'/amdovx-testdata.git )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-testdata; git branch -m develop-personal )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-testdata; git remote add amd http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-testdata.git )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-testdata; git fetch --all )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-testdata; git checkout -b master --track amd/master )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-testdata; git checkout -b develop --track amd/develop; git pull )');
	os.system('(cd '+buildGIT_dir+'; git submodule init; git submodule update --recursive  )');
	os.system('(cd '+buildGIT_dir+'/deps/amdovx-modules; git submodule init; git submodule update --recursive )');

# AMDOVX Build
build_dir = os.path.expanduser(buildDir_AMDOVX+'/build')
if(os.path.exists(build_dir)):
	os.system('(cd '+buildDir_AMDOVX+'; rm -rf build)');
	os.system('(cd '+buildDir_AMDOVX+'; mkdir build)');
else:
	os.system('(cd '+buildDir_AMDOVX+'; mkdir build)');

os.system('(cd '+buildDir_AMDOVX+'/build; cmake -DCMAKE_BUILD_TYPE=Release ../amdovx-testscripts )');
os.system('(cd '+buildDir_AMDOVX+'/build; make -j8 )');
from subprocess import call
cmd='(cd '+buildDir_AMDOVX+'/build; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd '+buildDir_AMDOVX+'/build; ls -l bin )');
