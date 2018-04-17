import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:')
 
sudoPassword = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg

if sudoPassword == '':
    print('Invalid command line arguments. -s [Sudo Password] is required')
    exit()

# AMDOVX Work Flow
deps_dir = os.path.expanduser('~/AMDOVX/amdovx-modules')
if(os.path.exists(deps_dir)):
	print("\nGit Folder Exist\n")
	os.system('(cd ~/AMDOVX/amdovx-modules; git pull; git submodule init; git submodule update --recursive )');
else:
	os.system('rm -rf ~/AMDOVX');
	os.system('(cd ; mkdir AMDOVX)');
	os.system('(cd ~/AMDOVX; git clone --recursive -b develop http://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules )');
	os.system('(cd ~/AMDOVX/amdovx-modules; git submodule init; git submodule update --recursive  )');

# AMDOVX Build
build_dir = os.path.expanduser('~/AMDOVX/build')
if(os.path.exists(build_dir)):
	os.system('(cd ~/AMDOVX; rm -rf build)');
	os.system('(cd ~/AMDOVX; mkdir build)');
else:
	os.system('(cd ~/AMDOVX; mkdir build)');

os.system('(cd ~/AMDOVX/build; cmake -DCMAKE_BUILD_TYPE=Release ../amdovx-modules )');
os.system('(cd ~/AMDOVX/build; make -j8 )');
from subprocess import call
cmd='(cd ~/AMDOVX/build; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd ~/AMDOVX/build; ls -l bin )');
