import os
import getopt
import sys
import subprocess
 

opts, args = getopt.getopt(sys.argv[1:], 's:d:')
 
sudoPassword = ''
setupDir = ''

for opt, arg in opts:
    if opt == '-s':
        sudoPassword = arg
    elif opt =='-d':
    	setupDir = arg

if sudoPassword == '':
    print('Invalid command line arguments. -s [sudo password - required] -d [setup directory - optional] ')
    exit()

if setupDir == '':
	setupDir_deps = '~/deps'
else:
	setupDir_deps = setupDir+'deps'

from subprocess import call
deps_dir = os.path.expanduser(setupDir_deps)

# AMDOVX setup
if(os.path.exists(deps_dir)):
	print("\nAMDOVX Dependencies Installed\n")
else:
	print("\nAMDOVX Dependencies Installation\n")
	os.system('(cd '+setupDir+'; mkdir deps)');
	os.system('(cd '+deps_dir+'; git clone https://github.com/RadeonOpenCompute/rocm-cmake.git )');
	os.system('(cd '+deps_dir+'; git clone https://github.com/ROCmSoftwarePlatform/MIOpenGEMM.git )');
	os.system('(cd '+deps_dir+'; git clone https://github.com/ROCmSoftwarePlatform/MIOpen.git )');
	os.system('(cd '+deps_dir+'; git clone https://github.com/google/protobuf.git )');
	os.system('(cd '+deps_dir+'; wget https://github.com/opencv/opencv/archive/3.3.0.zip )');
	os.system('(cd '+deps_dir+'; unzip 3.3.0.zip )');
	os.system('(cd '+deps_dir+'; mkdir build )');
	os.system('(cd '+deps_dir+'/build; mkdir rocm-cmake MIOpenGEMM MIOpen OpenCV )');
	os.system('(cd '+deps_dir+'/build/rocm-cmake; cmake ../../rocm-cmake )');
	os.system('(cd '+deps_dir+'/build/rocm-cmake; make -j8 )');
	cmd='(cd '+deps_dir+'/build/rocm-cmake; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/MIOpenGEMM; cmake ../../MIOpenGEMM )');
	os.system('(cd '+deps_dir+'/build/MIOpenGEMM; make -j8 )');
	cmd='(cd '+deps_dir+'/build/MIOpenGEMM; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/MIOpen; sudo -S cmake -P install_deps.cmake )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S apt-get install libssl-dev libboost-dev libboost-system-dev libboost-filesystem-dev  )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/MIOpen; cmake -DMIOPEN_BACKEND=OpenCL ../../MIOpen )');
	os.system('(cd '+deps_dir+'/build/MIOpen; make -j8 )');
	os.system('(cd '+deps_dir+'/build/MIOpen; make MIOpenDriver )');
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S apt autoremove )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/MIOpen; sudo -S apt autoclean )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S apt-get install autoconf automake libtool curl make g++ unzip )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S apt autoremove )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S apt autoclean )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/protobuf; git submodule update --init --recursive )');
	os.system('(cd '+deps_dir+'/protobuf; ./autogen.sh )');
	os.system('(cd '+deps_dir+'/protobuf; ./configure )');
	os.system('(cd '+deps_dir+'/protobuf; make -j16 )');
	os.system('(cd '+deps_dir+'/protobuf; make check -j16 )');
	cmd='(cd '+deps_dir+'/protobuf; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S apt-get install python-pip )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/protobuf; sudo -S pip install protobuf )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd '+deps_dir+'/build/OpenCV; cmake -DWITH_OPENCL=OFF -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENCLAMDBLAS=OFF -DWITH_VA_INTEL=OFF -DWITH_OPENCL_SVM=OFF ../../opencv-3.3.0 )');
	os.system('(cd '+deps_dir+'/build/OpenCV; make -j8 )');
	cmd='(cd '+deps_dir+'/build/OpenCV; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd '+deps_dir+'/build/OpenCV; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
