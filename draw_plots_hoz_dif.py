'''

    Draw Difference plots
    Zhun Guo 
'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import math
import os
import Common_functions
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import cartopy.crs as ccrs
import cmaps

from matplotlib import font_manager as fm
from subprocess import call
from scipy.interpolate import griddata

def traditional_round(number, ndigits=0):                                                                           
        multiplier = 10 ** ndigits                                                                                      
        return int((number * multiplier + 0.5) / multiplier) 

def weighted_rmse(y_true, y_pred, weights):
    assert len(y_true) == len(y_pred) == len(weights), "arrays MUST have same size"
    
    weighted_squared_errors = np.square(y_true - y_pred) * weights
    
    weighted_mse = np.sum(weighted_squared_errors)
    
    wrmse = np.sqrt(weighted_mse / np.sum(weights))
    
    return wrmse

def rmse(obs,pre):
    obs=obs.flatten()
    pre=pre.flatten()
    return np.sqrt(np.sum((obs-pre)**2)/len(obs))

def draw_dif_plot (ptype,pixel,cseason, ncases, cases, casenames, nsite, lats, lons, regridpath, filepathobs,casedir,list_of_parameters,REG,LatS,LatN,LonE, LonW, ncopath,datapath):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# regridpath, regrided model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 if not os.path.exists(casedir+'/2D'):
        os.mkdir(casedir+'/2D') 

 intll   = 20.

 infiles  = ['' for x in range(ncases)] 
 infiles2 = ['' for x in range(ncases)]
 infiles3 = ['' for x in range(ncases)]
 ncdfs    = ['' for x in range(ncases)] 
 alpha    = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','A','B','C','D','E','F','G','H','I','J','K','L','M','N']
 cunits = ['']

 varis    = ['SWCF',          'LWCF']#,           'PRECT'] 
 varisobs = ['toa_cre_sw_mon','toa_cre_lw_mon']#, 'PRECT'] 
 cscale   = [     1,               1,         86400000] 
 cscaleobs =  [1,1,1]
 
 obsdataset=['ceres_ebaf_toa_v4.1','ceres_ebaf_toa_v4.1','GPCP_v2.3']
 rangeyr   =[      '200101_201812',     '200101_201812',          '']

# no need to edit
 nvaris = len(varis)
 plotdif=['' for x in range(nvaris)]
 cmap1 = cmaps.temp_diff_18lev  # color bars 

 for iv in range(0, nvaris):
# make the "right" levels for each variables  
   levels=np.array([-60,-50,-40,-30,-20,-10,-5,0,5,10,20,30,40,50,60])
   print(varis[iv])
   if(varis[iv] == 'CLDTOT' or varis[iv] == 'CLDLOW' or varis[iv] == 'CLDHGH'):
      levels=levels *1 
   if(varis[iv] == 'LWCF'):
      levels=levels *0.5
   if(varis[iv] == 'SWCF' or varis[iv] =='FLUT'):
      levels=levels *1
   if(varis[iv] == 'PRECT' or varis[iv]=='QFLX'):
      levels=levels *1
   if(varis[iv] == 'LHFLX'):
      levels=levels *1
   if(varis[iv] == 'SHFLX'):
      levels=levels *1
   if(varis[iv] == 'U10'):
      levels=levels *0.1
   if(varis[iv] == 'TMQ'):
      levels=levels *0.5
   if(varis[iv] == 'TGCLDLWP'):
      levels=levels *1

#  Observational data
   if(obsdataset[iv] =='CCCM'):
       if(cseason == 'ANN'):
           fileobs = '/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-'+cseason+'.nc'
       else:
           fileobs = '/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-2010-'+cseason+'.nc'
   else:
       if (varisobs[iv] == 'PRECT' or varis[iv] == 'CLDTOT' or varis[iv] == 'CLDLOW' or varis[iv] == 'CLDHGH'):
           fileobs = filepathobs+'/'+obsdataset[iv]+'/'+obsdataset[iv]+'_'+cseason+'_climo.nc'
       else:
           fileobs = filepathobs + '/'+obsdataset[iv]+'/'+obsdataset[iv]+'_'+cseason+'_'+rangeyr[iv] +'_climo.nc'

   inptrobs = Dataset(fileobs,'r') 
   latobs=inptrobs.variables['lat'][:]
   lonobs=inptrobs.variables['lon'][:]
   if (varisobs[iv] =='U10'):
      B0=inptrobs.variables[varisobs[iv]][0,:,:] 
      B1=inptrobs.variables['V10'][0,:,:]
      B=(B0*B0+B1*B1)
      B=B * cscaleobs[iv]
      B=np.sqrt(B)
   elif (varisobs[iv] == 'MSWCF'):
      B=inptrobs.variables['toa_cre_sw_mon'][0,:,:]
      B=B * cscaleobs[iv] *(-1)
   elif (varisobs[iv] == 'wap'):
      levobs=inptrobs.variables['plev'][:]
      levobs_idx = np.abs(levobs - clevel*100).argmin()
      B=inptrobs.variables['wap'][0,levobs_idx,:,:]
   else:
      B=inptrobs.variables[varisobs[iv]][0,:,:]
      B=B * cscaleobs[iv]
      if (obsdataset[iv] =='CALIPSOCOSP'):
          B=np.maximum(B,0)
   inptrobs.close()
# Obs data

   #************************************************
   # create plot
   #************************************************
   plotname = casedir+'/2D/Diffplot_'+varis[iv]+'_'+cseason
   plotdif[iv] = 'Diffplot_'+varis[iv]+'_'+cseason

   nplt     = ncases

   fig, axes = plt.subplots( nrows= traditional_round(nplt/2), ncols=2, figsize=(12, 8 ), subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
   axes      = axes.flatten()

   for im in range(0, ncases):
       ncdfs[im]  = datapath+cases[im]+'_site_location.nc' 
       infiles[im] = regridpath[im][0]+cases[im]+regridpath[im][1]+cases[im]+'_'+cseason+'_climo.nc'
       inptrs  = Dataset(infiles[im],'r')       # regular SE file (before remap) as A 

       lat=inptrs.variables['lat'][:]
       nlat=len(lat)
       lon=inptrs.variables['lon'][:]
       nlon=len(lon)
#       area=inptrs.variables['area'][:]

       area_wgt = np.zeros(nlat)

       sits=np.linspace(0,nsite-1,nsite)
       ncdf= Dataset(ncdfs[im],'r')
       n   =ncdf.variables['n'][:]
       idx_cols=ncdf.variables['idx_cols'][:]

       infiles2[im] = regridpath[im][0]+cases[im]+regridpath[im][1]+cases[im]+'_ANN_climo.nc'
       inptrs2 = Dataset(infiles2[im],'r')       # Read the remaped file. Lat-lon as C!
       rlat=inptrs2.variables['lat'][:]
       rlon=inptrs2.variables['lon'][:]

       weights=rlat
       weights=np.cos(rlat*3.1415/180)
       weights_2d=np.tile(weights.reshape(len(rlat), 1), (1, len(rlon)))

       if (varis[iv] != 'O500' and varis[iv] != 'PRECT' and varis[iv] != 'FLUT' and varis[iv] != 'U10' and varis[iv] != 'MSWCF'):
           A  = inptrs.variables[varis[iv]][0,:]
           C  = inptrs2.variables[varis[iv]][0,:,:]
       elif (varis[iv] == 'MSWCF'):
           A  = inptrs.variables['SWCF'][0,:]
           A  = A* (-1)
           C  = inptrs2.variables['SWCF'][0,:,:]
           C  = C* (-1)
       elif (varis[iv] == 'PRECT'):
           A  = inptrs.variables['PRECC'][0,:]+inptrs.variables['PRECL'][0,:]
           C  = inptrs2.variables['PRECC'][0,:,:]+inptrs2.variables['PRECL'][0,:,:]
       elif (varis[iv] == 'U10'):
           A  = inptrs.variables['U10'][0,:]*inptrs.variables['U10'][0,:]
           A  = np.sqrt(A)
           C  = inptrs2.variables['U10'][0,:,:]*inptrs2.variables['U10'][0,:,:]
           C  = np.sqrt(C)
       elif (varis[iv] == 'O500'):
           lev=inptrs.variables['lev'][:]
           lev_idx = np.abs(lev - clevel).argmin()
           A  = inptrs.variables['OMEGA'][0,lev_idx,:]
       elif (varis[iv] == 'FLUT'):
           A  = inptrs.variables['FLUT'][0,:]-inptrs.variables['FLNS'][0,:]
           C  = inptrs2.variables['FLUT'][0,:,:]-inptrs2.variables['FLNS'][0,:,:]

# A_xy is not used here, because diff plots MUST use the lat-lon format! C_xy is in lat-lon
       A_xy = A
       A_xy = A_xy * cscale[iv]
       C_xy = C
       C_xy = C_xy * cscale[iv]

       D    = B  # B means obs
       D    = C_xy-B         

       ax = axes[im]
       # grid boxes
       gl = ax.gridlines(
           crs=ccrs.PlateCarree(),
           draw_labels=True,
           linewidth=0.5,
           color='black',
           alpha=0.5,
           linestyle='--'
       )

       #  matplotlib.ticker  FixedLocator 
       gl.xlocator = ticker.FixedLocator(np.arange(-180, 181, intll))
       gl.ylocator = ticker.FixedLocator(np.arange(-90, 91, intll))

# We dont need the labels on top and right
       gl.top_labels   = False
       gl.right_labels = False
       ax.plot = ax.contourf(rlon, rlat,D,
                               levels=levels,  
                               transform=ccrs.PlateCarree(),  # 
                               cmap=cmap1,  # colors
                               extend='both')  

       ax.coastlines()
       ax.set_linewidth=2
       ax.spines['geo'].set_linewidth(1) 
       text_properties = fm.FontProperties( size=14,weight='bold')
       ax.set_title(casenames[im],fontproperties=text_properties,loc='left')

       RMSE= round(weighted_rmse(B,C_xy,weights_2d),2)
       print(RMSE)
       ax.set_title('RMSE='+str(RMSE),fontproperties=text_properties,loc='right')
#  END LOP

   title_text = f"{varis[iv]}" 
   cbar_ax = fig.add_axes([0.1, 0.035, 0.8, 0.02])
   cbar = fig.colorbar(ax.plot, cax=cbar_ax, orientation='horizontal')
   fig.suptitle(title_text,fontsize=16, ha='center', va='center')
   plt.tight_layout()
#   plt.tight_layout(rect=[0, 0, 1, 1])
   plt.savefig(plotname+'.'+ptype, dpi=pixel)

   plt.close()

   del(fig)
   ncdf.close()   
   inptrs.close()
   inptrs2.close()

 return plotdif
