import os
import getopt
import sys
import subprocess
from subprocess import call

# caffe models to benchmark
caffeModelConfig =	[ 
					('dmnet',3,1024,2048),
					('googlenet',3,224,224),
					('inceptionv4',3,299,299),
					('resnet50',3,224,224),
					('resnet101',3,224,224),
					('resnet152',3,224,224),
					('vgg16',3,224,224),
					('vgg19',3,224,224)
					]

opts, args = getopt.getopt(sys.argv[1:], 'd:')

buildDir = ''

for opt, arg in opts:
    if opt == '-d':
    	buildDir = arg

if buildDir == '':
    print('Invalid command line arguments. -d [build directory - required] ')
    exit()

if buildDir == '':
	buildDir_AMDOVX = '~/AMDOVX'
else:
	buildDir_AMDOVX = buildDir+'AMDOVX'

# Bring CaffeModels
caffeModels_dir = os.path.expanduser(buildDir_AMDOVX+'/caffeModels')
if(os.path.exists(caffeModels_dir)):
	print("\nCaffeModel Folder Exist\n")
else:
	os.system('(cd '+buildDir_AMDOVX+'; scp -r client@amdovx-file-server:~/caffeModels . )');
	if(os.path.exists(caffeModels_dir)):
		print("\nCaffeModel Retrived from the amdovx-file-server\n")
	else:
		print("\nERROR -- FILE SERVER CONNECTION FAILED, CHECK CONNECTION\n")
		exit()


# run caffe models
develop_dir = os.path.expanduser(buildDir_AMDOVX+'/develop')
if(os.path.exists(develop_dir)):
	os.system('(cd '+buildDir_AMDOVX+'; rm -rf develop)');

os.system('(cd '+buildDir_AMDOVX+'; mkdir develop)');


# run caffe2openvx flow
for i in range(len(caffeModelConfig)):
	modelName, channel, height, width = caffeModelConfig[i]
	print "\n caffe2openvx -- ",modelName,"\n"
	os.system('(cd '+develop_dir+'; mkdir '+modelName+')');
	os.system('(cd '+develop_dir+'/'+modelName+'; cp -r ../../caffeModels/'+modelName+' .)');
	if(modelName == 'dmnet'):
			x = 1
			print "\n",modelName," - Batch size ", x
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.caffemodel '+x+' '+str(channel)+' '+str(height)+' '+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.prototxt '+x+' '+str(channel)+' '+str(height)+' '+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; ./anntest | tee -a ../../output.log)');
	else:
		for x in range(7):
			x = 2**x
			print "\n",modelName," - Batch size ", x
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.caffemodel '+x+' '+str(channel)+' '+str(height)+' '+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; export PATH=$PATH:/opt/rocm/bin; export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib; caffe2openvx ../'+modelName+'/'+modelName+'.prototxt '+x+' '+str(channel)+' '+str(height)+' '+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/build_'+x+'; ./anntest | tee -a ../../output.log)');

runAwk_csv = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s,%3d,%8.3f ms,%8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/output.log > '''+develop_dir+'''/caffe2openvx_profile.csv'''
os.system(runAwk_csv);
runAwk_txt = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s %3d %8.3f ms %8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/output.log > '''+develop_dir+'''/caffe2openvx_profile.txt'''
os.system(runAwk_txt);


