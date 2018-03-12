import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:u:p:')
 
sudoPassword = ''
githubUserName = ''
githubPassword = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt == '-u':
        githubUserName = arg
    elif opt == '-p':
        githubPassword = arg

if sudoPassword == '' or githubUserName == '' or githubPassword == '':
    print('Invalid command line arguments. -s [Sudo Password] ' \
          '-u [GitHub UserName] -p [GitHub Password] are required')
    exit()

# AMDOVX Work Flow
deps_dir = os.path.expanduser('~/AMDOVX/amdovx-testscripts')
if(os.path.exists(deps_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git pull; git submodule init; git submodule update --recursive )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-modules; git submodule init; git submodule update --recursive )');
else:
	os.system('rm -rf ~/AMDOVX');
	os.system('(cd ; mkdir AMDOVX)');
	os.system('(cd ~/AMDOVX; git clone --recursive http://'+githubUserName+':'+githubPassword+'@github.com/'+githubUserName+'/amdovx-testscripts )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git branch -m develop-personal )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git remote add amd http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-testscripts )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git fetch --all )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git checkout -b master --track amd/master )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git checkout -b develop --track amd/develop; git pull )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps; rm -rf amdovx-testdata )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps; git clone --recursive http://'+githubUserName+':'+githubPassword+'@github.com/'+githubUserName+'/amdovx-testdata.git )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-testdata; git branch -m develop-personal )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-testdata; git remote add amd http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-testdata.git )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-testdata; git fetch --all )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-testdata; git checkout -b master --track amd/master )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-testdata; git checkout -b develop --track amd/develop; git pull )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts; git submodule init; git submodule update --recursive  )');
	os.system('(cd ~/AMDOVX/amdovx-testscripts/deps/amdovx-modules; git submodule init; git submodule update --recursive )');

# AMDOVX Build
build_dir = os.path.expanduser('~/AMDOVX/build')
if(os.path.exists(build_dir)):
	os.system('(cd ~/AMDOVX; rm -rf build)');
	os.system('(cd ~/AMDOVX; mkdir build)');
else:
	os.system('(cd ~/AMDOVX; mkdir build)');

os.system('(cd ~/AMDOVX/build; cmake -DCMAKE_BUILD_TYPE=Release ../amdovx-testscripts )');
os.system('(cd ~/AMDOVX/build; make -j8 )');
from subprocess import call
cmd='(cd ~/AMDOVX/build; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd ~/AMDOVX/build; ls -l bin )');
