'''
Time series
    Benjamin A. Stephens:stepheba@ucar.edu
    Kate Thayer-Calder : katec@ucar.edu
    modifed by Zhun Guo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''
import glob
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import Common_functions
import xarray as xr
import os
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
import cmaps

from matplotlib import font_manager as fm
from scipy.interpolate import griddata
from subprocess import call

def ts_plots(ptype,pixel, pname,cseason, varis, ncases, cases, casenames, nsite, lats, lons,years,nyear, filepath, filepathobs,casedir,affl,suffix, dofv,datapath):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 #infiles  = [[] for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

 nvaris = len(varis)
 cscale = [1, 1, 1, 1, 1., 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
 plotts=["" for x in range(nsite)]


 # NEED to concatenate the relevant files.
 # right now this just takes the years and nyears from the main python file, 
 # it doesn't deal with the extra two months
 varstring = ""
 for i in range(nvaris):
   varstring = varstring + f"{varis[i]},"

 for im in range(ncases):
   if not os.path.exists(datapath+"/temp"):
     os.mkdir(datapath+"/temp")
   histlist=[]
   for iy in range(nyear[im]):
     histlist=histlist+sorted(glob.glob(filepath[im][0] +cases[im]+filepath[im][1]+cases[im]+'.'+affl[im]+'.'+suffix[im]+'.'+str(years[im]+iy).rjust(4,'0')+"*"))
   for ifile,file in enumerate(histlist):
     os.system(f"ncea -v {varstring[0:-1]} {file} -o {datapath}/temp/{casenames[im]}_"+str(ifile).rjust(2,'0')+".nc")
   os.system(f"ncrcat {datapath}/temp/*.nc {datapath}/{casenames[im]}_timeseries.nc")
   os.system(f"rm -rf {datapath}/temp")


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     plotts[ire] = pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

     fig, axes = plt.subplots( nrows=nvaris//2, ncols=2, figsize=(15, 15 ))
     axes      = axes.flatten()

     for iv in range (0, nvaris):

         ax = axes[iv]

         for im in range (0,ncases):
             ncdfs[im]  = datapath+"/"+cases[im]+'_site_location.nc'
             infiles=f"{datapath}/{casenames[im]}_timeseries.nc" 
             inptrs = xr.open_dataset(infiles)       # pointer to file1
             lat=np.array(inptrs['lat'][:])
             nlat=len(lat)
             lon=np.array(inptrs['lon'][:])
             nlon=len(lon)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv[im]):
                 idx_lats=ncdf.variables['idx_coord_lat'][:,:]
                 idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             if (im ==0):
                 ntime = nyear[im]*12   #TODO: fix this up real nice
                 A_field = np.zeros((ncases,ntime),np.float32)

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if (dofv[im]):
                    npointlat=idx_lats[ire,0]
                    npointlon=idx_lons[ire,0]
                    tmp=np.array(inptrs[varis[iv]])[:,npointlat,npointlon] 
                 else:
                    tmp=np.array(inptrs[varis[iv]])[:,npoint]

                 theunits=str(cscale[iv])+inptrs[varis[iv]].units
                 A_field[im,:] = (A_field[im,:]+tmp[:]/n[ire]).astype(np.float32 )

             A_field[im,:] = A_field[im,:] *cscale[iv]
             ax.plot(np.arange(ntime),A_field[im, :], label=cases[im])
             inptrs.close()

         ax.set_xlabel('Time')
         ax.grid(True)
         ax.set_ylabel(varis[iv]+" ("+theunits+ ")")
         ax.legend()
         ax.invert_yaxis()

     title_text = pname+f" Time Series at at {lons[ire]}E, {lats[ire]}N"
     fig.suptitle(title_text,fontsize=16, ha='center', va='center')
     plt.tight_layout(rect=[0, 0, 1, 0.96])
     plt.savefig(plotname+'.'+ptype, dpi=pixel)
     plt.close()

 os.system(f"rm {datapath}/*timeseries*")

 return plotts


     

