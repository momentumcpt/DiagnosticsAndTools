'''
    CLUBB budgets
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
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

def draw_clubb_bgt (ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,dofv,datapath):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# climopath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

 varisobs   = [ "CLOUD", "OMEGA","SHUM","CLWC_ISBL", "THATA","RELHUM"]
 nvaris     = len(varis)
 cunits     = ["%", "mba/day","g/kg","g/kg","K", "%", "mba/day", "K", "g/kg", "m/s", "m/s","K","m"]
 cscaleobs  = [100., 100/86400., 1., 1000, 1., 1., 1, 1,1,1]
 obsdataset = ["CCCM", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI","ERAI","ERAI"]
 
 b_lev = 0 

 plotbgt=["" for x in range(nsite*ncases)] 

 for ire in range (0, nsite):
     for im in range (0,ncases):
         if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
             os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

         plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
         plotbgt[im+ncases*ire] = pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

         fig, axes = plt.subplots( nrows=2, ncols=2, figsize=(15, 15 )) 
         axes      = axes.flatten()

         for iv in range (0, nvaris):
             ax = axes[iv]

             if (varis[iv] == "rtp2" or varis[iv] == "thlp2"):
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_pd', '_cl', '_sf', '_forcing', '_mc']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_cl', '_mc']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == 'upwp' or varis[iv] == "vpwp"):
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_pr4', '_dp1', '_mlf', '_cl', '_mc']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_pr4', '_dp1',  '_cl', '_mc']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_pr4', '_dp1', '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "wprtp") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1', '_mlf', '_cl', '_sicl', '_pd', '_forcing', '_mc']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1',  '_cl',  '_mc']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1',  '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "wpthlp") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1', '_mlf', '_cl', '_sicl',  '_forcing', '_mc']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1',  '_cl',  '_mc']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1',  '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "rtpthlp") :
                 if (b_lev == 2 ): 
                    budget_ends = ['_bt', '_ma', '_ta', '_tp1', '_tp2', '_dp1', '_dp2', '_cl', '_sf', '_forcing', '_mc']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp1', '_tp2', '_dp1', '_dp2', '_cl', '_mc' ]
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp1', '_tp2', '_dp1', '_dp2', '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "wp2") :
                 budget_ends = ["_bt", "_ma", "_ta", "_ac","_bp","_pr1","_pr2", "_pr3","_dp1","_dp2", "_cl", "_pd", "_sf"]
                 if (b_lev == 2 ): 
                    budget_ends = ['_bt', '_ma', '_ta', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1', '_dp2', '_sdmp', '_pd', '_cl', '_sf', '_splat']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_ac', '_bp', '_pr1', '_pr2', '_pr3', '_dp1', '_dp2',  '_cl' , '_splat' ]
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_ac', '_bp', '_pr1', '_dp1', '_dp2',  '_cl'  ]
                 nterms = len (budget_ends)

             if (varis[iv] == "wp3") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp1', '_pr1', '_pr2', '_pr3', '_dp1', '_sdmp', '_cl', '_splat']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp1', '_pr1', '_pr2', '_dp1', '_cl' , '_splat']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_ac', '_bp1', '_pr1', '_pr2', '_dp1', '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "up2" or varis[iv] == "vp2") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_pr1', '_pr2', '_cl', '_pd', '_sf', '_sdmp', '_splat']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_pr1', '_pr2', '_cl' , '_splat']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_tp', '_dp1', '_dp2', '_pr1', '_pr2', '_cl' ]
                 nterms = len (budget_ends)

             if (varis[iv] == "um" or varis[iv] == "vm") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_gf', '_cf', '_ta', '_f', '_sdmp', '_ndg', '_mfl']
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_gf', '_cf', '_ta', '_f']
                 else :
                    budget_ends = ['_bt', '_ma', '_gf', '_cf', '_ta']
                 nterms = len (budget_ends)

             if (varis[iv] == "thlm" or varis[iv] == "rtm") :
                 if (b_lev == 2 ):
                    budget_ends = ['_bt', '_ma', '_ta', '_cl',  '_mc', '_mfl', '_tacl', '_forcing','_sdmp' ]
                 elif (b_lev == 1) :
                    budget_ends = ['_bt', '_ma', '_ta', '_cl',  '_mc']
                 else :
                    budget_ends = ['_bt', '_ma', '_ta', '_cl']
                 nterms = len (budget_ends)

             ncdfs[im]  = datapath+cases[im]+'_site_location.nc'
             infiles[im]= climopath[im][0]+cases[im]+climopath[im][1]+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             ilev=inptrs.variables['ilev'][:]
             nilev=len(ilev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv[im]):
               idx_lats=ncdf.variables['idx_coord_lat'][:,:]
               idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             A_field = np.zeros((nterms,nilev),np.float32)
             theunits=str(chscale[iv])+"x"+inptrs.variables[varis[iv]+'_bt'].units


             for it in range(0, nterms):
                 for subc in range( 0, n[ire]):
                     varis_bgt= varis[iv]+budget_ends[it]
                     npoint=idx_cols[ire,n[subc]-1]-1
                     if(dofv[im]):
                        npointlat=idx_lats[ire,0]
                        npointlon=idx_lons[ire,0]
                     if (dofv[im]):
                        tmp=inptrs.variables[varis_bgt][0,:,npointlat,npointlon]
                     else:
                        tmp=inptrs.variables[varis_bgt][0,:,npoint] #/n[ire]
                     if (varis[iv] == "wprtp" ) :
                         tmp [0:10] = 0.0

                     tmp=tmp*cscale[iv]
                     A_field[it,:] = (A_field[it,:]+tmp[:]/n[ire]).astype(np.float32 )

                 ax.plot(A_field[it, :],ilev, label=varis_bgt[:])
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

         title_text = pname+f"{cases[im]} CLUBB BUDGET at {lons[ire]}E, {lats[ire]}N"
         fig.suptitle(title_text,fontsize=16, ha='center', va='center')
         plt.tight_layout(rect=[0, 0, 1, 0.96])
         plt.savefig(plotname+'.'+ptype, dpi=pixel)
         plt.close()

 return plotbgt

