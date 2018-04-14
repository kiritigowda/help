# AMDOVX Help 

This folder contains scripts to setup, build, and profile AMDOVX Neural Network Extension Library. The open source GitHub project can be found at [amdovx-modules](https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules)

## scripts 

Prerequisites for running the scripts
1. [rocm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)
2. Install cmake and git
````
sudo apt-get install cmake git
````


This folder has the following python scripts

1. AMDOVX-setup.py - This scipts builds all the prerequisites required by amdovx modules. The setup script creates a deps folder in the home directory and installs all the prerequisites, this script only needs to be executed once.

usage:

````
python AMDOVX-setup.py -s [sudo password]
```` 

2. AMDOVX-build.py - This scripts clones the latest amdovx modules from github, builds and installs the project.

usage:

````
python AMDOVX-build.py -s [sudo password]
```` 

3. AMDOVX-profile.py - This script downloads the caffe .models & .prototxt from a remote file server and runs every model with different batch sizes and dumps an output.log file, profile.csv & profile.txt.

usage:

````
python AMDOVX-profile.py
```` 
