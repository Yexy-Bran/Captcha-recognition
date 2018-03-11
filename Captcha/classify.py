#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time
from skimage import io,transform
import skimage
from PIL import Image,ImageDraw,ImageFont,ImageFilter

import caffe

def erode(img, size):
    row = img.shape[0]
    col = img.shape[1]
    n = (size-1)/2
    res = img[:]
    for i in range(n, row-n):
        for j in range(n, col-n):
            b = 0
            c = 0
            for x in range(-n, n+1):
                for y in range(-n, n+1):
                    if img[i+x][j+y] == 255:
                        c+=1
                        if c > pow(size, 2) - size:
                            b = 1
                            break
                if b==1:
                    break
            if b==1:
                res[i][j] = 255
    return res

def extract_character(img):
    res = []
    row = img.shape[0]
    col = img.shape[1]
    for i in range(0, row):
        for j in range(0, col):
            if img[i][j][0] + img[i][j][1] + img[i][j][2] >= 15:
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
    img=Image.fromarray(img)
    img=np.array(img.convert('L'))
    img[img>30]=255
    img[img<=30]=0
    erode(img, 3)
    co = 23
    ro = 14
    for k in range(0, 6):
        r = 12
        c = 12
        temp = np.zeros([r,c])
        for i in range(0, r):
            for j in range(0, c):
                temp[i][j] = img[i+ro][j+co]
        co+=18
        res.append(temp)
    return res

def process_image(imgfile):
    img = Image.open(imgfile)
    r, g, b, a = img.split()
    img = Image.merge("RGB", (r, g, b))
    img = np.array(img)
    res = extract_character(img)
    for k in range(0, 6):
        tmp = Image.fromarray(res[k])
        tmp = tmp.convert('L')
        #import pdb;pdb.set_trace()
        ind = imgfile.rfind('.')
        path = os.getcwd()+'/'+imgfile[:ind]+str(k+1)+'.png'
        if not os.path.exists(path):
            tmp.save(path)
    return res

def output(input_file,input_scale=0.00390625,):
    pycaffe_dir = os.path.dirname(__file__)
    #import pdb;pdb.set_trace()
    model_def=os.path.join(pycaffe_dir,
                "deploy.prototxt")
    pretrained_model=os.path.join(pycaffe_dir,
                "lenet_iter_20000.caffemodel")
    gpu='store_true'

    images_dim='12,12'

    mean_file=os.path.join(pycaffe_dir,
                             'caffe/imagenet/ilsvrc_2012_mean.npy')
    raw_scale=1

    channel_swap='0'
    ext='png'
    image_dims = [int(s) for s in images_dim.split(',')]

    mean, channel_swap = None, None
    #if args.mean_file:
        #mean = np.load(args.mean_file)
    caffe.set_mode_gpu()
    print("GPU mode")

    # Make classifier.
    classifier = caffe.Classifier(model_def, pretrained_model,
            image_dims=image_dims, mean=mean,
            input_scale=input_scale, raw_scale=raw_scale,
            channel_swap=channel_swap)

    # Load numpy array (.npy), directory glob (*.jpg), or image file.
    input_file = os.path.expanduser(input_file)
    if input_file.endswith('npy'):
        print("Loading file: %s" % input_file)
        inputs = np.load(input_file)
    elif os.path.isdir(input_file):
        print("Loading folder: %s" % input_file)
        inputs =[caffe.io.load_image(im_f)
                 for im_f in glob.glob(input_file + '/*.' + ext)]
    else:
        print("Loading file: %s" % input_file)
        inputs = [caffe.io.load_image(input_file)]

    print("Classifying %d inputs." % len(inputs))
    #import pdb;pdb.set_trace()
    img = skimage.io.imread(input_file)*1.0
    tmp = []
    if len(img.shape) == 2:
        img = img.reshape(img.shape[0], img.shape[1], 1)
    tmp.append(img)
    inputs = tmp

    # Classify.
    start = time.time()
    predictions = classifier.predict(inputs, gpu)
    print("Done in %.2f s." % (time.time() - start))
    res=[[0] * 2 for row in range(36)]
    maxnum = 0
    maxind = ''
    smaxnum = 0
    smaxind = ''
    for i in range(predictions.shape[1]):
        res[i][0] = i if i < 10 else chr(int(ord('A'))+i-10)
        res[i][1] = predictions[0][i]
        if predictions[0][i]>maxnum:
            maxnum = predictions[0][i]
            maxind = str(i) if i < 10 else chr(int(ord('A'))+i-10)
    for i in range(predictions.shape[1]):
        if predictions[0][i]>smaxnum and predictions[0][i]<maxnum:
            smaxnum = predictions[0][i]
            smaxind = str(i) if i < 10 else chr(int(ord('A'))+i-10)
    #import pdb;pdb.set_trace()

    return maxind,maxnum,smaxind,smaxnum

if __name__ == '__main__':
    
    for k in range(1,6):
        process_image('test/'+str(k)+'.png')
        ans = []
        for i in range(1,7):
            maxind,maxnum,smaxind,smaxnum = output('./test/'+str(k)+str(i)+'.png')
            tmp = [maxind,maxnum,smaxind,smaxnum]
            ans.append((str(maxind)+':'+str(maxnum)+'; '+str(smaxind)+':'+str(smaxnum)))
        output_file = './test/'+str(k)+'.txt'
        f=open(output_file,'w')
        for j in range(len(ans)):
        	f.write(ans[j]+'\n')
        f.close()
        #import pdb;pdb.set_trace()
