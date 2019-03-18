# AMD - NSF I/UCRC Consortium - Work Order

## NSF I/UCRC Consortium for Embedded Systems at Southern Illinois University Carbondale

The NSF Center for Embedded Systems (CES) is a research collaboration between academia 
(Southern Illinois University Carbondale and Arizona State University), Industry 
(leading embedded systems companies throughout the world) and government agencies 
(the National Science Foundation and other agencies). Its purpose is to advance in the 
field of embedded systems (hardware, software, and architectures) to new levels; thereby, 
sharing resulting advancements and commercializing applications in automotive, aerospace 
and micro-electronics to advance commerce.

#### Contact
Spyros Tragoudas, Professor & Department Chair, Electrical & Computer Engineering Department, SIUC

## AMD project summary

## Cascading models with fused single kernel model as lightweight model for each application

**Duration:** 1 year

Considering multiple applications. Each application relies on multiple neural network
models. A small lightweight model per application feeds a larger complex model that may be
shared for multiple applications in order to accommodate limited resources. The simple model
triggers the larger model when it fails or when the desired output is more complex than its
specification.

The assumption is that the common complex model will be triggered sparingly for each
application. A scheduler will handle collisions among different applications at the expense of
small increase in latency.

The smaller decision network is to be created as fused single kernel network that handles all the
optimizations within the kernel using existing OpenVX and OpenCL along with AMD libraries for
neural networks.

Train or use pre-trained models to develop an application which runs a lightweight model, 
which is optimized to use less power and resources, to detect some object or scene to trigger
running of a more complex model, which does detection of a scene or segmentation, to complete a given task.

## Proposed Phases

### Quarter 1

Create a fused single kernel model for the first application (image/vision)
supported by OpenVX in MIVisionX. It will be optimized for AMD tools and libraries.
It will be designed to delegate certain tasks to a more complex model.

### Quarter 2

Development of a light weight model as in 1, for a second application. Start
the development of the common larger model for the two applications.

### Quarter 3

Profile the cascaded common model using AMD hardware, and make
necessary adjustments for maximum saving in resources.

### Quarter 4

Thorough experimental evaluation of proposed models. A study on
applications other than vision/image that utilize a simple lightweight model that feeds a
common complex model that also handles the applications in 1 and 2.

## Budget:
$50K for a year.

**This will be an annual membership of AMD to the NSF IUCRC for Embedded Systems (CES). Matched by the NSF.**
