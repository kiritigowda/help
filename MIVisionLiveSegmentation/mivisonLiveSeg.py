from __future__ import division

import argparse
import array
import csv
import ctypes
import cv2
import io
import math
import numpy
import numpy as np
import os
import os.path
import scipy
import sys
import time

from skimage.transform import resize
from ctypes import cdll, c_char_p
from numpy.ctypeslib import ndpointer

overlayColors = [
					(  0,  0,  0),
					(128, 64,128), 		# road
					(244, 35,232), 		# sidewalk
					( 250, 150, 70), 	# building
					(102,102,156), 		# wall
					(190,153,153), 		# fence
					(153,153,153), 		# pole
					(250,170, 30), 		# traffic light
					(220,220,  0), 		# traffic sign
					(107,142, 35), 		# vegetation
					(152,251,152), 		# terrain
					( 70,130,180), 		# sky
					(220, 20, 60), 		# person
					(255,  0,  0), 		# rider
					(  0,  0,255), 		# car
					(  0,  0, 70), 		# truck
					(  0, 60,100), 		# bus
					(  0, 80,100), 		# train
					(  0,  0,230), 		# motorcycle
					(119, 11, 32)  		# bicycle
				]

def getMaskedImage(output_dims, output_layer, threshold):
    numClasses = output_dims[1];
    height = output_dims[2];
    width = output_dims[3];

    # Initialize buffers
    prob = np.zeros((width * height), dtype=np.float32)
    classImg = np.zeros((width * height), dtype=np.uint8)

    rangeValue = 0
    for c in range(0,numClasses):
    	for i in range(0,width * height):
            if((output_layer[rangeValue+i] >= threshold) and (output_layer[rangeValue+i] > prob[i])):
            	prob[i] = output_layer[rangeValue+i];
            	classImg[i] = c + 1;
        rangeValue += (width * height);

    # Mask Image
    imgMask = np.zeros((height, width, 3), dtype=np.uint8)
    img_r,img_g,img_b = cv2.split(imgMask)

    for i in range(0, height):
    	for j in range(0,width):
    		posID = (i * width) + j
    		R, G, B = overlayColors[classImg[posID]]
    		img_r[i,j] = R
    		img_g[i,j] = G
    		img_b[i,j] = B

    img_bgr = cv2.merge([img_b,img_g,img_r])
    return img_bgr

class AnnAPI:
	def __init__(self,library):
		self.lib = ctypes.cdll.LoadLibrary(library)
		self.annQueryInference = self.lib.annQueryInference
		self.annQueryInference.restype = ctypes.c_char_p
		self.annQueryInference.argtypes = []
		self.annCreateInference = self.lib.annCreateInference
		self.annCreateInference.restype = ctypes.c_void_p
		self.annCreateInference.argtypes = [ctypes.c_char_p]
		self.annReleaseInference = self.lib.annReleaseInference
		self.annReleaseInference.restype = ctypes.c_int
		self.annReleaseInference.argtypes = [ctypes.c_void_p]
		self.annCopyToInferenceInput = self.lib.annCopyToInferenceInput
		self.annCopyToInferenceInput.restype = ctypes.c_int
		self.annCopyToInferenceInput.argtypes = [ctypes.c_void_p, ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_size_t, ctypes.c_bool]
		self.annCopyFromInferenceOutput = self.lib.annCopyFromInferenceOutput
		self.annCopyFromInferenceOutput.restype = ctypes.c_int
		self.annCopyFromInferenceOutput.argtypes = [ctypes.c_void_p, ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_size_t]
		self.annRunInference = self.lib.annRunInference
		self.annRunInference.restype = ctypes.c_int
		self.annRunInference.argtypes = [ctypes.c_void_p, ctypes.c_int]
		print('OK: AnnAPI found "' + self.annQueryInference().decode("utf-8") + '" as configuration in ' + library)

class AnnieObjectWrapper():
	def __init__(self, annpythonlib, weightsfile):
		select = 1
		self.api = AnnAPI(annpythonlib)
		input_info,output_info = self.api.annQueryInference().decode("utf-8").split(';')
		input,name,ni,ci,hi,wi = input_info.split(',')
		output,opName,no,co,ho,wo = output_info.split(',')
		self.hdl = self.api.annCreateInference(weightsfile.encode('utf-8'))
		self.dim = (int(wi),int(hi))
		self.outputDim = (int(no),int(co),int(ho),int(wo))

	def __del__(self):
		self.api.annReleaseInference(self.hdl)

	def runInference(self,img, out):
		# create input.f32 file
		img_r = img[:,:,0]
		img_g = img[:,:,1]
		img_b = img[:,:,2]
		img_t = np.concatenate((img_r, img_g, img_b), 0)
		
		# copy input.f32 to inference input
		status = self.api.annCopyToInferenceInput(self.hdl, np.ascontiguousarray(img_t, dtype=np.float32), (img.shape[0]*img.shape[1]*3*4), 0)
		#print('INFO: annCopyToInferenceInput status %d'  %(status))
		# run inference
		status = self.api.annRunInference(self.hdl, 1)
		#print('INFO: annRunInference status %d ' %(status))
		# copy output.f32
		status = self.api.annCopyFromInferenceOutput(self.hdl, np.ascontiguousarray(out, dtype=np.float32), out.nbytes)
		#print('INFO: annCopyFromInferenceOutput status %d' %(status))

		return out

	def Detect(self, img):
		# create output.f32 buffer
		out_buf = bytearray(self.outputDim[0]*self.outputDim[1]*self.outputDim[2]*self.outputDim[3]*4)
		out = np.frombuffer(out_buf, dtype=numpy.float32)
		# run inference & receive output.f32
		output = self.runInference(img, out)

		return output

