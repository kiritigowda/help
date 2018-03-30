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

from subprocess import call

# Bring CaffeModels
caffeModels_dir = os.path.expanduser('~/AMDOVX/caffeModels')
if(os.path.exists(caffeModels_dir)):
	print("\nCaffeModel Folder Exist\n")
else:
	os.system('(cd ~/AMDOVX; sshpass -p 'AMD12345' scp -r client@amdovx-file-server:~/caffeModels . )');
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

print("\nvgg19 layer\n")
os.system('(cd ~/AMDOVX/develop; mkdir vgg16)');
os.system('(cd ~/AMDOVX/develop/vgg16; cp -r ../../caffeModels/vgg16 .)');
for x in range(7):
	x = 2**x
	print "\nVGGnet-16-layer - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/vgg16; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../vgg16/vgg16.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; echo VGGnet-16-layer - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/vgg16/build_'+x+'; ./anntest | tee -a ../../output.log)');

print("\nvgg19 layer\n")
os.system('(cd ~/AMDOVX/develop; mkdir vgg19)');
os.system('(cd ~/AMDOVX/develop/vgg19; cp -r ../../caffeModels/vgg19 .)');
for x in range(7):
	x = 2**x
	print "\nVGGnet-19-layer - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/vgg19; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/vgg19/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../vgg19/vgg19.caffemodel '+x+' 3 224 224)');
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
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../googlenet/googlenet.caffemodel '+x+' 3 224 224, caffe2openvx ../googlenet/googlenet.prototxt '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; echo googlenet - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/googlenet/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run inceptionV4
print("\inceptionv4\n")
os.system('(cd ~/AMDOVX/develop; mkdir inceptionv4)');
os.system('(cd ~/AMDOVX/develop/inceptionv4; cp -r ../../caffeModels/inceptionv4 .)');
for x in range(7):
	x = 2**x
	print "\inceptionv4 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/inceptionv4; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../inceptionv4/inceptionv4.caffemodel '+x+' 3 299 299)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; echo inceptionv4 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/inceptionv4/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet50
print("\nresnet50\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet50)');
os.system('(cd ~/AMDOVX/develop/resnet50; cp -r ../../caffeModels/resnet50 .)');
for x in range(7):
	x = 2**x
	print "\nresnet50 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet50; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet50/resnet50.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; echo resnet50 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet50/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet101
print("\nresnet101\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet101)');
os.system('(cd ~/AMDOVX/develop/resnet101; cp -r ../../caffeModels/resnet101 .)');
for x in range(7):
	x = 2**x
	print "\nresnet101 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet101; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet101/resnet101.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; echo resnet101 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet101/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run resnet152
print("\nresnet152\n")
os.system('(cd ~/AMDOVX/develop; mkdir resnet152)');
os.system('(cd ~/AMDOVX/develop/resnet152; cp -r ../../caffeModels/resnet152 .)');
for x in range(7):
	x = 2**x
	print "\nresnet152 - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/resnet152; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../resnet152/resnet152.caffemodel '+x+' 3 224 224)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; echo resnet152 - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/resnet152/build_'+x+'; ./anntest | tee -a ../../output.log)');

# run dmnet
print("\dmnet\n")
os.system('(cd ~/AMDOVX/develop; mkdir dmnet)');
os.system('(cd ~/AMDOVX/develop/dmnet; cp -r ../../caffeModels/dmnet .)');
for x in range(1):
	x = 2**x
	print "\nDMNet - Batch size ", x 
	x = str(x)
	os.system('(cd ~/AMDOVX/develop/dmnet; mkdir build_'+x+')');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../dmnet/dmnet.caffemodel '+x+' 3 1024 2048)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; cmake .; make)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; echo DMNet - Batch size '+x+'  | tee -a ../../output.log)');
	os.system('(cd ~/AMDOVX/develop/dmnet/build_'+x+'; ./anntest | tee -a ../../output.log)');
