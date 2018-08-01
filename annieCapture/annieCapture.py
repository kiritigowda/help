import sys,os,time,csv,getopt,cv2,argparse
import numpy, ctypes, array
import numpy as np
from datetime import datetime
from ctypes import cdll, c_char_p
from skimage.transform import resize
from numpy.ctypeslib import ndpointer
import ntpath
import scipy.misc
from PIL import Image


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

def PreprocessImage(img, dim):
    imgw = img.shape[1]
    imgh = img.shape[0]
    imgb = np.empty((dim[0], dim[1], 3))    #for inception v4
    imgb.fill(1.0)
    if imgh*dim[0] > imgw*dim[1]:
        neww = int(imgw * dim[1] / imgh)
        newh = dim[1]
    else:
        newh = int(imgh * dim[0] / imgw)
        neww = dim[0]
    offx = int((dim[0] - neww)/2)
    offy = int((dim[1] - newh)/2)
    imgc = img.copy()*(2.0/255.0) - 1.0

    #print('INFO:: imw: %d imh: %d dim0: %d dim1:%d newW:%d newH:%d offx:%d offy: %d' % (imgw, imgh, dim[0], dim[1], neww, newh, offx, offy))
    imgb[offy:offy+newh,offx:offx+neww,:] = resize(imgc,(newh,neww),1.0)
    #im = imgb[:,:,(2,1,0)]
    return imgb

def runInference(img, api, hdl):
    imgw = img.shape[1]
    imgh = img.shape[0]
    out_buf = bytearray(1000*4)
    out = np.frombuffer(out_buf, dtype=numpy.float32)
    #convert image to tensor format (RGB in seperate planes)
    img_r = img[:,:,0]
    img_g = img[:,:,1]
    img_b = img[:,:,2]
    img_t = np.concatenate((img_r, img_g, img_b), 0)

    status = api.annCopyToInferenceInput(hdl, np.ascontiguousarray(img_t, dtype=np.float32), (img.shape[0]*img.shape[1]*3*4), 0)
    #print('INFO: annCopyToInferenceInput status %d'  %(status))
    status = api.annRunInference(hdl, 1)
    #print('INFO: annRunInference status %d ' %(status))
    status = api.annCopyFromInferenceOutput(hdl, np.ascontiguousarray(out, dtype=np.float32), len(out_buf))
    #print('INFO: annCopyFromInferenceOutput status %d' %(status))
    return out

def predict_fn(images):
    results = np.zeros(shape=(len(images), 1000))
    for i in range(len(images)):
        results[i] = runInference(images[i])    
    return results

def getKey(item):
    return item[1]  


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', dest='image', type=str,
                        default='./images/dog.jpg', help='An image path.')
    parser.add_argument('--capture', dest='capmode', type=int,
                        default=0, help='Display Mode.')
    parser.add_argument('--annpythonlib', dest='pyhtonlib', type=str,
                        default='./libannpython.so', help='pythonlib')
    parser.add_argument('--weights', dest='weightsfile', type=str,
                        default='./weights.bin', help='A directory with images.')
    parser.add_argument('--labels', dest='labelfile', type=str,
                        default='./labels.txt', help='file with labels')
    parser.add_argument('--hierarchy', dest='hierarchyfile', type=str,
                        default='./hier-may14.csv', help='file with labels')
    args = parser.parse_args()

    imagefile = args.image
    synsetfile = args.labelfile
    weightsfile = args.weightsfile
    annpythonlib = args.pyhtonlib
    hierarchyfile = args.hierarchyfile
    Mode = args.capmode;
    api = AnnAPI(annpythonlib)
    input_info,output_info = api.annQueryInference().decode("utf-8").split(';')
    input,name,ni,ci,hi,wi = input_info.split(',')
    hdl = api.annCreateInference(weightsfile)
    inp_dim = (299, 299)
    #read synset names
    if synsetfile:
        fp = open(synsetfile, 'r')
        names = fp.readlines()
        names = [x.strip() for x in names]
        fp.close()

    #read hierarchy names
    if hierarchyfile:
        fp = open(hierarchyfile, 'r')
        hierarchies = fp.readlines()
        hierarchies = [x.strip() for x in hierarchies]
        fp.close()

    if sys.argv[1] == '--image':
        # image preprocess
        top_indeces = []
        top_labels = []
        img = cv2.imread(imagefile)
        imgb = PreprocessImage(img, inp_dim)
        start = datetime.now()
        output = runInference(imgb, api, hdl)
        for x in output.argsort()[-3:]:
            print (x, names[x], output[x])
            top_indeces.append(x)
            top_labels.append(names[x])

        txt =  top_labels[2]   
        size = cv2.getTextSize(top_labels[2], cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.1, 2)
        t_width = size[0][0]
        t_height = size[0][1]
        cv2.rectangle(img, (50, 50), (t_width+50,t_height+50), (192,192,128), -1)
        cv2.putText(img,txt,(52,52),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.1,(20,20,20),2)
        cv2.imshow('Demo', img)
        key = cv2.waitKey()
        #cv2.destroyAllWindows()
        #AnnInferenceLib.annReleaseContext(ctypes.c_void_p(hdl))
        api.annReleaseInference(hdl)
        exit()

    elif sys.argv[1] == '--capture':
        cap = cv2.VideoCapture(0)
        assert cap.isOpened(), 'Cannot capture source'    
        frames = 0
        start = time.time()
        while cap.isOpened():        
            top_indeces = []
            top_labels = []
            top_prob = []
            top_hei = []
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)                
                imgb = PreprocessImage(frame, inp_dim)
                #output = runInference(imgb)
                output = runInference(imgb, api, hdl)
                for x in output.argsort()[-3:]:
                    top_indeces.append(x)
                    top_labels.append(names[x])
                    top_prob.append(output[x])
                    top_hei.append(hierarchies[x])
                    #print (x, names[x], output[x])
                #print (top_labels[2], top_indeces[2])
                if Mode == 0:
                    #draw a rectangle on the image at top    
                    txt =  top_labels[2].lstrip(top_labels[2].split(' ')[0])   
                    size = cv2.getTextSize(top_labels[2], cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)
                    t_width = size[0][0]
                    t_height = size[0][1]
                    cv2.rectangle(frame, (10, 10), (t_width+2,t_height+16), (192,192,128), -1)
                    cv2.putText(frame,txt,(10,t_height+10),cv2.FONT_HERSHEY_DUPLEX,0.7,(20,20,20),2)
                    cv2.imshow('AMD InceptionV4 Live', frame)
                elif Mode == 1:
                    txt =  top_labels[2].lstrip(top_labels[2].split(' ')[0])   
                    txt1 =  top_hei[2].replace(',', ' ')
                    size = cv2.getTextSize(top_hei[2], cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)
                    t_width = size[0][0]
                    t_height = size[0][1]
                    t_height1 = size[0][1]*2
                    cv2.rectangle(frame, (10, 10), (t_width+10,t_height1+16), (192,192,128), -1)
                    cv2.putText(frame,txt,(10,t_height+10),cv2.FONT_HERSHEY_DUPLEX,0.7,(20,20,20),2)
                    cv2.putText(frame,txt1,(10,t_height1+10),cv2.FONT_HERSHEY_DUPLEX,0.7,(20,20,20),2)
                    cv2.imshow('AMD InceptionV4 Live', frame)
                    
                key = cv2.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                frames += 1
                print("FPS of the video is {:5.2f}".format( frames / (time.time() - start)))
            else:
                break

        api.annReleaseInference(hdl)
        exit()

