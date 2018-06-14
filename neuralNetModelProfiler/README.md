[![Maintainability](https://api.codeclimate.com/v1/badges/9f54c6dcd01eb87d799c/maintainability)](https://codeclimate.com/github/kiritigowda/help/maintainability)
# Neural Net Model Profiler

This folder contains scripts to setup, build, and profile AMDOVX Neural Network Extension Library. The open source GitHub project can be found at [amdovx-modules](https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules)


## Prerequisites for running the Profiler
1. ubuntu 16.04
2. [rocm supported hardware](https://rocm.github.io/hardware.html)
3. [rocm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)
4. Install cmake, wget, unzip, and git
````
sudo apt-get install cmake git wget unzip
````

## scripts 
This folder has the following python scripts

1. **NNProfiler-setup.py** - This scipts builds all the prerequisites required by amdovx modules. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If -d option for directory is not given the script will install deps folder in '~/' directory by default, else in the user specified folder.

usage:

````
python NNProfiler-setup.py -s [sudo password] -d [setup directory - optional]
```` 

2. **NNProfiler-build.py** - This scripts clones the latest amdovx modules from github, builds and installs the project. If the -d build directory is not given the script creates a AMDOVX folder in '~/' directory by default, else in the user specified folder.

usage:

````
python NNProfiler-build.py -s [sudo password] -d [build directory - optional]
```` 

3. **NNProfiler-profile.py** - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt. The build directory should be the same director passed to the NNProfiler-build.py script. If no directory was given, pass '~/' for the directory option. 

usage:

````
python NNProfiler-profile.py -d [build directory - required]
```` 

## outputs
The NNProfiler-profile.py will generate profile.txt and profile.csv.
