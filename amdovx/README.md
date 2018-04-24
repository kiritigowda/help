[![Maintainability](https://api.codeclimate.com/v1/badges/9f54c6dcd01eb87d799c/maintainability)](https://codeclimate.com/github/kiritigowda/help/maintainability)
# AMDOVX Neural Network Extension Library - Model Profiler

This folder contains scripts to setup, build, and profile AMDOVX Neural Network Extension Library. The open source GitHub project can be found at [amdovx-modules](https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules)

## scripts 

Prerequisites for running the scripts
1. [rocm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)
2. Install cmake and git
````
sudo apt-get install cmake git
````


This folder has the following python scripts

1. AMDOVX-setup.py - This scipts builds all the prerequisites required by amdovx modules. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If -d option for directory is not given the script will install deps folder in '~/' directory by default, else in the user specified folder.

usage:

````
python AMDOVX-setup.py -s [sudo password] -d [setup directory - optional]
```` 

2. AMDOVX-build.py - This scripts clones the latest amdovx modules from github, builds and installs the project. If the -d build directory is not given the script creates a AMDOVX folder in '~/' directory by default, else in the user specified folder.

usage:

````
python AMDOVX-build.py -s [sudo password] -d [build directory - optional]
```` 

3. AMDOVX-profile.py - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt. The build directory should be the same director passed to the AMDOVX-build.py script. If no directory was given, pass '~/' for the directory option. 

usage:

````
python AMDOVX-profile.py -d [build directory - required]
```` 

## output
The AMDOVX-profile.py will generate profile.txt and profile.csv.