#channel_names: 'road, sidewalk, building, wall, fence, pole, traffic light, traffic sign, vegetation, terrain, sky, person, rider, car, truck, bus, train, motorcycle, bicycle'

class AnnAPI:
	def __init__(self,library):
		self.lib = ctypes.cdll.LoadLibrary(library)
		self.annQueryInference = self.lib.annQueryInference
		self.annQueryInference.restype = ctypes.c_char_p
		self.annQueryInference.argtypes = []
		self.annCreateInference = self.lib.annCreateInference
		self.annCreateInference.restype = ctypes.c_void_p
		self.annCreateInference.argtypes = [ctypes.c_char_p]
		self.annReleaseInference = self.lib.annReleaseInference
		self.annReleaseInference.restype = ctypes.c_int
		self.annReleaseInference.argtypes = [ctypes.c_void_p]
		self.annCopyToInferenceInput = self.lib.annCopyToInferenceInput
		self.annCopyToInferenceInput.restype = ctypes.c_int
		self.annCopyToInferenceInput.argtypes = [ctypes.c_void_p, ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_size_t, ctypes.c_bool]
		self.annCopyFromInferenceOutput = self.lib.annCopyFromInferenceOutput
		self.annCopyFromInferenceOutput.restype = ctypes.c_int
		self.annCopyFromInferenceOutput.argtypes = [ctypes.c_void_p, ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), ctypes.c_size_t]
		self.annRunInference = self.lib.annRunInference
		self.annRunInference.restype = ctypes.c_int
		self.annRunInference.argtypes = [ctypes.c_void_p, ctypes.c_int]
		print('OK: AnnAPI found "' + self.annQueryInference().decode("utf-8") + '" as configuration in ' + library)

# Import arguments
parser = argparse.ArgumentParser()
parser.add_argument('--video',       type=str, default='',        help='A video path.')
parser.add_argument('--modelLib',    type=str, required=True,     help='MIVision complied model .so for python module')
parser.add_argument('--weights',     type=str, required=True,     help='MIVision complied model weight.bin')
parser.add_argument('--imageWidth',  type=int, default=2048,      help='seg model input image width')
parser.add_argument('--imageHeight', type=int, default=1024,      help='seg model input image height')
parser.add_argument('--outputWidth', type=int, default=720,       help='display image width')
parser.add_argument('--outputHeight',type=int, default=480,       help='display image height')
parser.add_argument('--numOutClass', type=int, default=19,        help='seg model output classes')
parser.add_argument('--threshold',   type=float, default=0.001,   help='pixel threshold')
args = parser.parse_args()

annpythonlib = args.modelLib
weightsfile = args.weights
inputImageWidth = args.imageWidth
inputImageHeight = args.imageHeight
numOutputClasses = args.numOutClass
videoFile_location = args.video
outputImageWidth = args.outputWidth
outputImageHeight = args.outputHeight
pixelThreshold = args.threshold

detector = AnnieObjectWrapper(annpythonlib, weightsfile)

cv2.namedWindow("Input")
cv2.namedWindow("Segmentation")

if videoFile_location == '':
	cap = cv2.VideoCapture(0)
else:
	cap = cv2.VideoCapture(videoFile_location)

rval = True
frame_number = 0

while rval:
	# get frame from live or video
	start = time.time()
	rval, frame = cap.read()
	if rval == False:
		break
	end = time.time()
	print '%30s' % 'Grabbed camera frame in ', str((end - start)*1000), 'ms'

	# resize and process frame
	start = time.time()
	resizedFrame = cv2.resize(frame, (inputImageWidth,inputImageHeight))
	RGBframe = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2RGB)
	end = time.time()
	print '%30s' % 'Resized & Format to RGB in ', str((end - start)*1000), 'ms'

	# run inference
	start = time.time()
	out = detector.Detect(RGBframe)
	end = time.time()
	print '%30s' % 'Executed Model in ', str((end - start)*1000), 'ms'

	#dump input/output
	#cv2.imwrite('newInput-'+str(frame_number)+'.png',resizedFrame)
	#with open('newOutput-'+str(frame_number)+'.f32', 'wb') as f:
		#np.array(softmaxOutput, dtype=np.float32).tofile(f)
	#frame_number += 1

	# post process output file
	start = time.time()
	softmaxOutput = np.float32(out)
	output_dims = (1, numOutputClasses, inputImageHeight, inputImageWidth)
	RGB_outputImage = getMaskedImage(output_dims, softmaxOutput, pixelThreshold)
	end = time.time()
	print '%30s' % 'Processed results in ', str((end - start)*1000), 'ms'

	# display output
	start = time.time()
	inputDisplay = cv2.resize(resizedFrame, (outputImageWidth,outputImageHeight))
	outputDisplay = cv2.resize(RGB_outputImage, (outputImageWidth,outputImageHeight))
	end = time.time()
	print '%30s' % 'resized result for display in ', str((end - start)*1000), 'ms\n'
	cv2.imshow("Input", inputDisplay)
	cv2.imshow("Segmentation", outputDisplay)

	#Merge Outputs
	dst = cv2.addWeighted(inputDisplay, 0.7, outputDisplay, 0.3, 0)
	cv2.imshow("Merged Output", dst)
	
	key = cv2.waitKey(1)
	if key == 27: # exit on ESC
		break

cap.release()
cv2.destroyAllWindows()