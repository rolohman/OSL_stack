#!/usr/bin/env python3

   
import os
import glob
import re
from osgeo import gdal

bb=[2000, 4000, 28000, 3000]

workDir='/home/jovyan/Oman'
oldDirs = ['SLC_VV','SLC_VH','geom_reference']

for searchDir in oldDirs:
    testdir = os.path.join(workDir,'merged',searchDir)
    if re.search(r'SLC',searchDir):
        for dateDir in os.listdir(testdir):
            if re.search(r'\d{8}', dateDir):
                oldDir=os.path.join(testdir,dateDir);
                newDir=os.path.join(workDir,'cropped',searchDir,dateDir);
                try:
                    os.makedirs(newDir)
                except OSError as error:
                    print(newDir,' already created')
 
                for file in os.listdir(oldDir):
                    if file.endswith("slc.full"):
                        newfile=os.path.join(newDir,file)
                        ds = gdal.Open(os.path.join(oldDir,file))
                        ds = gdal.Translate(newfile, ds, srcWin = bb,format='ISCE')
                        ds = None
                    
    else:
        oldDir=testdir
        newDir=os.path.join(workDir,'cropped',searchDir);
        try:
            os.makedirs(newDir)
        except OSError as error:
            print(newDir,' already created')
 
        for file in os.listdir(oldDir):
            if file.endswith("rdr") and re.match(r'\w{3}\.',file):
                newfile=os.path.join(newDir,file)
                ds = gdal.Open(os.path.join(oldDir,file))
                ds = gdal.Translate(newfile, ds, srcWin = bb,format='ISCE')
                ds = None
