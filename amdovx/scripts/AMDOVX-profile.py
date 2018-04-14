import os
import getopt
import sys
import subprocess
from subprocess import call

caffeModelConfig =	[ 
   					('vgg16',3,224,224),
   					('vgg19',3,224,224),
   					('resnet50',3,224,224),
   					('resnet101',3,224,224),
   					('resnet152',3,224,224),
   					('googlenet',3,224,224),
   					('inceptionv4',3,299,299),
   					('dmnet',3,1024,2048)
					]


# Bring CaffeModels
caffeModels_dir = os.path.expanduser('~/AMDOVX/caffeModels')
if(os.path.exists(caffeModels_dir)):
	print("\nCaffeModel Folder Exist\n")
else:
	#os.system('(cd ~/AMDOVX; sshpass -p "AMD12345" scp -r client@amdovx-file-server:~/caffeModels . )');
	cmd='(cd ~/AMDOVX; scp -r client@amdovx-file-server:~/caffeModels . )'
	scpPassword = "AMD12345"
	call('echo {} | {}'.format(scpPassword, cmd), shell=True)
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


for i in range(len(caffeModelConfig)):
	modelName, channel, width, height = caffeModelConfig[i]
	print "\n",modelName,"\n"
	os.system('(cd ~/AMDOVX/develop; mkdir '+modelName+')');
	os.system('(cd ~/AMDOVX/develop/'+modelName+'; cp -r ../../caffeModels/'+modelName+' .)');
	if(modelName == 'dmnet'):
			x = 1
			print "\n",modelName," - Batch size ", x 
			x = str(x)
			os.system('(cd ~/AMDOVX/develop/'+modelName+'; mkdir build_'+x+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.caffemodel '+x+' '+str(channel)+' '+str(width)+' '+str(height)+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.prototxt '+x+' '+str(channel)+' '+str(width)+' '+str(height)+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; cmake .; make)');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../output.log)');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; ./anntest | tee -a ../../output.log)');
	else:
		for x in range(7):
			x = 2**x
			print "\n",modelName," - Batch size ", x 
			x = str(x)
			os.system('(cd ~/AMDOVX/develop/'+modelName+'; mkdir build_'+x+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.caffemodel '+x+' '+str(channel)+' '+str(width)+' '+str(height)+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.prototxt '+x+' '+str(channel)+' '+str(width)+' '+str(height)+')');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; cmake .; make)');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../output.log)');
			os.system('(cd ~/AMDOVX/develop/'+modelName+'/build_'+x+'; ./anntest | tee -a ../../output.log)');

runAwk_csv = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s,%3d,%8.3f ms,%8.3f ms\n", net, bsize, $4, $4/bsize); }' AMDOVX/develop/output.log > AMDOVX/develop/profile.csv'''
os.system(runAwk_csv);
runAwk_txt = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s %3d %8.3f ms %8.3f ms\n", net, bsize, $4, $4/bsize); }' AMDOVX/develop/output.log > AMDOVX/develop/profile.txt'''
os.system(runAwk_txt);