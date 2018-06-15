# AMD Neural Net Inference Docker

## Prerequisites for running the Profiler
* ubuntu 16.04.3 LTS
* rocm supported hardware (Vega 10 - Frontier)
* rocm-dkms

### Starting from a fresh Ubuntu 16.04.3 LTS
````
sudo apt update
sudo apt dist-upgrade
sudo apt install libnuma-dev
sudo reboot
````
````
sudo apt install linux-headers-4.13.0-32-generic linux-image-4.13.0-32-generic linux-image-extra-4.13.0-32-generic linux-signed-image-4.13.0-32-generic
sudo reboot 
````
````
wget -qO - http://repo.radeon.com/rocm/apt/debian/rocm.gpg.key | sudo apt-key add -
sudo sh -c 'echo deb [arch=amd64] http://repo.radeon.com/rocm/apt/debian/ xenial main > /etc/apt/sources.list.d/rocm.list'
sudo apt update
sudo apt install rocm-dkms
sudo reboot
````

## Step 1 - *Setup Docker*
````
sudo apt-get install curl
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo systemctl status docker
````

## Step 2 - *Get Docker Image*
````
sudo docker pull kiritigowda/ubuntu_16.04.3:amdovx-drop
````

## Step 3 - *Run the docker image*
````
sudo docker run -it --device=/dev/kfd --device=/dev/dri --group-add video --network host kiritigowda/ubuntu_16.04.3:amdovx-drop
````
## Step 4 - *Run Resnet50 Test*

### caffe2openvx flow - Trained Caffe Model conversion to OpenVX Graph
````
. ~/rocmrc 
cd ~/AMDOVX/
mkdir build
cd build/
caffe2openvx ../caffeModels/resnet50/resnet50.caffemodel 1 3 224 224
cmake .
make
./anntest 
````

### caffe2nnir & nnir2openvx - Trained Caffe Model conversion to Neural Net Intermeditate Format (NNIR) to OpenVX Graph

````
. ~/rocmrc 
cd ~/AMDOVX/
mkdir build
cd build/
python ../amdovx-modules/utils/model_compiler/python/caffe2nnir.py ../caffeModels/resnet50/resnet50.caffemodel resnet50 --input-dims 1,3,224,224
python ../amdovx-modules/utils/model_compiler/python/nnir2openvx.py resnet50/ resnet50-build
cd resnet50-build/
cmake .
make
./anntest weights.bin 
````

