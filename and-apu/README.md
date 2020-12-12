# MIVisionX Inference on AMD Accelerated Processing Unit (APU)

[MIVisionX](https://gpuopen-professionalcompute-libraries.github.io/MIVisionX/) toolkit is a set of comprehensive computer vision and machine intelligence libraries, utilities, and applications bundled into a single toolkit. AMD MIVisionX delivers highly optimized open-source implementation of the Khronos OpenVX™ and OpenVX™ Extensions along with Convolution Neural Net Model Compiler & Optimizer supporting ONNX, and Khronos NNEF™ exchange formats. The toolkit allows for rapid prototyping and deployment of optimized computer vision and machine learning inference workloads on a wide range of computer hardware, including small embedded x86 CPUs, APUs, discrete GPUs, and heterogeneous servers.

* [Inference with MIVisionX](#inference)
* [Accelerated Processing Unit](#accelerated-processing-unit)
* [Pre-requisites](#pre-requisites)
* [Steps to Run Inference on AMD APU](#steps-to-run-inference-on-amd-apu)

## Inference
MIVisionX component [Neural Net Model Compiler & Optimizer](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/tree/master/model_compiler#neural-net-model-compiler--optimizer) converts pre-trained neural network models to MIVisionX runtime code for optimized inference

<p align="center"><img width="80%" src="https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/raw/master/docs/images/modelCompilerWorkflow.png" /></p>

Pre-trained models in [ONNX](https://onnx.ai/), [NNEF](https://www.khronos.org/nnef), & [Caffe](http://caffe.berkeleyvision.org/) formats are supported by the model compiler & optimizer. The model compiler first converts the pre-trained models to AMD Neural Net Intermediate Representation (NNIR), once the model has been translated into AMD NNIR (AMD's internal open format), the Optimizer goes through the NNIR and applies various optimizations which would allow the model to be deployed on to target hardware most efficiently. Finally, AMD NNIR is converted into OpenVX C code, which could be compiled and deployed on any targeted AMD hardware.

<p align="center"><img width="80%" src="https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/raw/master/docs/images/frameworks.png" /></p>

## Accelerated Processing Unit
The AMD Accelerated Processing Unit (APU), formerly known as Fusion, is the term used for a series of 64-bit microprocessors from AMD, designed to act as a central processing unit (CPU) and graphics processing unit (GPU) on a single die.

### APUs targeted

* [AMD Ryzen™ Mobile Processors with Radeon™ Graphics](https://www.amd.com/en/products/ryzen-processors-laptop)
* [AMD Ryzen™ Embedded Processors with Radeon™ Graphics](https://www.amd.com/en/products/embedded-ryzen-series)

## Pre-requisites

* Hardware - ROCm OpenCL supported APU 
* Operating System - Ubuntu `18.04.5` LTS (Bionic Beaver)

## Steps to Run Inference on AMD APU

### Step 1: [Install Ubuntu](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview) 18.04.5 on the system with AMD APU

* Get [Ubuntu 18.04.5 LTS (Bionic Beaver)](https://releases.ubuntu.com/bionic/)
* Follow [installation instructions](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview)

```
% cat /etc/lsb-release 
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=18.04
DISTRIB_CODENAME=bionic
DISTRIB_DESCRIPTION="Ubuntu 18.04.5 LTS"
```

### Step 2: Enable IOMMU feature in BIOS

IOMMU (I/O Memory Management Unit) is a feature supported by motherboard chipsets that provide enhanced virtual-to-physical memory mapping capabilities, including the ability to map large portions of non-contiguous memory. IOMMU can be enabled in the motherboard's BIOS, in order to resolve issues with virtual machine device drivers.

* Check your system BIOS manufacturers manual for information on how to enable IOMMU

### Step 3: Install `ROCm 3.10`

#### Run the following code to ensure that your system is up to date:

```
sudo apt update

sudo apt dist-upgrade

sudo apt install libnuma-dev

sudo reboot
```

#### Add the ROCm apt repository:

```
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -

echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/3.10/ xenial main' | sudo tee /etc/apt/sources.list.d/rocm.list
```

#### Install the ROCm meta-package. Update the appropriate repository list and install the rocm-dkms meta-package:

```
sudo apt update

sudo apt install rocm-dkms && sudo reboot
```

#### Verify installation

* `rocminfo`

```
% /opt/rocm/bin/rocminfo

ROCk module is loaded
Able to open /dev/kfd read-write
=====================    
HSA System Attributes    
=====================    
Runtime Version:         1.1
System Timestamp Freq.:  1000.000000MHz
Sig. Max Wait Duration:  18446744073709551615 (0xFFFFFFFFFFFFFFFF) (timestamp count)
Machine Model:           LARGE                              
System Endianness:       LITTLE                             

==========               
HSA Agents               
==========               
*******                  
Agent 1                  
*******                  
  Name:                    AMD Ryzen Embedded V1605B with Radeon Vega Gfx
  Uuid:                    CPU-XX                             
  Marketing Name:          AMD Ryzen Embedded V1605B with Radeon Vega Gfx
  Vendor Name:             CPU                                
  Feature:                 None specified                     
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        0(0x0)                             
  Queue Min Size:          0(0x0)                             
  Queue Max Size:          0(0x0)                             
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             CPU                                
  Cache Info:              
    L1:                      32(0x20) KB                        
  Chip ID:                 5597(0x15dd)                       
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   2000                               
  BDFID:                   1024                               
  Internal Node ID:        0                                  
  Compute Unit:            8                                  
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                None
  Pool Info:               
    Pool 1                   
      Segment:                 GLOBAL; FLAGS: KERNARG, FINE GRAINED
      Size:                    16776832(0xfffe80) KB              
      Allocatable:             TRUE                               
      Alloc Granule:           4KB                                
      Alloc Alignment:         4KB                                
      Accessible by all:       TRUE                               
  ISA Info:                
    N/A                      
*******                  
Agent 2                  
*******                  
  Name:                    gfx902                             
  Uuid:                    GPU-XX                             
  Marketing Name:          AMD Ryzen Embedded V1605B with Radeon Vega Gfx
  Vendor Name:             AMD                                
  Feature:                 KERNEL_DISPATCH                    
  Profile:                 FULL_PROFILE                       
  Float Round Mode:        NEAR                               
  Max Queue Number:        128(0x80)                          
  Queue Min Size:          4096(0x1000)                       
  Queue Max Size:          131072(0x20000)                    
  Queue Type:              MULTI                              
  Node:                    0                                  
  Device Type:             GPU                                
  Cache Info:              
    L1:                      16(0x10) KB                        
  Chip ID:                 5597(0x15dd)                       
  Cacheline Size:          64(0x40)                           
  Max Clock Freq. (MHz):   1100                               
  BDFID:                   1024                               
  Internal Node ID:        0                                  
  Compute Unit:            11                                 
  SIMDs per CU:            4                                  
  Shader Engines:          1                                  
  Shader Arrs. per Eng.:   1                                  
  WatchPts on Addr. Ranges:4                                  
  Features:                KERNEL_DISPATCH 
  Fast F16 Operation:      FALSE                              
  Wavefront Size:          64(0x40)                           
  Workgroup Max Size:      1024(0x400)                        
  Workgroup Max Size per Dimension:
    x                        1024(0x400)                        
    y                        1024(0x400)                        
    z                        1024(0x400)                        
  Max Waves Per CU:        160(0xa0)                          
  Max Work-item Per CU:    10240(0x2800)                      
  Grid Max Size:           4294967295(0xffffffff)             
  Grid Max Size per Dimension:
    x                        4294967295(0xffffffff)             
    y                        4294967295(0xffffffff)             
    z                        4294967295(0xffffffff)             
  Max fbarriers/Workgrp:   32                                 
  Pool Info:               
    Pool 1                   
      Segment:                 GROUP                              
      Size:                    64(0x40) KB                        
      Allocatable:             FALSE                              
      Alloc Granule:           0KB                                
      Alloc Alignment:         0KB                                
      Accessible by all:       FALSE                              
  ISA Info:                
    ISA 1                    
      Name:                    amdgcn-amd-amdhsa--gfx902+xnack    
      Machine Models:          HSA_MACHINE_MODEL_LARGE            
      Profiles:                HSA_PROFILE_BASE                   
      Default Rounding Mode:   NEAR                               
      Default Rounding Mode:   NEAR                               
      Fast f16:                TRUE                               
      Workgroup Max Size:      1024(0x400)                        
      Workgroup Max Size per Dimension:
        x                        1024(0x400)                        
        y                        1024(0x400)                        
        z                        1024(0x400)                        
      Grid Max Size:           4294967295(0xffffffff)             
      Grid Max Size per Dimension:
        x                        4294967295(0xffffffff)             
        y                        4294967295(0xffffffff)             
        z                        4294967295(0xffffffff)             
      FBarrier Max Size:       32                                 
*** Done ***            
```

* `clinfo`

```
% /opt/rocm/opencl/bin/clinfo

Number of platforms:				 1
  Platform Profile:				 FULL_PROFILE
  Platform Version:				 OpenCL 2.0 AMD-APP (3212.0)
  Platform Name:				 AMD Accelerated Parallel Processing
  Platform Vendor:				 Advanced Micro Devices, Inc.
  Platform Extensions:				 cl_khr_icd cl_amd_event_callback 


  Platform Name:				 AMD Accelerated Parallel Processing
Number of devices:				 1
  Device Type:					 CL_DEVICE_TYPE_GPU
  Vendor ID:					 1002h
  Board name:					 AMD Ryzen Embedded V1605B with Radeon Vega Gfx
  Device Topology:				 PCI[ B#4, D#0, F#0 ]
  Max compute units:				 11
  Max work items dimensions:			 3
    Max work items[0]:				 1024
    Max work items[1]:				 1024
    Max work items[2]:				 1024
  Max work group size:				 256
  Preferred vector width char:			 4
  Preferred vector width short:			 2
  Preferred vector width int:			 1
  Preferred vector width long:			 1
  Preferred vector width float:			 1
  Preferred vector width double:		 1
  Native vector width char:			 4
  Native vector width short:			 2
  Native vector width int:			 1
  Native vector width long:			 1
  Native vector width float:			 1
  Native vector width double:			 1
  Max clock frequency:				 1100Mhz
  Address bits:					 64
  Max memory allocation:			 6695813120
  Image support:				 Yes
  Max number of images read arguments:		 128
  Max number of images write arguments:		 8
  Max image 2D width:				 16384
  Max image 2D height:				 16384
  Max image 3D width:				 16384
  Max image 3D height:				 16384
  Max image 3D depth:				 8192
  Max samplers within kernel:			 5597
  Max size of kernel argument:			 1024
  Alignment (bits) of base address:		 1024
  Minimum alignment (bytes) for any datatype:	 128
  Single precision floating point capability
    Denorms:					 Yes
    Quiet NaNs:					 Yes
    Round to nearest even:			 Yes
    Round to zero:				 Yes
    Round to +ve and infinity:			 Yes
    IEEE754-2008 fused multiply-add:		 Yes
  Cache type:					 Read/Write
  Cache line size:				 64
  Cache size:					 16384
  Global memory size:				 7877427200
  Constant buffer size:				 6695813120
  Max number of constant args:			 8
  Local memory type:				 Scratchpad
  Local memory size:				 65536
  Max pipe arguments:				 16
  Max pipe active reservations:			 16
  Max pipe packet size:				 2400845824
  Max global variable size:			 6695813120
  Max global variable preferred total size:	 7877427200
  Max read/write image args:			 64
  Max on device events:				 1024
  Queue on device max size:			 8388608
  Max on device queues:				 1
  Queue on device preferred size:		 262144
  SVM capabilities:				 
    Coarse grain buffer:			 Yes
    Fine grain buffer:				 Yes
    Fine grain system:				 Yes
    Atomics:					 No
  Preferred platform atomic alignment:		 0
  Preferred global atomic alignment:		 0
  Preferred local atomic alignment:		 0
  Kernel Preferred work group size multiple:	 64
  Error correction support:			 0
  Unified memory for Host and Device:		 1
  Profiling timer resolution:			 1
  Device endianess:				 Little
  Available:					 Yes
  Compiler available:				 Yes
  Execution capabilities:				 
    Execute OpenCL kernels:			 Yes
    Execute native function:			 No
  Queue on Host properties:				 
    Out-of-Order:				 No
    Profiling :					 Yes
  Queue on Device properties:				 
    Out-of-Order:				 Yes
    Profiling :					 Yes
  Platform ID:					 0x7ff4a1f7fcf0
  Name:						 gfx902+xnack
  Vendor:					 Advanced Micro Devices, Inc.
  Device OpenCL C version:			 OpenCL C 2.0 
  Driver version:				 3212.0 (HSA1.1,LC)
  Profile:					 FULL_PROFILE
  Version:					 OpenCL 2.0 
  Extensions:					 cl_khr_fp64 cl_khr_global_int32_base_atomics cl_khr_global_int32_extended_atomics cl_khr_local_int32_base_atomics cl_khr_local_int32_extended_atomics cl_khr_int64_base_atomics cl_khr_int64_extended_atomics cl_khr_3d_image_writes cl_khr_byte_addressable_store cl_khr_fp16 cl_khr_gl_sharing cl_amd_device_attribute_query cl_amd_media_ops cl_amd_media_ops2 cl_khr_image2d_from_buffer cl_khr_subgroups cl_khr_depth_images cl_amd_copy_buffer_p2p cl_amd_assembly_program 
```

### Step 4: Install MIVisionX pre-requites using `MIVisionX-setup.py`

#### Clone MIVisionX repository from GitHub

```
git clone https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX.git
```

#### Use Setup script to install dependencies 

```
python MIVisionX/MIVisionX-setup.py --rali no
```

### Step 5: Build and Install MIVisionX

#### Build MIVisionX
```
mkdir build && cd build
cmake ../MIVisionX
make
```

#### Install MIVisionX
```
sudo make install
```

### Step 6: Verify Inference Workflow 

#### MNIST Digits Classification

<p align="center">
 <img src="https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/raw/master/docs/images/DGtest.gif">
</p>

##### Build Sample Classification Application
```
cd MIVisionX/apps/dg_test
mkdir build && cd build
cmake ../
make
```

##### Run Application
```
./DGTest ../data/weights.bin
```

<p align="center">
 <img src="https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/raw/master/docs/images/dg_test_sample.png">
</p>

#### MIVisionX Model Compiler Samples

In this sample, we will learn how to run inference efficiently using [OpenVX](https://www.khronos.org/openvx/) and [OpenVX Extensions](https://www.khronos.org/registry/OpenVX/extensions/vx_khr_nn/1.2/html/index.html). The sample will go over each step required to convert a pre-trained neural net model into an OpenVX Graph and run this graph efficiently on any target hardware. In this sample, we will also learn about AMD MIVisionX which delivers an open-source implementation of OpenVX and OpenVX Extensions along with MIVisionX Neural Net Model Compiler & Optimizer.

* Sample-1: [Classification Using Pre-Trained ONNX Model](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/blob/master/samples/model_compiler_samples/README.md#sample-1---classification-using-pre-trained-onnx-model)
* Sample-2: [Detection Using Pre-Trained Caffe Model](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/blob/master/samples/model_compiler_samples/README.md#sample-2---detection-using-pre-trained-caffe-model)
* Sample-3: [Classification Using Pre-Trained NNEF Model](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/blob/master/samples/model_compiler_samples/README.md#sample-3---classification-using-pre-trained-nnef-model)
* Sample-4: [Classification Using Pre-Trained Caffe Model](https://github.com/GPUOpen-ProfessionalCompute-Libraries/MIVisionX/blob/master/samples/model_compiler_samples/README.md#sample-4---classification-using-pre-trained-caffe-model)


