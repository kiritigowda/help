import os
import getopt
import sys
import subprocess

caffeModelConfig =	[ \
   					['resnet50',3,224,224],\
   					['resnet101',3,224,224],\
   					['resnet152',3,224,224],\
   					['vgg16',3,224,224],\
   					['vgg19',3,224,224],\
   					['googlenet',3,224,224],\
   					['inceptionv4',3,299,299],\
   					['dmnet',3,1024,2048]
					]

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
	os.system('(cd ~/deps/build/MIOpen; cmake -DMIOPEN_BACKEND=OpenCL ../../MIOpen )');
	os.system('(cd ~/deps/build/MIOpen; make -j8 )');
	os.system('(cd ~/deps/build/MIOpen; make MIOpenDriver )');
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
cmd='(cd ~/AMDOVX/build; sudo -S make install )'
call('echo {} | {}'.format(sudoPassword, cmd), shell=True)
os.system('(cd ~/AMDOVX/build; ls -l bin )');

# Bring CaffeModels
caffeModels_dir = os.path.expanduser('~/AMDOVX/caffeModels')
if(os.path.exists(caffeModels_dir)):
	print("\nCaffeModel Folder Exist\n")
else:
	os.system('(cd ~/AMDOVX; scp -r kiriti@amdovx-file-server:~/dataBase/caffeModels .)');
	if(os.path.exists(caffeModels_dir)):
		print("\nCaffeModel Retrived from the amdovx-file-server\n")
	else:
		print("\nERROR -- FILE SERVER CONNECTION FAILED, CHECK CONNECTION\n")
		exit()


# run caffe models
develop_dir = os.path.expanduser('~/AMDOVX/develop')
if(os.path.exists(develop_dir)):
	os.system('(cd ~/AMDOVX; rm -rf develop)');

os.system('(cd ~/AMDOVX; mkdir develop)');

print("\nVGGnet-16-layer\n")
os.system('(cd ~/AMDOVX/develop; mkdir vgg16)');
os.system('(cd ~/AMDOVX/develop/vgg16; cp -r ../../caffeModels/vgg16 .)');
for x in range(7):
	x = 2**x
	print "\nVGGnet-16-layer - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/vgg16; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../vgg16/VGGnet-16-layer.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; echo VGGnet-16-layer - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; ./anntest | tee -a ../../output.log)');

print("\nVGGnet-19-layer\n")
os.system('(cd ~/AMDOVX/develop; mkdir vgg19)');
os.system('(cd ~/AMDOVX/develop/vgg19; cp -r ../../caffeModels/vgg19 .)');
for x in range(7):
	x = 2**x
	print "\nVGGnet-19-layer - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/vgg19; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/vgg19/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../vgg19/net.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/vgg19/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/vgg19/build_'+x+'; echo VGGnet-19-layer - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/vgg19/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run googlenet
print("\ngooglenet\n")
os.system('(cd ~/AMDOVX/develop; mkdir googlenet)');
os.system('(cd ~/AMDOVX/develop/googlenet; cp -r ../../caffeModels/googlenet .)');
for x in range(7):
	x = 2**x
	print "\ngooglenet - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/googlenet; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../googlenet/net.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; echo googlenet - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run inceptionV4
print("\ninceptionV4\n")
os.system('(cd ~/AMDOVX/develop; mkdir inceptionv4)');
os.system('(cd ~/AMDOVX/develop/inceptionv4; cp -r ../../caffeModels/inceptionv4 .)');
for x in range(7):
	x = 2**x
	print "\ninceptionV4 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/inceptionv4; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../inceptionv4/inception-v4.caffemodel '+x+' 3 299 299)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; echo inceptionv4 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet50
print("\nresnet50\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet50)');
os.system('(cd ~/AMDOVX/develop/resnet50; cp -r ../../caffeModels/resnet/resnet50 .)');
for x in range(7):
	x = 2**x
	print "\nresnet50 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet50; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet50/ResNet-50-model.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; echo resnet50 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet101
print("\nresnet101\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet101)');
os.system('(cd ~/AMDOVX/develop/resnet101; cp -r ../../caffeModels/resnet/resnet101 .)');
for x in range(7):
	x = 2**x
	print "\nresnet101 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet101; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet101/ResNet-101-model.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; echo resnet101 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet152
print("\nresnet152\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet152)');
os.system('(cd ~/AMDOVX/develop/resnet152; cp -r ../../caffeModels/resnet/resnet152 .)');
for x in range(7):
	x = 2**x
	print "\nresnet152 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet152; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet152/ResNet-152-model.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; echo resnet152 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run dmnet
print("\nDMNet\n")
os.system('(cd ~/AMDOVX/develop; mkdir dmnet)');
os.system('(cd ~/AMDOVX/develop/dmnet; cp -r ../../caffeModels/dmnet .)');
for x in range(1):
	x = 2**x
	print "\nDMNet - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/dmnet; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../dmnet/weights.caffemodel '+x+' 3 1024 2048)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; echo DMNet - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; ./anntest | tee -a ../../output.log)');
