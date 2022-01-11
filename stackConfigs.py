#!/usr/bin/env python3

import numpy as np

targetNumDates = 5 #may be able to increase this if you are using less than a full frame (<9-10 bursts, <3 swaths)
workdir  ='LagunaSalada' #make sure this exists
dem      = '/home/jovyan/LagunaSalada/DEM/demLat_N31_N33_Lon_W117_W115.dem.wgs84' #make sure this exists too!

polygon = "&intersectsWith=POLYGON((-116.0339 31.7594,-115.1386 31.7594,-115.1386 32.7782,-116.0339 32.7782,-116.0339 31.7594))"
track   = "&relativeOrbit=173" #also referred to as "relative orbit"



# now adding more dates to start on making a FULL stack 
date1   = '&start=2017-05-10'  #start of search date period
date2   = '&end=2022-01-10'    #end of search date period
refdate = '20170510'
pltdate = '20170510_20170522' #pair that you will plot in a later step   

rlooks     = 20 #range looks
alooks     = 4  #azimuth looks
looks      = ' -r '+str(rlooks)+' -z '+str(alooks)+' ' #final looks of your large-area interferograms
swaths     = ' -n \'1 2 3\''    #list of swaths if you know you only need one or two, otherwise all.

#this is the area you want to use to select bursts but may need be adjusted after your first iter of stackSentinel_VH
narrowpoly = ' -b \'32.29 32.75 -116.0 -115.15\' ' 

# croppoly: min_range, min_azimuth, range_diff/width, azimuth_diff/width 
croppoly   = np.array([[450*20, 450*4, 900*20, 900*4],[450*20, 5*4, 500*20, 445*4]]) 
