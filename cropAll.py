#!/usr/bin/env python3

import os
import glob
import re
from osgeo import gdal
import numpy as np
import stackConfigs as sC


#bb   = [500*20, 600*4, 900*20, 400*4] #Olivia Edited 12/10/21
workDir='/home/jovyan/'+sC.workdir

oldDirs = ['SLC_vv','SLC_vh','geom_reference']

#loop over polygons
for i in np.arange(sC.croppoly.shape[0]):
    #the bounding box for this poly: upper left corner, width, length
    bb = sC.croppoly[i,:]
    #name of new directory including crop info
    cropname = os.path.join(workDir,'cropped_'+str(bb[0])+'_'+str(bb[1])+'_'+str(bb[2])+'_'+str(bb[3]))
    for searchDir in oldDirs:
        testdir = os.path.join(workDir,'merged',searchDir)
        if os.path.isdir(testdir):
            if re.search(r'SLC',searchDir):
                for dateDir in os.listdir(testdir):
                    if re.search(r'\d{8}', dateDir):
                        oldDir=os.path.join(testdir,dateDir);
                        newDir=os.path.join(cropname,searchDir,dateDir);
                        os.makedirs(newDir, exist_ok=True)
                
                        for file in os.listdir(oldDir):
                            if file.endswith("slc.full"):
                                print('cropping '+os.path.join(oldDir,file))
                                newfile=os.path.join(newDir,file)
                                ds = gdal.Open(os.path.join(oldDir,file))
                                ds = gdal.Translate(newfile, ds, srcWin = bb,format='ISCE')
                                ds = None
                    
            else:
                oldDir=testdir
                newDir=os.path.join(cropname,searchDir);
                os.makedirs(newDir, exist_ok=True)
           
                for file in os.listdir(oldDir,):
                    if file.endswith("rdr.full") and re.match(r'\w{3}\.',file):
                        print('cropping '+os.path.join(oldDir,file))
                        newfile=os.path.join(newDir,file)
                        ds = gdal.Open(os.path.join(oldDir,file))
                        ds = gdal.Translate(newfile, ds, srcWin = bb,format='ISCE')
                        ds = None
