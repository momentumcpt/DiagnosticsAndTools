'''
    CLUBB standard variables 
    Updates on Jan 2025 
    Zhun Guo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
    Kate Thayer-Calder
    Benjamin A. Stephens:stepheba@ucar.edu
'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import Common_functions
import os
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
import cmaps

from matplotlib import font_manager as fm
from scipy.interpolate import griddata
from subprocess import call

def atm_std_prf (ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs, casedir,varis,cscale,chscale,pname,dofv,datapath):


# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

# varisobs = ["CC_ISBL", "OMEGA","SHUM","CLWC_ISBL", "THETA","RELHUM","U","CIWC_ISBL","T" ]
 nvaris = len(varis)
# cunits = ["%","mba/day","g/kg","g/kg","K", "%", "m/s", "g/kg", "m/s", "m/s","K","m" ]
# cscaleobs = [100,        1,     1, 1000 , 1.,   1,     1,   1000,     1,1,1,1,1,1,1]
# obsdataset =["ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI","ERAI","ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI","ERAI","ERAI"]

 plotstd=["" for x in range(nsite)]


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     plotstd[ire] = pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

     fig, axes = plt.subplots( nrows=nvaris//2, ncols=2, figsize=(15, 15 ))
     axes      = axes.flatten()

     for iv in range (0, nvaris):   

         ax = axes[iv]

         for im in range (0,ncases):
             ncdfs[im]  = datapath+cases[im]+'_site_location.nc'
             infiles[im]= climopath[im][0]+cases[im]+climopath[im][1]+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             lev=inptrs.variables['lev'][:]
             ilev=inptrs.variables['ilev'][:]
             nlev=len(lev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             ncdf.close()
             if (im ==0):
                 A_field = np.zeros((ncases,nlev),np.float32)
                 lev0=lev

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if(dofv[im]):
                     npointlat=idx_lats[ire,0]
                     npointlon=idx_lons[ire,0]
                 if varis[iv] in {'rcm'}: 
                     if (dofv[im]):
                        tmp=inptrs.variables[varis[iv]][0,:,npointlat,npointlon]
                     else:
                        tmp=inptrs.variables[varis[iv]][0,:,npoint]
                     theunits=str(chscale[iv])+'x'+inptrs.variables[varis[iv]].units
                     tmp_o = np.interp(lev0, ilev, tmp)
                 else:
                     if (dofv[im]):
                        tmp=inptrs.variables[varis[iv]][0,:,npointlat,npointlon]
                     else:
                        tmp=inptrs.variables[varis[iv]][0,:,npoint]
                     theunits=str(chscale[iv])+'x'+inptrs.variables[varis[iv]].units
                     tmp_o = np.interp(lev0, lev, tmp)

                 A_field[im,:] = (A_field[im,:]+tmp_o[:]/n[ire]).astype(np.float32 )

             A_field[im,:] = A_field[im,:] * cscale[iv]
             ax.plot(A_field[im, :],lev0, label=cases[im])
             inptrs.close()

         ax.set_title(f'({varis[iv] if iv < len(varis) else "Unknown"})')        
         levind= top_level//1000*72
         if (np.abs(np.min(A_field[:, levind:])) <= 0.001*np.abs(np.max(A_field[:, levind:]))):
             lest=0
         else:
             lest=np.min(A_field[:, levind:])
         maximum = np.max(A_field[:, levind:])
         ax.set_xlim(lest,maximum)

         ax.set_ylim(bottom=top_level, top=1000) 
         ax.set_xlabel('Value')
         ax.grid(True)
         ax.set_ylabel('Pressure Level (hPa)')
         ax.set_xlabel(theunits)
         ax.legend()
         ax.invert_yaxis()

     title_text = pname + f" VAR at {lons[ire]}E, {lats[ire]}N"
     fig.suptitle(title_text,fontsize=16, ha='center', va='center')
     plt.tight_layout(rect=[0, 0, 1, 0.96])
     plt.savefig(plotname+'.'+ptype, dpi=pixel)
     plt.close()

 return plotstd

