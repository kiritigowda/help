[![Maintainability](https://api.codeclimate.com/v1/badges/9f54c6dcd01eb87d799c/maintainability)](https://codeclimate.com/github/kiritigowda/help/maintainability)

# AMDOVX Neural Network Inference Engine - ANNIE Installer

This folder contains scripts to setup, build, and help run AMDOVX Neural Network Inference Engine. The open source GitHub project can be found at [amdovx-modules](https://github.com/GPUOpen-ProfessionalCompute-Libraries/amdovx-modules#amd-openvx-modules-amdovx-modules)

## Prerequisites for running the installer

1. ubuntu 16.04
2. [rocm supported hardware](https://rocm.github.io/hardware.html)
3. [rocm](https://github.com/RadeonOpenCompute/ROCm#installing-from-amd-rocm-repositories)
4. QTCreator, and QT5 or above
````
sudo apt-get install qt5-default qtcreator
````
5. install cmake and git
````
sudo apt-get install cmake git
````
## Installer
**RadeonInferenceInstaller.py** - Run this installer script to install all the dependencies and build the Inference Server.

**Usage** - To install the dependencies and the inference engine, cd into the scripts folder of this project and run the RadeonInferenceInstaller script as shown below.
````
python RadeonInferenceInstaller.py -s [sudo password - required] -d [dependencies directory - optional] -b [build directory - optional]
````

## Scripts 
This folder has the following python scripts in scripts folder

1. **inference-setup.py** - This script builds all the prerequisites required by inference modules. The setup script creates a deps folder and installs all the prerequisites, this script only needs to be executed once. If the -d option for directory is not given the script will install deps folder in '~/'or 'home' directory by default, else in the user specified folder.

usage:

````
python inference-setup.py -s [sudo password] -d [setup directory - optional]
```` 

2. **inference-build.py** - This script clones the latest inference modules from github, builds and installs the project. If the -d build directory is not given the script creates a AMDOVX folder in '~/' directory by default, else in the user specified folder.

usage:

````
python inference-build.py -s [sudo password] -d [build directory - optional]
```` 

3. **RadeonInferenceInstaller.py** - This installer script will run the inference setup and build scripts mentioned above.
````
python RadeonInferenceInstaller.py -s [sudo password - required] -d [dependencies directory - optional] -b [build directory - optional]
````
## Running the Inference Engine 

1. Step 1 - Launch **Inference Server Application** - is built by the installer script. You can launch the server using the following commands 
````
export PATH=$PATH:/opt/rocm/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rocm/lib
annInferenceServer
````
2. Step 2 - Launch **Inference Client Application** - The client Application is available in -b option directory (build directory passed to the installer) or the home directory if -b option was not used. 

  * -B_DIR_OR_HOME_DIR/**AMDOVX/amdovx-modules/utils/annInferenceApp** folder. 

  * Open annInferenceApp.pro with the QTCreator and build the client application. Once the client is built, launch the application. Below is the image of the client application

![Inference Client](images/annInferenceClientApp.png "Inference Client Application")

3. Step 3 - Connect Server and Client - After launching the server and client applications on the system, you can connect them using the default port. The server and client could also be launched on two different machines.

![Inference Client Connect](images/serverConnect.png "Inference Client Connect")

4. Step 4 - Upload Caffe Model - Once the connection is established, load the caffe model and prototxt to the server using the client application. 

The client application section Inference Complier needs to be completed as shown in the below example.

![Inference Client Model Upload](images/modelUploader.png "Inference Client Model Upload")
  * CNN Model: upload or select preloaded models. (User needs to save models are preloaded on the server)
  * CxHxW(inp): enter the height and width of the input images to the model
  * Prototxt: give the location of the model .prototxt
  * CaffeModel: give the location of the pretrained caffe model .caffemodel
  * Options: BGR/RGB  Publishas: Model Name and password: radeon ( To load the models to the server)

5. Step 5 - Load Image DataBase - Now you can run a simple test inference using the tinyDataSet provided in this help project within the sampleDataSet folder. 

The client application section Inference Run-time needs the labels.txt, the AMD-tinyDataSet folder location, & AMD-tinyDataSet-val.txt provided in the sampleDataSet folder.
![Inference Client Image Upload](images/inferenceRunTime.png "Inference Client Image Upload")
  * Labels: location to /radeonInferenceInstaller/sampleDataSet/labels.txt
  * Image Folder: location to /radeonInferenceInstaller/sampleDataSet/AMD-tinyDataSet folder
  * Image List: location to /radeonInferenceInstaller/sampleDataSet/AMD-tinyDataSet-val.txt (image validation text)

6. Step 6 - Run Inference - Once all the required fields are completed on the client app the run button will turn green. You can now run the inference.


# Inference RunTime Video

[![Radeon Inference](images/inferenceVideo.png)](http://www.youtube.com/watch?v=0GLmnrpMSYs)
