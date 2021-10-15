#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Kyle Murray
Fri Jan 11 12:26:33 2019
Description:
    
    doVH.py

"""
import os
import glob
import re


##for now, set reference date since I'm lazy about searching config_reference
reference='20180502';
print('We have set reference date to ' + reference + ', change for your example\n')

#note: this is a quick script so it's not checking file existence, etc.

#move merged slcfiles to new directory
os.system('mv merged/SLC merged/SLC_VV')

#make config_reference_vh
os.system('cp configs/config_reference configs/config_reference_vh')
#replace vv with vh
os.system('sed -i "s/pol : vv/pol : vh/" configs/config_reference_vh')
#cut off everything after "topo"
os.system('sed -i -n "/topo/q;p" configs/config_reference_vh')

#replace vv with vh in all pawns while renaming them at same time
#note that we've made vh version of single pol scenes, which is silly
os.system('sed -i_vh "s/pol : vv/pol :  vh/" configs/config_secondary*')
os.system('sed -i "s/pol : vh/pol : vv/" configs/config_secondary*')
os.system('sed -i "s/pol : vv/pol : vh/" configs/config_secondary*vh')

#make copies of resamp dir (don't have to redo range/azimuth)
os.system('sed -i_vh '' configs/config_fullBurst_resample_2*');

#make new run_files directory 
os.mkdir('run_files_vh')

#only mv required files to new run_files directory
os.system('cp run_files/*unpack* run_files_vh')
os.system('cp run_files/*fullBurst_resample* run_files_vh')
os.system('cp run_files/*merge* run_files_vh')


#replace with vh where necessary (add to end of each line)
os.system('sed -i "s/\$/_vh/" run_files_vh/run*unpack*')

os.system('sed -i "s/\$/_vh/" run_files_vh/run*fullBurst_resample*')
#remove lat/lon/los/hgt/Mask from merge command
os.system('sed -i -nr "/merge_[0-9]{8}/p" run_files_vh/run*merge*')


#now sort and then remove VV-only files.
flist = glob.glob('configs/config_secondary*vh')
singles = list() #predefine a list
for f in flist:
    file = open(f, "r")
    for line in file:
        if re.search('SSV',line):
            singles.append(re.findall('\d{8}',f)[0])

#also add reference if it's single pol
file = open('configs/config_reference_vh','r')
for line in file:
        if re.search('SSV',line):
            singles.append(reference)

for single in singles:
    print(single)
    os.system('sed -i -n "/' + single + '/!p" run_files_vh/run*')

print("now just run commands in run_files_vh\n")
