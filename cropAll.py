#!/usr/bin/env python3

   
import os
import glob
import re
from osgeo import gdal

bb   = [5000, 2000, 30000, 3500] #Rowena Edit

workDir='/home/jovyan/CV'
oldDirs = ['SLC_vv','SLC_vh','geom_reference']

for searchDir in oldDirs:
    testdir = os.path.join(workDir,'merged',searchDir)
    if os.path.isdir(testdir):
        if re.search(r'SLC',searchDir):
            for dateDir in os.listdir(testdir):
                if re.search(r'\d{8}', dateDir):
                    oldDir=os.path.join(testdir,dateDir);
                    newDir=os.path.join(workDir,'cropped',searchDir,dateDir);
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
            newDir=os.path.join(workDir,'cropped',searchDir);
            os.makedirs(newDir, exist_ok=True)
           
            for file in os.listdir(oldDir,):
                if file.endswith("rdr.full") and re.match(r'\w{3}\.',file):
                    print('cropping '+os.path.join(oldDir,file))
                    newfile=os.path.join(newDir,file)
                    ds = gdal.Open(os.path.join(oldDir,file))
                    ds = gdal.Translate(newfile, ds, srcWin = bb,format='ISCE')
                    ds = None
