#!/usr/bin/env python3

import os,sys
import glob
import pandas
from osgeo import gdal
import datetime 
from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

targetNumDates = 5 #may be able to increase this if you are using less than a full frame (<9-10 bursts, <3 swaths)
workdir  ='/home/jovyan/CV' #make sure this exists
dem      = '/home/jovyan/CV/dem/demLat_N34_N37_Lon_W118_W121.dem.wgs84' #make sure this exists too!

polygon = "&intersectsWith=POLYGON((-120.22 35.74,-119.25 35.74,-119.25 36.24,-120.22 36.24,-120.22 35.74))"
track   = "&relativeOrbit=144" #also referred to as "relative orbit"
date1   = '&start=2019-08-14'  #start of search date period
date2   = '&end=2021-09-30'    #end of search date period
refdate = '20190814'
pltdate = '20190820_20190826' #pair that you will plot in a later step

narrowpoly = ' -b \'35.74 36.24 -120.22 -119.25\' ' #this is the area you want to extract, but may need be adjusted after your first iter of stackSentinel_VH
swaths     = ' -n \'1 2 3\''    #list of swaths if you know you only need one or two, otherwise all.
looks      = ' -r 20 -z 4 ' #final looks of your large-area interferograms
croppoly   = [5000, 2000, 30000, 3500] #UL corner, width and length

df = pandas.read_csv(workdir+'/list.csv')
df['Acquisition Date'] = pandas.to_datetime(df['Acquisition Date'])
df['date'] = pandas.to_datetime(df['Acquisition Date'])    
numfiles = np.shape(df)[0]

uniqueDates=df['date'].dt.date.unique()
uniqueDates.sort()
totNumDates=np.size(uniqueDates)
print(str(totNumDates)+ ' unique dates and ' + str(numfiles) +' total files')

coregSLCDir = os.path.join(workdir, 'coreg_secondarys/vv') #look in vv since that should be complete
if os.path.exists(coregSLCDir):
    coregSecondarys = glob.glob(os.path.join(coregSLCDir, '[0-9]???[0-9]?[0-9]?'))
    coregSLC = [os.path.basename(slv) for slv in coregSecondarys]
    coregSLC.sort()

    if len(coregSLC)>0:
        print('It looks like the following dates have already been done')
        print(coregSLC)
        index=len(coregSLC)
        print('Starting on date: '+str(uniqueDates[index]))
        remNumDates = totNumDates-len(coregSLC)

    else:
        index=0
        remNumDates = totNumDates

else:
    index=0
    remNumDates = totNumDates

batches = int(np.ceil(remNumDates / targetNumDates))
print(str(batches)+' batches with '+str(targetNumDates)+ ' dates each')

i=0

for i in np.arange(i,batches):
    #i=i+1
    #if i == 3:
    print('Starting batch '+str(int(i)))
    for j in np.arange(targetNumDates):
        if index < totNumDates:
            for k in np.arange(numfiles):
                 if df.date[k].date() == uniqueDates[index]:
                    rawFile=df['URL'][k]
                    rawRoot=os.path.basename(rawFile)
                    if os.path.exists(os.path.join(workdir,'raw',rawRoot)):
                        print(rawRoot+' already downloaded')
                    else:
                        print('Downloading '+rawRoot)
                        wstr='wget '+ rawFile+' --directory-prefix=' + workdir + '/raw'
                        os.system(wstr+' -q  --show-progress  --progress=bar:force:noscroll')
 
            index+=1
    
    command='stackSentinel_VH.py -s '+workdir+'/raw -m '+refdate+' -o /home/jovyan/ -a '+workdir+'/aux/ -w '+workdir+' -d '+dem+narrowpoly+swaths+looks+' -c 1 -O 1 -W interferogram'
    os.system(command)
    os.system(workdir+'/runstuff  > errors 2> extraerrors')
    os.system(workdir+'/runstuff2 > errors2 2> extraerrors2')
    os.rename(workdir+'/run_files',workdir+'/run_files'+str(i))
    os.rename(workdir+'/runstuff',workdir+'/run_files'+str(i)+'/runstuff')
    os.rename(workdir+'/runstuff2',workdir+'/run_files'+str(i)+'/runstuff2')
