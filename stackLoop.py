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
import stackConfigs as sC


df = pandas.read_csv(sC.workdir+'/list.csv')
df['Acquisition Date'] = pandas.to_datetime(df['Acquisition Date'])
df['date'] = pandas.to_datetime(df['Acquisition Date'])    
numfiles = np.shape(df)[0]
print(numfiles)
uniqueDates=df['date'].dt.date.unique()
uniqueDates.sort()

totNumDates=np.size(uniqueDates)
uniqueDateStr=[]
for i in np.arange(totNumDates):
    uniqueDateStr.append(uniqueDates[i].strftime('%Y%m%d'))

print(str(totNumDates)+ ' unique dates and ' + str(numfiles) +' total files')

coregSLCDir = os.path.join(sC.workdir, 'coreg_secondarys/vv') #look in vv since that should be complete
if os.path.exists(coregSLCDir):
    coregSecondarys = glob.glob(os.path.join(coregSLCDir, '[0-9]???[0-9]?[0-9]?'))
    coregSLC = [os.path.basename(slv) for slv in coregSecondarys]
    coregSLC.sort()

    if len(coregSLC)>0:
        print('It looks like the following dates have already been done')
        print(coregSLC)
        remNumDates = totNumDates-len(coregSLC)

    else:
        remNumDates = totNumDates

else:
    remNumDates = totNumDates


newDates = np.setdiff1d(uniqueDateStr,coregSLC)

print(str(remNumDates)+' dates still to process, length of newDates='+str(newDates.size))
print(newDates)
batches = int(np.ceil(remNumDates / sC.targetNumDates))
print(str(batches)+' batches based on '+str(sC.targetNumDates)+ ' dates/batch')

i=0
index=0

for i in np.arange(i,batches):
    print('Starting batch '+str(int(i)))
    for j in np.arange(sC.targetNumDates):
        if index < remNumDates:
            for k in np.arange(numfiles):
                if df.date[k].strftime('%Y%m%d') == newDates[index]:
                    rawFile=df['URL'][k]
                    rawRoot=os.path.basename(rawFile)
                    if os.path.exists(os.path.join(sC.workdir,'raw',rawRoot)):
                        print(rawRoot+' already downloaded')
                    else:
                        print('Downloading '+rawRoot)
                        wstr='wget '+ rawFile+' --directory-prefix=' + sC.workdir + '/raw'
                        os.system(wstr+' -q  --show-progress  --progress=bar:force:noscroll')
 
            index+=1

    command='stackSentinel_VH.py -s '+sC.workdir+'/raw -m '+sC.refdate+' -o /home/jovyan/ -a '+sC.workdir+'/aux/ -w '+sC.workdir+' -d '+sC.dem+sC.narrowpoly+sC.swaths+sC.looks+' -c 1 -O 1 -W interferogram'
    os.system(command)
    os.system(sC.workdir+'/runstuff  > errors 2> extraerrors')
    os.system(sC.workdir+'/runstuff2 > errors2 2> extraerrors2')
    os.rename(sC.workdir+'/run_files',sC.workdir+'/run_files'+str(i))
    os.rename(sC.workdir+'/runstuff',sC.workdir+'/run_files'+str(i)+'/runstuff')
    os.rename(sC.workdir+'/runstuff2',sC.workdir+'/run_files'+str(i)+'/runstuff2')