# run caffe2nnir2openvx no fuse flow
modelCompilerScripts_dir = os.path.expanduser(buildDir_AMDOVX+'/amdovx-modules/utils/model_compiler/python')
print(modelCompilerScripts_dir)
for i in range(len(caffeModelConfig)):
	modelName, channel, height, width = caffeModelConfig[i]
	print "\n caffe2nnir2openvx --",modelName,"\n"
	if(modelName == 'dmnet'):
			x = 1
			print "\n",modelName," - Batch size ", x
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir nnir_build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; python '+modelCompilerScripts_dir+'/caffe2nnir.py ../'+modelName+'/'+modelName+'.caffemodel . --input-dims '+x+','+str(channel)+','+str(height)+','+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; python '+modelCompilerScripts_dir+'/nnir2openvx.py . .)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../nnir_output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; ./anntest weights.bin | tee -a ../../nnir_output.log)');
	else:
		for x in range(7):
			x = 2**x
			print "\n",modelName," - Batch size ", x
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir nnir_build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; python '+modelCompilerScripts_dir+'/caffe2nnir.py ../'+modelName+'/'+modelName+'.caffemodel . --input-dims '+x+','+str(channel)+','+str(height)+','+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; python '+modelCompilerScripts_dir+'/nnir2openvx.py . .)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../nnir_output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_build_'+x+'; ./anntest weights.bin | tee -a ../../nnir_output.log)');

runAwk_csv = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s,%3d,%8.3f ms,%8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/nnir_output.log > '''+develop_dir+'''/caffe2nnir2openvx_noFuse_profile.csv'''
os.system(runAwk_csv);
runAwk_txt = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s %3d %8.3f ms %8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/nnir_output.log > '''+develop_dir+'''/caffe2nnir2openvx_noFuse_profile.txt'''
os.system(runAwk_txt);

# run caffe2nnir2openvx with fuse flow
modelCompilerScripts_dir = os.path.expanduser(buildDir_AMDOVX+'/amdovx-modules/utils/model_compiler/python')
print(modelCompilerScripts_dir)
for i in range(len(caffeModelConfig)):
	modelName, channel, height, width = caffeModelConfig[i]
	print "\n caffe2nnir2openvx --",modelName,"\n"
	if(modelName == 'dmnet'):
			x = 1
			print "\n",modelName," - Batch size ", x 
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir nnir_fuse_build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; python '+modelCompilerScripts_dir+'/caffe2nnir.py ../'+modelName+'/'+modelName+'.caffemodel . --input-dims '+x+','+str(channel)+','+str(height)+','+str(width)+')');
			
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; python '+modelCompilerScripts_dir+'/nnir2openvx.py . .)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../nnir_fuse_output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; ./anntest weights.bin | tee -a ../../nnir_fuse_output.log)');
	else:
		for x in range(7):
			x = 2**x
			print "\n",modelName," - Batch size ", x 
			x = str(x)
			os.system('(cd '+develop_dir+'/'+modelName+'; mkdir nnir_fuse_build_'+x+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; python '+modelCompilerScripts_dir+'/caffe2nnir.py ../'+modelName+'/'+modelName+'.caffemodel . --input-dims '+x+','+str(channel)+','+str(height)+','+str(width)+')');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; python '+modelCompilerScripts_dir+'/nnir-update.py --fuse-ops 1 . .)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; python '+modelCompilerScripts_dir+'/nnir2openvx.py . .)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; cmake .; make)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; echo '+modelName+' - Batch size '+x+'  | tee -a ../../nnir_fuse_output.log)');
			os.system('(cd '+develop_dir+'/'+modelName+'/nnir_fuse_build_'+x+'; ./anntest weights.bin | tee -a ../../nnir_fuse_output.log)');

runAwk_csv = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s,%3d,%8.3f ms,%8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/nnir_fuse_output.log > '''+develop_dir+'''/caffe2nnir2openvx_fuse_profile.csv'''
os.system(runAwk_csv);
runAwk_txt = r'''awk 'BEGIN { net = "xxx"; bsize = 1; } / - Batch size/ { net = $1; bsize = $5; } /average over 100 iterations/ { printf("%-16s %3d %8.3f ms %8.3f ms\n", net, bsize, $4, $4/bsize); }' '''+develop_dir+'''/nnir_fuse_output.log > '''+develop_dir+'''/caffe2nnir2openvx_fuse_profile.txt'''
os.system(runAwk_txt);
