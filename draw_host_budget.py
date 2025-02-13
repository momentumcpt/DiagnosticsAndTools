'''
    Host Model's budgets, for CESM and E3SM both
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

def draw_host_bgt (ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,dpsc,mpsc,dofv,datapath):

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

 nvaris = len(varis)

 plothostbgt=["" for x in range(nsite*ncases)] 

 for ire in range (0, nsite):
     for im in range (0,ncases):
         if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
             os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

         plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/HOST_Budgets_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
         plothostbgt[im+ncases*ire] = 'HOST_Budgets_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

         fig, axes = plt.subplots( nrows=nvaris//2, ncols=2, figsize=(15, 15 ))
         axes      = axes.flatten()

         for iv in range (0, nvaris):
             ax = axes[iv]

             if (varis[iv] == "Q_PHY" ):
                 budget_ends = ["RVMTEND_CLUBB"]
                 if (dpsc[im] == "zm" ):
                     budget_ends.extend(["ZMDQ", "EVAPQZM"])
                 if (mpsc[im] == 'P3'):
                     budget_ends.extend(["P3_mtend_Q"])
                 elif (mpsc[im] == 'MG'):
                     budget_ends.extend(["MPDQ"])

             if (varis[iv] == "T_PHY" ):
                 if (dofv[im]):
                     budget_ends = ["STEND_CLUBB"]
                 else:
                     budget_ends = ["TTEND_CLUBB"]

                 if (dpsc[im] == "zm" ):
                     budget_ends.extend(["ZMDT", "EVAPTZM", "ZMMTT"])
                 if (mpsc[im] == 'P3'):
                     budget_ends.extend(["P3_mtend_TH"])
                 elif (mpsc[im] == 'MG'):
                     budget_ends.extend(["MPDT", "DPDLFT"])

             if (varis[iv] == "T_DYC") :
                 budget_ends = ["DTCOND", "QRS", "QRL"]#,  "TTGW"]

             if (varis[iv] == "CLOUDLIQ") :
                 budget_ends = ["RCMTEND_CLUBB","DPDLFLIQ"]
                 if (dpsc[im] == "zm" ):
                     budget_ends.extend(["ZMDLIQ"])
                 if (mpsc[im] == 'P3'):
                     budget_ends.extend(["P3_mtend_CLDLIQ"])
                 elif (mpsc[im] == 'MG'):
                     budget_ends.extend([ "MPDLIQ"])

             if (varis[iv] == "CLOUDICE") :
                 budget_ends = ["RIMTEND_CLUBB","DPDLFICE"]
                 if (dpsc[im] == "zm" ):
                     budget_ends.extend(["ZMDICE"])
                 if (mpsc[im] == 'P3'):
                     budget_ends.extend(["P3_mtend_CLDICE"])
                 elif (mpsc[im] == 'MG'):
                     budget_ends.extend([ "MPDICE"])

             nterms = len (budget_ends)

             ncdfs[im]  = datapath+cases[im]+'_site_location.nc'
             infiles[im]= climopath[im][0]+cases[im]+climopath[im][1]+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             ilev=inptrs.variables['lev'][:]
             nilev=len(ilev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv[im]):
               idx_lats=ncdf.variables['idx_coord_lat'][:,:]
               idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             A_field = np.zeros((nterms,nilev),np.float32)
             theunits=str(chscale[iv])+"x"+inptrs.variables[budget_ends[0]].units


             for it in range(0, nterms):
                 for subc in range( 0, n[ire]):
                     varis_bgt= budget_ends[it]
                     npoint=idx_cols[ire,n[subc]-1]-1
                     if(dofv[im]):
                        npointlat=idx_lats[ire,0]
                        npointlon=idx_lons[ire,0]
                     if (dofv[im]):
                        tmp=inptrs.variables[varis_bgt][0,:,npointlat,npointlon]
                     else:
                        tmp=inptrs.variables[varis_bgt][0,:,npoint] 
                     tmp=tmp*cscale[iv]
                     if (varis_bgt == "P3_mtend_TH" ): #or varis_bgt == "STEND_CLUBB" ):
                        tmp=tmp/1004
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

         title_text = pname+f"{cases[im]} HOST MODEL BUDGET at {lons[ire]}E, {lats[ire]}N"
         fig.suptitle(title_text,fontsize=16, ha='center', va='center')
         plt.tight_layout(rect=[0, 0, 1, 0.96])
         plt.savefig(plotname+'.'+ptype, dpi=pixel)
         plt.close()

 return (plothostbgt)

