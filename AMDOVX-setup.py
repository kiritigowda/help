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
    print('Invalid command line arguments. -s [Sudo Paasword] ')
    exit()

from subprocess import call
deps_dir = os.path.expanduser('~/deps')

# AMDOVX setup
if(os.path.exists(deps_dir)):
	print("\nAMDOVX Dependencies Installed\n")
else:
	print("\nAMDOVX Dependencies Installation\n")
	os.system('(cd ; mkdir deps)');
	os.system('(cd ~/deps; git clone https://github.com/RadeonOpenCompute/rocm-cmake.git )');
	os.system('(cd ~/deps; git clone https://github.com/ROCmSoftwarePlatform/MIOpenGEMM.git )');
	os.system('(cd ~/deps; git clone https://github.com/ROCmSoftwarePlatform/MIOpen.git )');
	os.system('(cd ~/deps; git clone https://github.com/google/protobuf.git )');
	os.system('(cd ~/deps; wget https://github.com/opencv/opencv/archive/3.3.0.zip )');
	os.system('(cd ~/deps; unzip 3.3.0.zip )');
	os.system('(cd ~/deps; mkdir build )');
	os.system('(cd ~/deps/build; mkdir rocm-cmake MIOpenGEMM MIOpen OpenCV )');
	os.system('(cd ~/deps/build/rocm-cmake; cmake ../../rocm-cmake )');
	os.system('(cd ~/deps/build/rocm-cmake; make -j8 )');
	cmd='(cd ~/deps/build/rocm-cmake; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd ~/deps/build/MIOpenGEMM; cmake ../../MIOpenGEMM )');
	os.system('(cd ~/deps/build/MIOpenGEMM; make -j8 )');
	cmd='(cd ~/deps/build/MIOpenGEMM; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd ~/deps/MIOpen; sudo -S cmake -P install_deps.cmake )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd ~/deps/build/MIOpen; sudo -S apt-get install libssl-dev libboost-dev libboost-system-dev libboost-filesystem-dev  )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(~/cd deps/build/MIOpen; cmake -DMIOPEN_BACKEND=OpenCL ../../MIOpen )');
	os.system('(~/cd deps/build/MIOpen; make -j8 )');
	os.system('(~/cd deps/build/MIOpen; make MIOpenDriver )');
	cmd='(cd ~/deps/build/MIOpen; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='sudo -S apt-get install autoconf automake libtool curl make g++ unzip'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd ~/deps/protobuf; ./autogen.sh )');
	os.system('(cd ~/deps/protobuf; ./configure )');
	os.system('(cd ~/deps/protobuf; make -j8 )');
	os.system('(cd ~/deps/protobuf; make check -j8 )');
	cmd='(cd ~/deps/protobuf; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd ~/deps/protobuf; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	os.system('(cd ~/deps/build/OpenCV; cmake -DWITH_OPENCL=OFF -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENCLAMDBLAS=OFF -DWITH_VA_INTEL=OFF -DWITH_OPENCL_SVM=OFF ../../opencv-3.3.0 )');
	os.system('(cd ~/deps/build/OpenCV; make -j8 )');
	cmd='(cd ~/deps/build/OpenCV; sudo -S make install )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
	cmd='(cd ~/deps/build/OpenCV; sudo -S ldconfig )'
	call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
