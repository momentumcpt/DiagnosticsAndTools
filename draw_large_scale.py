'''
    Large-scale variables (compared with observations)
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

def large_scale_prf (ptype,pixel,cseason, top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs, casedir,dofv, datapath,pname):


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

 varis    = [ "CLOUD"  , "OMEGA",   "Q",   "CLDLIQ", "THETA","RELHUM","U",   "CLDICE","T"]
 varisobs = ["CC_ISBL", "OMEGA","SHUM","CLWC_ISBL", "THETA","RELHUM","U","CIWC_ISBL","T" ]
 nvaris = len(varis)
 cunits = ["%","mba/day","g/kg","g/kg","K", "%", "m/s", "g/kg", "m/s", "m/s","K","m" ]
 cscale = [100,      864,  1000, 1000 , 1.,   1,     1,   1000,     1,1,1,1,1,1,1 ]
 cscaleobs  = [100,        1,     1, 1000 , 1.,   1,     1,   1000,     1,1,1,1,1,1,1]
 obsdataset = ["ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI","ERAI","ERAI"]
 rangeyr    = ['197901_201612','197901_201612','197901_201612','197901_201612','197901_201612','197901_201612','197901_201612','197901_201612','197901_201612','197901_201612']

 plotlgs=["" for x in range(nsite)]

 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')
     if(top_level  == 0):
           plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
           plotlgs[ire] = pname+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     else:
           plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/lev_'+pname+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
           plotlgs[ire] = 'lev_'+pname+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

     fig, axes = plt.subplots( nrows=3, ncols=3, figsize=(15, 15 )) 
     axes      = axes.flatten()

     for iv in range (0, nvaris): 

         if(obsdataset[iv] =="CCCM"):
             if(cseason == "ANN"):
                 fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-"+cseason+".nc"
             else:
                 fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-2010-"+cseason+".nc"
             inptrobs = Dataset(fileobs,'r')
             latobs=inptrobs.variables['lat'][:]
             latobs_idx = np.abs(latobs - lats[ire]).argmin()
             lonobs=inptrobs.variables['lon'][:]
             lonobs_idx = np.abs(lonobs - lons[ire]).argmin()

             B=inptrobs.variables[varisobs[iv]][:,latobs_idx,lonobs_idx]
         else:
             if (varisobs[iv] =="PRECT"):
                 fileobs = filepathobs+'/GPCP_'+cseason+'_climo.nc'
             else:
              #   fileobs = filepathobs + '/'+obsdataset[iv]+'/'+obsdataset[iv]+'_'+cseason+'_'+rangeyr[iv]+'_climo.nc'
                 fileobs = filepathobs + '/'+obsdataset[iv]+'_'+cseason+'_climo.nc'
             inptrobs = Dataset(fileobs,'r')
             if (varisobs[iv] =="THETA"):
                 latobs=inptrobs.variables['lat'][:]
                 latobs_idx = np.abs(latobs - lats[ire]).argmin()
                 lonobs=inptrobs.variables['lon'][:]
                 lonobs_idx = np.abs(lonobs - lons[ire]).argmin()
                 B = inptrobs.variables['T'][0,:,latobs_idx,lonobs_idx]
                 pre1 = inptrobs.variables['lev'][:]
                 for il1 in range (0, len(pre1)):
                     B[il1] = B[il1]*(1000/pre1[il1])**0.286
             else: 
                 pre1 = inptrobs.variables['lev'][:]
                 latobs=inptrobs.variables['lat'][:]
                 latobs_idx = np.abs(latobs - lats[ire]).argmin()
                 lonobs=inptrobs.variables['lon'][:]
                 lonobs_idx = np.abs(lonobs - lons[ire]).argmin()

                 B = inptrobs.variables[varisobs[iv]][0,:,latobs_idx,lonobs_idx]

         B[:]=B[:] * cscaleobs[iv]

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
             nlev=len(lev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv[im]):
                 idx_lats=ncdf.variables['idx_coord_lat'][:,:]
                 idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             if (im ==0):
                 A_field = np.zeros((ncases,nlev),np.float32)
                 lev0=lev

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if (dofv[im]):
                    npointlat=idx_lats[ire,0]
                    npointlon=idx_lons[ire,0]
                 if (dofv[im]):
                    ps=inptrs.variables['PS'][0,npointlat,npointlon]
                 else:
                    ps=inptrs.variables['PS'][0,npoint]

                 hyam =inptrs.variables['hyam'][:]
                 hybm =inptrs.variables['hybm'][:]
                 ps=ps
                 p0=100000 #inptrs.variables['P0']
                 pre = np.zeros((nlev),np.float32)

                 for il in range (0, nlev):
                     pre[il] = hyam[il]*p0 + hybm[il] * ps
                 lev = pre/100

                 if (varis[iv] == 'THETA'):
                     if (dofv[im]):
                       tmp = inptrs.variables['T'][0,:,npointlat,npointlon]
                     else:
                       tmp = inptrs.variables['T'][0,:,npoint]
                     for il in range (0, nlev):
                         tmp[il] = tmp[il] * (100000/pre[il])**0.286
                     theunits=str(cscale[iv])+"x"+inptrs.variables['T'].units
                 else:
                     if(dofv[im]):
                       tmp=inptrs.variables[varis[iv]][0,:,npointlat,npointlon]
                     else:
                       tmp=inptrs.variables[varis[iv]][0,:,npoint] 
                     theunits=str(cscale[iv])+"x"+inptrs.variables[varis[iv]].units
                     
                 tmp_o = np.interp(pre, lev, tmp)

                 A_field[im,:] = (A_field[im,:]+tmp_o[:]/n[ire]).astype(np.float32 )

             A_field[im,:] = A_field[im,:] *cscale[iv]
             ax.plot(A_field[im, :], pre, label=cases[im])
             inptrs.close()

         ax.plot( B,pre1, label='OBS', linestyle='--')

         if(varis[iv] == "THETA"):
             ax.set_xlim(270, 400)
         if(varis[iv] == "CLOUD" or varis[iv] =="RELHUM") :
             ax.set_xlim(0, 100)
         if(varis[iv] == "T") :
             ax.set_xlim(180, 300)
         if(varis[iv] == "U") :
             ax.set_xlim(-40, 40)

         ax.set_ylim(bottom=top_level, top=1000)
         ax.set_xlabel('Value')
         ax.grid(True)
         ax.set_title(f'({varis[iv] if iv < len(varis) else "Unknown"})')
         ax.set_ylabel('Pressure Level (hPa)')  #
         ax.set_xlabel(theunits)  # 
         ax.legend()  
         ax.invert_yaxis()

     title_text = f"Large-scale VAR at {lons[ire]}E, {lats[ire]}N"
     fig.suptitle(title_text,fontsize=16, ha='center', va='center')
     plt.tight_layout(rect=[0, 0, 1, 0.96])
     plt.savefig(plotname+'.'+ptype, dpi=pixel)
     plt.close()

 return plotlgs
