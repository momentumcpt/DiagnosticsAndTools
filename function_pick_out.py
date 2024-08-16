#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:24:40 2017

@author: zhunguo, guozhun@uwm.edu, guozhun@lasg.iap.ac.cn 
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import os
from subprocess import call

def closest_idx(lst, K):

    return min(range(len(lst)), key = lambda i: abs(lst[i]-K))

def pick_out(ncases, cases,years, nsite,lats, lons,area, filepath,casedir,fv,datapath):
# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# fv, calculate indices for fv dycore
 print(ncases)
# inptrs = [ncases]

 if not os.path.exists(datapath):
        os.mkdir(datapath)


 for im in range(0,ncases):
    
     infile=filepath[im]+cases[im]+'.cam.h0a.'+str(years[im]).rjust(4,'0')+'-01.nc'

     print(infile)
     print(im)
     inptrs = Dataset(infile,'r')       # pointer to file1
     lat=inptrs.variables['lat'][:]
     nlat=len(lat)
     lon=inptrs.variables['lon'][:] 
     nlon=len(lon)
#     idx_cols=[[0 for i in range(5)] for j in range(nsite)] 
     nh=[0 for k in range(nsite)]
#     print(idx_cols)
     cols=[0,1,2,3,4]
     sits=np.linspace(0,nsite-1,nsite)

     txtfile1=filepath[im]+cases[im]+'/run/diff*.asc'
     txtfile2=filepath[im]+cases[im]+'/run/log*.asc'
     os.system('mkdir '+ casedir+'/txt/')
     os.system('cp -f '+ txtfile1+ ' '+ casedir+'/txt/')
     os.system('cp -f '+ txtfile2+ ' '+ casedir+'/txt/')


     os.system('rm -f '+datapath+cases[im]+'_site_location.nc')
     outf =Dataset(datapath+cases[im]+'_site_location.nc','w')
     outf.createDimension("sit",nsite)
     outf.createDimension("col",5)
     outf.createDimension("coord",1)
#     outf.variables['sit'][:]=sits
#     outf.variables['col'][:]=cols
     outf.createVariable('idx_cols','i',('sit','col'))
     outf.createVariable('n','i',('sit'))
     outf.createVariable('idx_coord_lat','i',('sit','coord'))
     outf.createVariable('idx_coord_lon','i',('sit','coord'))
     outf.variables['n'][:]=0
     outf.variables['idx_cols'][:,:]=0
     outf.variables['idx_coord_lat'][:,:]=0
     outf.variables['idx_coord_lon'][:,:]=0

# ========================================================================== 
# find out the cols and their numbers
#    the axis of site is stored in idx_cols(site,n)

     if(fv):
       for s in range(0,nsite):
         A = lons[s]
         B = lats[s]
         outf.variables['idx_coord_lon'][s,0] = closest_idx(lon,A)
         outf.variables['idx_coord_lat'][s,0] = closest_idx(lat,B)
         outf.variables['n'][s] = nh[s]+1
     else:
       for i in range(0,nlat):
         for j in range(0,nsite): 
             if (lon[i] >= lons[j]-area) & (lon[i] < lons[j]+area) & (lat[i]>=lats[j]-area) & (lat[i] < lats[j]+area): 
                 outf.variables['idx_cols'][j,nh[j]]=i 
                 outf.variables['n'][j]=nh[j]+1

     outf.close()
